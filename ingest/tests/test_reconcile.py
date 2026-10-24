"""The reconciliation gate (R1 counts, R2 award sums, R3 agency-year dollars vs spending_over_time) on the real report shape.
R3 became a gate on 2026-10-24 once its grain was confirmed (docs/DECISIONS.md)."""
import copy
import json
from pathlib import Path

from civiclens_ingest.reconcile import summarize

REAL = Path(__file__).resolve().parents[2] / "evidence" / "reconcile" / "report.json"


def _report():
    if REAL.exists():                       # the committed report from ingest run 39997561946
        return json.loads(REAL.read_text())
    return {"R1": [{"agency_code": "020", "fiscal_year": 2023, "ours": 3308, "api_count_now": 3309, "delta": -1},
                   {"agency_code": "036", "fiscal_year": 2023, "ours": 100, "api_count_now": 100, "delta": 0}],
            "R2": [], "R3": [{"agency_code": "020", "fiscal_year": 2023, "ours": 2243192310.47, "api_spending_over_time": 2243255482.39, "delta": -63171.92, "available": True},
                             {"agency_code": "036", "fiscal_year": 2023, "ours": 6198741321.22, "api_spending_over_time": 6198741321.22, "delta": 0.0, "available": True}]}


def test_committed_report_passes_with_r3_as_a_gate():
    r = _report(); sm = summarize(r, 0)
    assert sm["pass"] and sm["r3_over_tolerance_cells"] == 0 and sm["r3_coupled_exact_violations"] == 0
    # every non-zero R3 delta sits on a cell whose row count was short — the dollars differ because rows are missing, not because amounts changed
    assert all(x["row_count_short"] for x in r["R3"] if x.get("available") and abs(x["delta"]) >= 0.005)


def test_dollar_difference_on_an_exact_cell_fails_even_inside_tolerance():
    r = _report()
    exact = next(x for x in r["R1"] if x["delta"] == 0)
    cell = next(x for x in r["R3"] if x.get("available") and (x["agency_code"], x["fiscal_year"]) == (exact["agency_code"], exact["fiscal_year"]))
    cell["delta"] = 12.34; cell["api_spending_over_time"] = cell["ours"] - 12.34          # 0.000000002% — inside any tolerance
    sm = summarize(r, 0)
    assert not sm["pass"] and sm["r3_coupled_exact_violations"] == 1 and sm["r3_over_tolerance_cells"] == 0


def test_r3_beyond_tolerance_fails_and_r2_mismatch_fails():
    r = _report()
    short = next(x for x in r["R3"] if x.get("available") and abs(x["delta"]) >= 0.005)
    short["api_spending_over_time"] = short["ours"] * 1.01; short["delta"] = short["ours"] - short["api_spending_over_time"]
    assert not summarize(copy.deepcopy(r), 0)["pass"]
    assert not summarize(_report(), 1)["pass"]
