from __future__ import annotations

import duckdb


def test_healthz_and_meta_expose_snapshot_version_and_dq(client):
    h = client.get("/healthz").json()
    assert h["ok"] and h["dq_all_pass"] is True and h["snapshot_version"]
    m = client.get("/v1/meta").json()
    assert m["settled_fiscal_years"] == [2022, 2023, 2024, 2025] and m["preliminary_fiscal_years"] == [2026]
    assert "036" in m["agencies"] and m["dq"]["_all_pass"]


def test_overview_totals_equal_silver_sum(client, snapshot_path):
    o = client.get("/v1/overview").json()
    api_total = sum(r["obligations"] for r in o["by_fiscal_year"])
    con = duckdb.connect(str(snapshot_path), read_only=True)
    silver = con.execute("SELECT SUM(obligation) FROM silver_contract_transactions").fetchone()[0]
    assert abs(float(api_total) - float(silver)) < 0.005
    assert abs(sum(r["obligations"] for r in o["by_agency"]) - float(silver)) < 0.005


def test_scope_filters_apply_consistently_across_sections(client):
    o = client.get("/v1/overview", params={"agency": "036", "fy": 2025}).json()
    assert all(r["fiscal_year"] == 2025 for r in o["by_fiscal_year"])
    a = client.get("/v1/agency", params={"agency": "036", "fy": 2025}).json()
    assert all(r["fiscal_year"] == 2025 and r["awarding_agency_code"] == "036" for r in a["agency_fy"])


def test_invalid_scope_is_rejected_not_widened(client):
    assert client.get("/v1/overview", params={"agency": "999"}).status_code == 422
    assert client.get("/v1/overview", params={"fy": 1999}).status_code == 422
    assert client.get("/v1/overview", params={"psc": "D3; DROP TABLE x"}).status_code == 422
    assert client.get("/v1/search", params={"query": "x"}).status_code == 422


def test_anomaly_list_and_detail_carry_explanation_fields(client):
    items = client.get("/v1/anomalies", params={"detector": "large_award", "fy": 2025}).json()["items"]
    assert items and items[0]["award_key"] == "AWD-OUTLIER"
    for k in ("peer_n", "baseline_median", "score", "threshold", "status", "limits", "usaspending_permalink"):
        assert k in items[0], k
    d = client.get(f"/v1/anomalies/{items[0]['award_key']}/2025").json()
    assert d["transactions"] and d["peer_group_sample"] and d["award_years"]
    assert "not a finding of wrongdoing" in d["limits"]
    assert client.get("/v1/anomalies/NOPE/2025").status_code == 404


def test_other_detectors_and_search(client):
    c = client.get("/v1/anomalies", params={"detector": "concentration", "fy": 2026}).json()["items"]
    assert c and c[0]["top_recipient_name"] == "GAMMA INC"
    g = client.get("/v1/anomalies", params={"detector": "recipient_growth"}).json()["items"]
    assert any(r["recipient_name"] == "GAMMA INC" for r in g)
    s = client.get("/v1/search", params={"query": "giant"}).json()["items"]
    assert s and s[0]["recipient_name"] == "GIANT CORP"


def test_sql_catalogue_is_published_and_no_endpoint_accepts_sql(client):
    cat = client.get("/v1/sql").json()
    assert "anomalies_large" in cat["queries"] and cat["row_cap"] == 2000
    paths = [r.path for r in client.app.routes]
    assert not any("sql" in p and p != "/v1/sql" for p in paths)


def test_response_headers_carry_snapshot_version_and_timing(client):
    r = client.get("/v1/meta")
    assert r.headers["X-Snapshot-Version"] and int(r.headers["X-Response-Time-ms"]) >= 0
