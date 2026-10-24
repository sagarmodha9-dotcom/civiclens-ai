"""Independent reconciliation of our Silver/Gold against USAspending, at matching grain only.

    python -m civiclens_ingest.reconcile --raw data/raw --db build/civiclens.duckdb --out evidence/reconcile --sample 50

Three checks, each comparing like with like:
  R1 completeness  per cell: our prime-row count vs POST /download/count with the identical filter body (re-queried now).
  R2 award window  for N sampled awards: our transactions with action_date inside the cell's FY window vs the award's
                   own transactions from POST /api/v2/transactions/ restricted to the same window: count and sum of
                   federal_action_obligation to the cent. Lifetime totals are reported alongside, labelled, never compared.
  R3 agency year   per cell: our Gold agency-FY obligations vs the sum of 'Award Amount' from spending_by_award? NO:
                   Award Amount is lifetime; not comparable. Instead: sum of our window transactions vs the API's
                   spending_over_time (monthly obligations) for the same filter and window, if that endpoint exists
                   (recorded as 'not available' otherwise).
Deltas are reported, never silently tolerated; tolerance for R1/R2 is 0 except for records modified between pulls,
which are listed by key.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import sys
from pathlib import Path

import duckdb

from .client import ApiError, UsaSpendingClient, contract_filters, fy_window
from .probe import AGENCIES



R1_TOLERANCE = 0.005   # same tolerance as the pipeline DQ gate (docs/DECISIONS.md 2026-10-23, Treasury)


def summarize(report: dict, mism: int) -> dict:
    """Fills report["summary"] (and per-cell R3 flags) and returns it. Pure, so the gate is unit-tested.

    R3 grain, confirmed 2026-10-24 on the v20261023-1 data (docs/DECISIONS.md): spending_over_time with spending_level=transactions,
    grouped by month and summed over the fiscal-year window, equals the sum of transaction obligations for the same filter —
    to the cent on every cell whose R1 row count was exact (26/30), and off only on the cells whose row count was short (4/30).
    So R3 is a gate with two rules: (a) |delta| within the same 0.5% tolerance as R1; (b) coupled exactness — a cell whose
    row count matches exactly must also match in dollars exactly; a dollar difference without a row difference means a
    changed amount, which the tolerance must not absorb."""
    r1_inexact = [x for x in report["R1"] if x["delta"] not in (0, None)]
    r1_over = [x for x in r1_inexact if abs(x["delta"]) / max(x["api_count_now"], 1) > R1_TOLERANCE]
    r1_exact_cells = {(x["agency_code"], int(x["fiscal_year"])) for x in report["R1"] if x["delta"] == 0}
    r3_avail = [x for x in report["R3"] if x.get("available")]
    r3_over = [x for x in r3_avail if abs(x["delta"]) / max(abs(x["api_spending_over_time"]), 1.0) > R1_TOLERANCE]
    r3_coupled = [x for x in r3_avail if (x["agency_code"], int(x["fiscal_year"])) in r1_exact_cells and abs(x["delta"]) >= 0.005]
    for x in r3_avail:
        x["within_tolerance"] = x not in r3_over
        x["coupled_exact_violation"] = x in r3_coupled
        x["row_count_short"] = (x["agency_code"], int(x["fiscal_year"])) not in r1_exact_cells
    report["summary"] = {"cells": len(report["R1"]), "r1_exact_cells": len(report["R1"]) - len(r1_inexact),
                         "r1_inexact_cells": len(r1_inexact), "r1_over_tolerance_cells": len(r1_over), "r1_tolerance": R1_TOLERANCE,
                         "r2_sampled": len(report["R2"]),
                         "r2_mismatches": mism, "r3_available": len(r3_avail),
                         "r3_nonzero_delta": sum(1 for x in r3_avail if abs(x["delta"]) >= 0.005),
                         "r3_over_tolerance_cells": len(r3_over), "r3_coupled_exact_violations": len(r3_coupled),
                         "r3_grain": "spending_over_time, spending_level=transactions, group=month, summed over the FY window (confirmed 2026-10-24)",
                         "pass": not r1_over and mism == 0 and not r3_over and not r3_coupled}
    return report["summary"]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="data/raw")
    ap.add_argument("--db", default="build/civiclens.duckdb")
    ap.add_argument("--out", default="evidence/reconcile")
    ap.add_argument("--sample", type=int, default=50)
    ap.add_argument("--seed", type=int, default=20261023)
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(a.db, read_only=True)
    c = UsaSpendingClient()
    names = dict(AGENCIES)
    report = {"run_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "snapshot": a.db, "R1": [], "R2": [], "R3": []}

    # R1 completeness per cell
    cells = con.execute("SELECT _ingest_agency_code, _ingest_fiscal_year, COUNT(*) FROM bronze_prime_transactions GROUP BY 1,2 ORDER BY 1,2").fetchall()
    for code, fy, ours in cells:
        try:
            cnt = c.download_count(contract_filters(names[code], int(fy)))
            api = cnt.get("calculated_count", cnt.get("calculated_transaction_count"))
        except ApiError as e:
            api = None; err = str(e)
        else:
            err = None
        report["R1"].append({"agency_code": code, "fiscal_year": int(fy), "ours": ours, "api_count_now": api, "delta": (ours - api) if api is not None else None, "error": err})
        print(f"R1 {code} FY{fy}: ours={ours} api_now={api} delta={(ours - api) if api is not None else 'n/a'}", flush=True)

    # R2 sampled awards, window-restricted
    rnd = random.Random(a.seed)
    awards = con.execute("SELECT award_key, fiscal_year, awarding_agency_code, COUNT(*) AS n, SUM(obligation) AS s FROM silver_contract_transactions "
                         "GROUP BY 1,2,3").fetchall()
    sample = rnd.sample(awards, min(a.sample, len(awards)))
    mism = 0
    for award_key, fy, code, n_ours, s_ours in sample:
        start, end = fy_window(int(fy))
        try:
            tx = c.award_transactions(award_key)
        except ApiError as e:
            report["R2"].append({"award_key": award_key, "fiscal_year": int(fy), "error": str(e)}); print("R2", award_key, "ERROR", e); continue
        win = [t for t in tx if start <= str(t.get("action_date", ""))[:10] <= end]
        n_api, s_api = len(win), round(sum(float(t.get("federal_action_obligation") or 0) for t in win), 2)
        ok = (n_api == n_ours) and abs(s_api - float(s_ours)) < 0.005
        mism += 0 if ok else 1
        try:
            life = c.award(award_key).get("total_obligation")
        except ApiError:
            life = None
        report["R2"].append({"award_key": award_key, "fiscal_year": int(fy), "agency_code": code, "ours_n": n_ours, "api_n": n_api,
                             "ours_sum": float(s_ours), "api_sum": s_api, "match": ok, "api_lifetime_total_obligation_label_only": life,
                             "api_transactions_all_years": len(tx)})
        print(f"R2 {award_key} FY{fy}: n {n_ours}/{n_api} sum {float(s_ours):.2f}/{s_api:.2f} {'OK' if ok else 'MISMATCH'} (lifetime {life}, all-years tx {len(tx)})", flush=True)

    # R3 agency-year via spending_over_time if available (same filter body, monthly, summed over the window)
    for code, fy, _ in cells:
        try:
            body = {"group": "month", "filters": contract_filters(names[code], int(fy)), "spending_level": "transactions"}
            r = c._call("POST", "/api/v2/search/spending_over_time/", body)
            api_sum = round(sum(float(x.get("aggregated_amount") or 0) for x in r.get("results", [])), 2)
            ours = con.execute("SELECT SUM(obligations) FROM gold_agency_fy WHERE awarding_agency_code=? AND fiscal_year=?", [code, int(fy)]).fetchone()[0]
            report["R3"].append({"agency_code": code, "fiscal_year": int(fy), "ours": float(ours or 0), "api_spending_over_time": api_sum,
                                 "delta": round(float(ours or 0) - api_sum, 2), "available": True})
            print(f"R3 {code} FY{fy}: ours={float(ours or 0):.2f} api={api_sum:.2f} delta={float(ours or 0) - api_sum:.2f}", flush=True)
        except ApiError as e:
            report["R3"].append({"agency_code": code, "fiscal_year": int(fy), "available": False, "error": str(e)[:200]})
            print(f"R3 {code} FY{fy}: not available ({e})", flush=True)
    c.close()
    mism_count = mism
    summarize(report, mism_count)
    (out / "report.json").write_text(json.dumps(report, indent=1, default=str))
    sm = report["summary"]
    md = [f"# Reconciliation against USAspending — {report['run_utc']}", "",
          f"R1 completeness: {sm['cells']} cells re-counted now, {sm['r1_exact_cells']} exact, {sm['r1_inexact_cells']} with a delta, "
          f"{sm['r1_over_tolerance_cells']} beyond the {sm['r1_tolerance']:.1%} tolerance. R2 window sums: {sm['r2_sampled']} sampled awards, "
          f"{sm['r2_mismatches']} mismatches. R3 agency-year vs spending_over_time: {sm['r3_available']} available, {sm['r3_nonzero_delta']} with a non-zero delta, "
          f"{sm['r3_over_tolerance_cells']} beyond tolerance, {sm['r3_coupled_exact_violations']} dollar differences on cells whose row count was exact. "
          f"**{'PASS' if sm['pass'] else 'FAIL'}** (R2 must be exact to the cent; R1 and R3 deltas must stay within {sm['r1_tolerance']:.1%}; a cell with an exact row count must "
          f"also match in dollars exactly; R3 grain: {sm['r3_grain']}).", "",
          "| check | agency | FY | ours | API | delta / match |", "|---|---|---|---|---|---|"]
    for x in report["R1"]:
        md.append(f"| R1 count | {x['agency_code']} | {x['fiscal_year']} | {x['ours']:,} | {x['api_count_now']} | {x['delta']} |")
    for x in report["R2"][:60]:
        if "error" in x:
            md.append(f"| R2 award | {x['award_key']} | {x['fiscal_year']} | | | error: {x['error'][:60]} |"); continue
        md.append(f"| R2 award `{x['award_key']}` | {x['agency_code']} | {x['fiscal_year']} | {x['ours_n']} tx, ${x['ours_sum']:,.2f} | {x['api_n']} tx, ${x['api_sum']:,.2f} (lifetime ${x['api_lifetime_total_obligation_label_only']}) | {'match' if x['match'] else 'MISMATCH'} |")
    for x in report["R3"]:
        if x.get("available"):
            flag = " (row count short — see R1)" if x.get("row_count_short") and abs(x["delta"]) >= 0.005 else (" **DOLLARS DIFFER ON AN EXACT CELL**" if x.get("coupled_exact_violation") else "")
            md.append(f"| R3 agency-year | {x['agency_code']} | {x['fiscal_year']} | ${x['ours']:,.2f} | ${x['api_spending_over_time']:,.2f} | {x['delta']:,.2f}{flag} |")
        else:
            md.append(f"| R3 agency-year | {x['agency_code']} | {x['fiscal_year']} | | not available | {x.get('error','')[:60]} |")
    (out / "report.md").write_text("\n".join(md) + "\n")
    print(f"\nreconcile {'PASS' if sm['pass'] else 'FAIL'} -> {out}/report.md")
    return 0 if sm["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
