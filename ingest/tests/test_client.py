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

SYNTHETIC_COUNT = {"calculated_transaction_count": 3, "maximum_transaction_limit": 500000, "transaction_rows_gt_limit": False}


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
    assert all(b["subawards"] is False for b in bodies)


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
def _zip_bytes(rows: int) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("Contracts_PrimeTransactions_1.csv", "contract_transaction_unique_key,action_date,federal_action_obligation\n" +
                   "\n".join(f"K{i},2025-01-0{i+1},{1000*(i+1)}" for i in range(rows)) + "\n")
    return buf.getvalue()


def _mock_download(rows_in_zip: int, count: int = 3):
    respx.get(f"{BASE}/api/v2/awards/last_updated/").mock(return_value=httpx.Response(200, json={"last_updated": "10/22/2026"}))
    respx.post(f"{BASE}/api/v2/download/count/").mock(return_value=httpx.Response(200, json={**SYNTHETIC_COUNT, "calculated_transaction_count": count}))
    respx.post(f"{BASE}/api/v2/download/transactions/").mock(return_value=httpx.Response(200, json={"file_name": "job1.zip", "file_url": "https://files.example/job1.zip", "status_url": "..."}))
    respx.get(f"{BASE}/api/v2/download/status/").mock(return_value=httpx.Response(200, json={"status": "finished", "file_url": "https://files.example/job1.zip", "total_rows": rows_in_zip}))
    return respx.get("https://files.example/job1.zip").mock(return_value=httpx.Response(200, content=_zip_bytes(rows_in_zip)))


@respx.mock
def test_pull_cell_writes_manifest_with_provenance_and_matching_counts(tmp_path: Path):
    _mock_download(3)
    m = pull_cell(client(), tmp_path, "036", "Department of Veterans Affairs", 2025, poll_seconds=0)
    d = tmp_path / "agency=036" / "fy=2025"
    assert m["status"] == "complete" and m["rows_total"] == 3 and m["count_matches"] is True
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
    respx.post(f"{BASE}/api/v2/download/count/").mock(return_value=httpx.Response(200, json={**SYNTHETIC_COUNT, "calculated_transaction_count": 4}))
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
    respx.post(f"{BASE}/api/v2/download/count/").mock(return_value=httpx.Response(200, json={**SYNTHETIC_COUNT, "transaction_rows_gt_limit": True}))
    with pytest.raises(ApiError) as ei:
        pull_cell(client(), tmp_path, "036", "VA", 2025, poll_seconds=0)
    assert "split the cell" in str(ei.value)


@respx.mock
def test_failed_download_leaves_previous_files_untouched(tmp_path: Path):
    _mock_download(3)
    pull_cell(client(), tmp_path, "036", "VA", 2025, poll_seconds=0)
    d = tmp_path / "agency=036" / "fy=2025"
    before = (d / "manifest.json").read_text()
    respx.post(f"{BASE}/api/v2/download/count/").mock(return_value=httpx.Response(200, json={**SYNTHETIC_COUNT, "calculated_transaction_count": 9}))
    respx.get(f"{BASE}/api/v2/download/status/").mock(return_value=httpx.Response(200, json={"status": "failed", "message": "boom"}))
    with pytest.raises(ApiError):
        pull_cell(client(), tmp_path, "036", "VA", 2025, poll_seconds=0)
    assert (d / "manifest.json").read_text() == before and (d / "Contracts_PrimeTransactions_1.csv").exists()
