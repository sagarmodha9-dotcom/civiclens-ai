"""Ingestion client tests against a MOCKED USAspending (respx). These prove the client's behaviour: retries,
timeouts, pagination, download polling, manifests, idempotency. They prove nothing about the real API; that is
`probe.py`'s job and its output lives in evidence/probe/. Fixture shapes are labelled SYNTHETIC."""
from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

import httpx
import pytest
import respx

from civiclens_ingest.client import BASE, ApiError, UsaSpendingClient, contract_filters, fy_window
from civiclens_ingest.worker import pull_cell

# shape recorded live by probe.py on 2026-10-23 (new names + deprecated twins); values synthetic
SYNTHETIC_COUNT = {"calculated_count": 3, "maximum_limit": 500000, "rows_gt_limit": False, "spending_level": "transactions",
                   "calculated_transaction_count": 3, "maximum_transaction_limit": 500000, "transaction_rows_gt_limit": False, "messages": []}


def client(**kw):
    return UsaSpendingClient(sleep=lambda s: None, **kw)


# ------------------------------------------------------------------ fiscal year + filters
@pytest.mark.parametrize("fy,start,end", [(2022, "2021-10-01", "2022-09-30"), (2026, "2025-10-01", "2026-09-30")])
def test_fy_window_boundaries(fy, start, end):
    assert fy_window(fy) == (start, end)


def test_contract_filters_are_the_single_scope_definition():
    f = contract_filters("Department of Veterans Affairs", 2025)
    assert f["time_period"] == [{"start_date": "2024-10-01", "end_date": "2025-09-30", "date_type": "action_date"}]
    assert f["award_type_codes"] == ["A", "B", "C", "D"]
    assert f["psc_codes"] == {"require": [["Service", "D"], ["Product", "70"]]}
    assert f["agencies"] == [{"type": "awarding", "tier": "toptier", "name": "Department of Veterans Affairs"}]


# ------------------------------------------------------------------ retries / timeouts
@respx.mock
def test_retries_on_503_then_succeeds_and_records_attempts():
    route = respx.post(f"{BASE}/api/v2/download/count/").mock(side_effect=[
        httpx.Response(503), httpx.Response(429, headers={"retry-after": "1"}), httpx.Response(200, json=SYNTHETIC_COUNT)])
    c = client()
    assert c.download_count({})["calculated_transaction_count"] == 3
    assert route.call_count == 3 and c.records[-1].attempts == 3 and c.records[-1].status == 200


@respx.mock
def test_transport_timeout_is_retried_then_surfaced_as_apierror():
    respx.get(f"{BASE}/api/v2/awards/last_updated/").mock(side_effect=httpx.ReadTimeout("slow"))
    c = client(max_retries=2)
    with pytest.raises(ApiError) as ei:
        c.last_updated()
    assert "ReadTimeout" in str(ei.value) and c.records[-1].attempts == 3


@respx.mock
def test_4xx_is_not_retried():
    route = respx.post(f"{BASE}/api/v2/download/count/").mock(return_value=httpx.Response(422, json={"detail": "bad filter"}))
    with pytest.raises(ApiError) as ei:
        client().download_count({"bad": 1})
    assert ei.value.status == 422 and route.call_count == 1


# ------------------------------------------------------------------ pagination
@respx.mock
def test_iter_awards_follows_hasNext_and_passes_keyset_fields():
    bodies = []

    def handler(request):
        body = json.loads(request.content); bodies.append(body)
        if body["page"] == 1:
            return httpx.Response(200, json={"results": [{"generated_internal_id": "CONT_AWD_1"}, {"generated_internal_id": "CONT_AWD_2"}],
                                             "page_metadata": {"page": 1, "hasNext": True, "last_record_unique_id": 2, "last_record_sort_value": "100"}})
        return httpx.Response(200, json={"results": [{"generated_internal_id": "CONT_AWD_3"}], "page_metadata": {"page": 2, "hasNext": False}})
    respx.post(f"{BASE}/api/v2/search/spending_by_award/").mock(side_effect=handler)
    ids = [r["generated_internal_id"] for r in client().iter_awards({}, ["Award ID"], limit=2)]
    assert ids == ["CONT_AWD_1", "CONT_AWD_2", "CONT_AWD_3"]
    assert bodies[1]["last_record_unique_id"] == 2 and bodies[1]["last_record_sort_value"] == "100"
    assert all(b["spending_level"] == "awards" for b in bodies)


# ------------------------------------------------------------------ download polling
@respx.mock
def test_wait_for_download_polls_until_finished_and_fails_on_failed():
    respx.get(f"{BASE}/api/v2/download/status/").mock(side_effect=[
        httpx.Response(200, json={"status": "running"}), httpx.Response(200, json={"status": "running"}),
        httpx.Response(200, json={"status": "finished", "file_url": "https://files.example/x.zip", "total_rows": 3})])
    assert client().wait_for_download("x.zip", poll_seconds=1)["total_rows"] == 3
    respx.get(f"{BASE}/api/v2/download/status/").mock(return_value=httpx.Response(200, json={"status": "failed", "message": "boom"}))
    with pytest.raises(ApiError):
        client().wait_for_download("x.zip", poll_seconds=1)


@respx.mock
def test_wait_for_download_gives_up_after_max_wait():
    respx.get(f"{BASE}/api/v2/download/status/").mock(return_value=httpx.Response(200, json={"status": "running"}))
    with pytest.raises(ApiError) as ei:
        client().wait_for_download("x.zip", poll_seconds=10, max_wait_seconds=30)
    assert "not finished" in str(ei.value)


# ------------------------------------------------------------------ worker: manifest, idempotency, atomic swap
def _zip_bytes(rows: int, subaward_rows: int = 2) -> bytes:
    """Mirrors the live zip layout (PrimeTransactionsAndSubawards_*.zip): one prime-transactions CSV and one
    sub-awards CSV. The sub-award rows must never be counted as prime spend."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("Contracts_PrimeTransactions_1.csv", "contract_transaction_unique_key,action_date,federal_action_obligation\n" +
                   "\n".join(f"K{i},2025-01-0{i+1},{1000*(i+1)}" for i in range(rows)) + "\n")
        z.writestr("Contracts_Subawards_1.csv", "subaward_unique_key,prime_award_unique_key,subaward_amount\n" +
                   "\n".join(f"S{i},K0,{100*(i+1)}" for i in range(subaward_rows)) + "\n")
    return buf.getvalue()


def _mock_download(rows_in_zip: int, count: int = 3):
    respx.get(f"{BASE}/api/v2/awards/last_updated/").mock(return_value=httpx.Response(200, json={"last_updated": "10/22/2026"}))
    respx.post(f"{BASE}/api/v2/download/count/").mock(return_value=httpx.Response(200, json={**SYNTHETIC_COUNT, "calculated_count": count, "calculated_transaction_count": count}))
    respx.post(f"{BASE}/api/v2/download/transactions/").mock(return_value=httpx.Response(200, json={"file_name": "PrimeTransactionsAndSubawards_job1.zip", "file_url": "https://files.example/job1.zip", "status_url": "..."}))
    # live: status.total_rows counts prime + sub-award rows together (272 vs 235 for SSA FY2026)
    respx.get(f"{BASE}/api/v2/download/status/").mock(return_value=httpx.Response(200, json={"status": "finished", "file_url": "https://files.example/job1.zip", "total_rows": rows_in_zip + 2, "total_columns": 415}))
    return respx.get("https://files.example/job1.zip").mock(return_value=httpx.Response(200, content=_zip_bytes(rows_in_zip)))


@respx.mock
def test_pull_cell_writes_manifest_with_provenance_and_matching_counts(tmp_path: Path):
    _mock_download(3)
    m = pull_cell(client(), tmp_path, "036", "Department of Veterans Affairs", 2025, poll_seconds=0)
    d = tmp_path / "agency=036" / "fy=2025"
    assert m["status"] == "complete" and m["rows_total"] == 3 and m["count_matches"] is True
    assert m["rows_subawards"] == 2 and m["download_total_rows_all_files"] == 5     # sub-awards kept, never counted as prime
    assert (d / "manifest.json").exists() and (d / "Contracts_PrimeTransactions_1.csv").exists()
    saved = json.loads((d / "manifest.json").read_text())
    for key in ("request", "filter_hash", "extracted_utc", "api_last_updated", "api_count", "zip", "files", "calls"):
        assert key in saved, key
    assert saved["files"][0]["sha256"] and saved["zip"]["sha256"] and saved["request"]["filters"]["time_period"][0]["start_date"] == "2024-10-01"
    assert not [p for p in d.iterdir() if p.name.startswith("civiclens-")]      # temp dir cleaned


@respx.mock
def test_pull_cell_is_idempotent_when_nothing_changed(tmp_path: Path):
    dl = _mock_download(3)
    pull_cell(client(), tmp_path, "036", "VA", 2025, poll_seconds=0)
    m2 = pull_cell(client(), tmp_path, "036", "VA", 2025, poll_seconds=0)
    assert m2.get("skipped") is True and dl.call_count == 1          # second run did not download again


@respx.mock
def test_pull_cell_repulls_when_api_count_changed(tmp_path: Path):
    dl = _mock_download(3)
    pull_cell(client(), tmp_path, "036", "VA", 2025, poll_seconds=0)
    respx.post(f"{BASE}/api/v2/download/count/").mock(return_value=httpx.Response(200, json={**SYNTHETIC_COUNT, "calculated_count": 4, "calculated_transaction_count": 4}))
    respx.get("https://files.example/job1.zip").mock(return_value=httpx.Response(200, content=_zip_bytes(4)))
    m = pull_cell(client(), tmp_path, "036", "VA", 2025, poll_seconds=0)
    assert m.get("skipped") is None and m["rows_total"] == 4 and m["count_matches"] is True


@respx.mock
def test_count_mismatch_is_flagged_not_hidden(tmp_path: Path):
    _mock_download(rows_in_zip=2, count=3)
    m = pull_cell(client(), tmp_path, "036", "VA", 2025, poll_seconds=0)
    assert m["status"] == "count_mismatch" and m["rows_total"] == 2 and m["api_count"] == 3


@respx.mock
def test_over_limit_cell_refuses_instead_of_truncating(tmp_path: Path):
    respx.get(f"{BASE}/api/v2/awards/last_updated/").mock(return_value=httpx.Response(200, json={"last_updated": "10/22/2026"}))
    respx.post(f"{BASE}/api/v2/download/count/").mock(return_value=httpx.Response(200, json={**SYNTHETIC_COUNT, "rows_gt_limit": True, "transaction_rows_gt_limit": True}))
    with pytest.raises(ApiError) as ei:
        pull_cell(client(), tmp_path, "036", "VA", 2025, poll_seconds=0)
    assert "split the cell" in str(ei.value)


@respx.mock
def test_failed_download_leaves_previous_files_untouched(tmp_path: Path):
    _mock_download(3)
    pull_cell(client(), tmp_path, "036", "VA", 2025, poll_seconds=0)
    d = tmp_path / "agency=036" / "fy=2025"
    before = (d / "manifest.json").read_text()
    respx.post(f"{BASE}/api/v2/download/count/").mock(return_value=httpx.Response(200, json={**SYNTHETIC_COUNT, "calculated_count": 9, "calculated_transaction_count": 9}))
    respx.get(f"{BASE}/api/v2/download/status/").mock(return_value=httpx.Response(200, json={"status": "failed", "message": "boom"}))
    with pytest.raises(ApiError):
        pull_cell(client(), tmp_path, "036", "VA", 2025, poll_seconds=0)
    assert (d / "manifest.json").read_text() == before and (d / "Contracts_PrimeTransactions_1.csv").exists()


@respx.mock
def test_zip_without_a_prime_transactions_file_is_refused(tmp_path: Path):
    _mock_download(3)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("Contracts_Subawards_1.csv", "subaward_unique_key\nS1\n")
    respx.get("https://files.example/job1.zip").mock(return_value=httpx.Response(200, content=buf.getvalue()))
    with pytest.raises(ApiError) as ei:
        pull_cell(client(), tmp_path, "036", "VA", 2025, poll_seconds=0)
    assert "no prime-transactions CSV" in str(ei.value)


def test_requests_carry_spending_level_not_deprecated_subawards_flag():
    import inspect
    from civiclens_ingest import client as mod
    src = inspect.getsource(mod)
    assert '"subawards": False' not in src and '"spending_level"' in src


def test_award_transactions_paginates_and_window_filter_is_same_grain():
    """R2's grain: our FY-window transactions vs the award's own transactions in the SAME window. Lifetime totals must
    never enter the comparison. Mocked two-page transaction list across two fiscal years."""
    import respx as _respx
    with _respx.mock:
        pages = iter([
            httpx.Response(200, json={"results": [{"action_date": "2024-11-01", "federal_action_obligation": 100.0}, {"action_date": "2025-03-01", "federal_action_obligation": -20.0}],
                                      "page_metadata": {"hasNext": True}}),
            httpx.Response(200, json={"results": [{"action_date": "2025-10-15", "federal_action_obligation": 999.0}], "page_metadata": {"hasNext": False}}),
        ])
        _respx.post(f"{BASE}/api/v2/transactions/").mock(side_effect=lambda req: next(pages))
        tx = client().award_transactions("CONT_AWD_X")
    assert len(tx) == 3
    start, end = fy_window(2025)
    win = [t for t in tx if start <= t["action_date"] <= end]
    assert len(win) == 2 and round(sum(t["federal_action_obligation"] for t in win), 2) == 80.0     # FY2026 row excluded



def test_pull_all_records_internal_failures_and_continues(tmp_path, monkeypatch, capsys):
    """Regression for the 13:40Z full run: an exception that was not an ApiError escaped pull_all after 5 cells and
    the report was never written. Now any exception is recorded per cell and the run continues."""
    import sys
    from civiclens_ingest import pull_all as pa
    calls = []

    def fake_pull(c, root, code, name, fy, force=False, poll_seconds=10):
        calls.append((code, fy))
        if (code, fy) == ("070", 2022):
            raise zipfile.BadZipFile("File is not a zip file")
        return {"agency_code": code, "agency_name": name, "fiscal_year": fy, "status": "complete", "rows_total": 1, "api_count": 1,
                "count_matches": True, "rows_subawards": 0, "extracted_utc": "x", "api_last_updated": "x", "run_id": "r"}
    monkeypatch.setattr(pa, "pull_cell", fake_pull)
    monkeypatch.setattr(pa, "UsaSpendingClient", lambda: type("C", (), {"close": lambda self: None})())
    monkeypatch.setattr(sys, "argv", ["pull_all", "--out", str(tmp_path / "raw"), "--report", str(tmp_path / "rep"), "--only", "036,070", "--fys", "2022,2023"])
    rc = pa.main()
    assert rc == 1 and len(calls) == 4                                     # kept going after the failure
    rep = json.loads((tmp_path / "rep" / "report.json").read_text())
    assert rep["totals"]["cells_failed"] == 1 and rep["failures"][0]["kind"] == "internal" and "BadZipFile" in rep["failures"][0]["error"]
    assert "Failure details" in (tmp_path / "rep" / "report.md").read_text()



@respx.mock
def test_fetch_file_retries_a_dropped_connection_then_succeeds(tmp_path: Path):
    """Regression for run 39961334170: the zip fetch hit a transport error after the job finished. Two failures then
    a good response must yield a complete file with the right hash; a partial file must not be left behind."""
    body = _zip_bytes(3)
    respx.get("https://files.example/big.zip").mock(side_effect=[httpx.ReadTimeout("headers"), httpx.RemoteProtocolError("dropped"),
                                                                  httpx.Response(200, content=body)])
    c = client()
    meta = c.fetch_file("https://files.example/big.zip", tmp_path / "big.zip")
    import hashlib
    assert meta["attempts"] == 3 and meta["sha256"] == hashlib.sha256(body).hexdigest() and (tmp_path / "big.zip").read_bytes() == body


@respx.mock
def test_fetch_file_gives_up_as_apierror_and_leaves_no_partial_file(tmp_path: Path):
    respx.get("https://files.example/big.zip").mock(side_effect=httpx.ReadTimeout("headers"))
    with pytest.raises(ApiError) as ei:
        client(max_retries=2).fetch_file("https://files.example/big.zip", tmp_path / "big.zip")
    assert "after 3 attempts" in str(ei.value) and not (tmp_path / "big.zip").exists()


# ------------------------------------------------------------------ cached download jobs (observed live 2026-10-23)
def test_split_time_period_covers_the_same_window_without_overlap():
    from civiclens_ingest.client import split_time_period
    f = contract_filters("Department of the Treasury", 2023)
    alt = split_time_period(f)
    tp = alt["time_period"]
    assert [ (t["start_date"], t["end_date"]) for t in tp ] == [("2022-10-01", "2023-03-31"), ("2023-04-01", "2023-09-30")]
    assert all(t["date_type"] == "action_date" for t in tp)
    assert {k: v for k, v in alt.items() if k != "time_period"} == {k: v for k, v in f.items() if k != "time_period"}
    assert f["time_period"] != tp and len(f["time_period"]) == 1          # original untouched


def test_job_created_utc_parses_live_file_names():
    from civiclens_ingest.client import job_created_utc
    t = job_created_utc("PrimeTransactionsAndSubawards_2026-10-23_H15M13S54923263.zip")
    assert t.isoformat() == "2026-10-23T15:13:54+00:00"
    assert job_created_utc("PrimeTransactionsAndSubawards_job1.zip") is None


@respx.mock
def test_cached_download_job_triggers_a_fresh_equivalent_request(tmp_path: Path):
    """Regression for Treasury FY2023-26: the API returned a 15-minute-old job for an identical request while the
    count had moved on. The worker must notice the stale job, prove the split-window variant has the same count,
    and request again with it."""
    import datetime as dt
    stale_name = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=15)).strftime("PrimeTransactionsAndSubawards_%Y-%m-%d_H%HM%MS%S000000.zip")
    fresh_name = dt.datetime.now(dt.timezone.utc).strftime("PrimeTransactionsAndSubawards_%Y-%m-%d_H%HM%MS%S111111.zip")
    _mock_download(3)
    dl_route = respx.post(f"{BASE}/api/v2/download/transactions/").mock(side_effect=[
        httpx.Response(200, json={"file_name": stale_name, "file_url": "https://files.example/stale.zip"}),
        httpx.Response(200, json={"file_name": fresh_name, "file_url": "https://files.example/fresh.zip"})])
    respx.get(f"{BASE}/api/v2/download/status/").mock(return_value=httpx.Response(200, json={"status": "finished", "file_url": "https://files.example/fresh.zip", "total_rows": 5, "total_columns": 415}))
    respx.get("https://files.example/fresh.zip").mock(return_value=httpx.Response(200, content=_zip_bytes(3)))
    stale = respx.get("https://files.example/stale.zip").mock(return_value=httpx.Response(200, content=_zip_bytes(2)))
    m = pull_cell(client(), tmp_path, "020", "Department of the Treasury", 2023, poll_seconds=0)
    assert dl_route.call_count == 2 and stale.call_count == 0            # stale zip never fetched
    second_body = json.loads(dl_route.calls[1].request.content)
    assert len(second_body["filters"]["time_period"]) == 2                 # variant request used
    assert m["download_was_cached"] is True and m["request"]["variant"] == "split_time_period"
    assert m["request"]["variant_count"] == 3 and m["request"]["scope_filters"]["time_period"][0]["start_date"] == "2022-10-01"
    assert m["status"] == "complete" and m["rows_total"] == 3


@respx.mock
def test_variant_with_a_different_count_is_refused(tmp_path: Path):
    import datetime as dt
    stale_name = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=15)).strftime("PrimeTransactionsAndSubawards_%Y-%m-%d_H%HM%MS%S000000.zip")
    _mock_download(3)
    respx.post(f"{BASE}/api/v2/download/transactions/").mock(return_value=httpx.Response(200, json={"file_name": stale_name, "file_url": "https://files.example/stale.zip"}))
    respx.post(f"{BASE}/api/v2/download/count/").mock(side_effect=[
        httpx.Response(200, json={**SYNTHETIC_COUNT, "calculated_count": 3}), httpx.Response(200, json={**SYNTHETIC_COUNT, "calculated_count": 2})])
    with pytest.raises(ApiError) as ei:
        pull_cell(client(), tmp_path, "020", "Department of the Treasury", 2023, poll_seconds=0)
    assert "split-window count 2 != standard count 3" in str(ei.value)
    assert not (tmp_path / "agency=020" / "fy=2023" / "manifest.json").exists()


@respx.mock
def test_fresh_job_is_not_treated_as_cached(tmp_path: Path):
    import datetime as dt
    fresh_name = dt.datetime.now(dt.timezone.utc).strftime("PrimeTransactionsAndSubawards_%Y-%m-%d_H%HM%MS%S111111.zip")
    _mock_download(3)
    dl_route = respx.post(f"{BASE}/api/v2/download/transactions/").mock(return_value=httpx.Response(200, json={"file_name": fresh_name, "file_url": "https://files.example/job1.zip"}))
    m = pull_cell(client(), tmp_path, "036", "VA", 2025, poll_seconds=0)
    assert dl_route.call_count == 1 and m["download_was_cached"] is False and m["request"]["variant"] == "standard"
