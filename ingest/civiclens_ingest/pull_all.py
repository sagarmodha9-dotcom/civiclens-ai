"""Pull every MVP cell (6 agencies x FY2022-FY2026) and write an ingestion report.

    python -m civiclens_ingest.pull_all --out data/raw --report evidence/ingest

Sequential, one download job at a time (the API runs them asynchronously; we do not queue several). Each cell is
idempotent via the worker. The report holds every manifest minus the bulky `calls`, plus totals and a list of
cells whose prime-row count did not equal the API count. Raw data stays out of git.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from .client import ApiError, UsaSpendingClient
from .probe import AGENCIES, FYS
from .worker import pull_cell


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/raw")
    ap.add_argument("--report", default="evidence/ingest")
    ap.add_argument("--only", default="", help="comma list of agency codes to restrict to")
    ap.add_argument("--fys", default="", help="comma list of fiscal years to restrict to")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    codes = set(a.only.split(",")) if a.only else None
    fys = [int(x) for x in a.fys.split(",")] if a.fys else FYS
    rep = Path(a.report); rep.mkdir(parents=True, exist_ok=True)
    c = UsaSpendingClient()
    results, failures = [], []
    for code, name in AGENCIES:
        if codes and code not in codes:
            continue
        for fy in fys:
            try:
                m = pull_cell(c, Path(a.out), code, name, fy, force=a.force, poll_seconds=10)
                slim = {k: v for k, v in m.items() if k not in ("calls", "api_count_response")}
                results.append(slim)
                print(f"  {code} FY{fy}: {m.get('status')}{' (skipped, unchanged)' if m.get('skipped') else ''} "
                      f"prime={m.get('rows_total')} api={m.get('api_count')} sub={m.get('rows_subawards')}", flush=True)
            except ApiError as e:
                failures.append({"agency_code": code, "fiscal_year": fy, "error": str(e)})
                print(f"  {code} FY{fy}: FAILED {e}", flush=True)
    c.close()
    total = sum(r.get("rows_total") or 0 for r in results)
    mism = [r for r in results if r.get("count_matches") is False]
    report = {"run_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "cells": results,
              "failures": failures, "totals": {"cells_ok": len(results), "cells_failed": len(failures),
              "prime_transactions": total, "count_mismatches": len(mism)}}
    (rep / "report.json").write_text(json.dumps(report, indent=1, default=str))
    md = [f"# Ingestion report — {report['run_utc']}", "",
          f"Cells complete: **{len(results)}**, failed: **{len(failures)}**, prime transactions: **{total:,}**, "
          f"count mismatches: **{len(mism)}**", "",
          "| agency | FY | status | prime rows | API count | match | sub-award rows | extracted | API last_updated |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        md.append(f"| {r['agency_name']} | {r['fiscal_year']} | {r['status']} | {r.get('rows_total'):,} | {r.get('api_count'):,} | "
                  f"{r.get('count_matches')} | {r.get('rows_subawards')} | {r.get('extracted_utc')} | {r.get('api_last_updated')} |")
    for f in failures:
        md.append(f"| {f['agency_code']} | {f['fiscal_year']} | FAILED | | | | | | {f['error'][:80]} |")
    (rep / "report.md").write_text("\n".join(md) + "\n")
    print(f"\n{len(results)} ok, {len(failures)} failed, {total:,} prime transactions, {len(mism)} mismatches -> {rep}/report.md")
    return 1 if failures or mism else 0


if __name__ == "__main__":
    sys.exit(main())
