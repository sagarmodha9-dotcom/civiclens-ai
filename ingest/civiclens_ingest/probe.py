"""Live validation of every USAspending endpoint CivicLens depends on. Read-only, no downloads of full files.

    python -m civiclens_ingest.probe --out evidence/probe

Writes one JSON per endpoint with: the exact request sent, HTTP status, top-level response keys, the first
result's keys, pagination metadata, identifiers seen, and counts; plus `summary.json` and `summary.md`.
Nothing downstream may rely on a field that does not appear in these files. Runs on GitHub Actions or a laptop;
the development sandbox cannot reach the API, which is itself recorded as a finding.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from .client import ApiError, UsaSpendingClient, contract_filters, fy_window

AGENCIES = [  # awarding toptier names exactly as USAspending spells them; the probe verifies each resolves
    ("036", "Department of Veterans Affairs"),
    ("070", "Department of Homeland Security"),
    ("075", "Department of Health and Human Services"),
    ("020", "Department of the Treasury"),
    ("013", "Department of Commerce"),
    ("028", "Social Security Administration"),
]
FYS = [2022, 2023, 2024, 2025, 2026]
AWARD_FIELDS = ["Award ID", "Recipient Name", "Recipient UEI", "Award Amount", "Total Outlays", "Description",
                "Start Date", "End Date", "Awarding Agency", "Awarding Sub Agency", "Contract Award Type",
                "NAICS", "PSC", "Last Modified Date", "generated_internal_id", "recipient_id"]


def keys_of(x) -> list[str]:
    return sorted(x.keys()) if isinstance(x, dict) else [f"<{type(x).__name__}>"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="evidence/probe")
    ap.add_argument("--quick", action="store_true", help="one agency, one FY")
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    c = UsaSpendingClient()
    findings: dict = {"run_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "ok": True,
                      "endpoints": {}, "counts": {}, "notes": []}

    def record(name: str, payload: dict):
        (out / f"{name}.json").write_text(json.dumps(payload, indent=1, default=str))
        findings["endpoints"][name] = {k: payload.get(k) for k in ("status", "response_keys", "first_result_keys",
                                                                  "page_metadata", "error") if k in payload}

    def step(name: str, fn):
        try:
            payload = fn()
            payload.setdefault("status", "ok")
            record(name, payload)
            print(f"  [ok  ] {name}: {payload.get('summary', '')}")
        except ApiError as e:
            findings["ok"] = False
            record(name, {"status": "error", "error": str(e), "url": e.url})
            print(f"  [FAIL] {name}: {e}")
        except Exception as e:  # noqa: BLE001  keep probing other endpoints
            findings["ok"] = False
            record(name, {"status": "error", "error": f"{type(e).__name__}: {e}"})
            print(f"  [FAIL] {name}: {type(e).__name__}: {e}")

    agencies = AGENCIES[:1] if args.quick else AGENCIES
    fys = FYS[-2:-1] if args.quick else FYS

    # 1 liveness + freshness
    def p_last_updated():
        v = c.last_updated(); findings["last_updated"] = v
        return {"response": {"last_updated": v}, "summary": f"last_updated={v}"}
    step("last_updated", p_last_updated)

    # 2 agency names resolve
    def p_agencies():
        rows = c.toptier_agencies()
        by_name = {r.get("agency_name"): r for r in rows}
        resolved = {name: by_name.get(name, {}).get("toptier_code") for _, name in agencies}
        missing = [n for n, code in resolved.items() if code is None]
        if missing:
            raise ApiError(0, f"agency names not found in toptier list: {missing}")
        return {"response_keys": keys_of(rows[0]) if rows else [], "resolved": resolved,
                "summary": f"{len(rows)} toptier agencies; all {len(resolved)} MVP names resolve"}
    step("toptier_agencies", p_agencies)

    # 3 counts per agency x FY with the exact production filter body
    def p_counts():
        table = {}
        for code, name in agencies:
            for fy in fys:
                f = contract_filters(name, fy)
                r = c.download_count(f)
                table[f"{code}:{fy}"] = {"agency": name, "fy": fy, "window": fy_window(fy), "response": r}
        first = next(iter(table.values()))["response"]
        findings["counts"] = {k: v["response"] for k, v in table.items()}
        total = sum((v["response"].get("calculated_transaction_count") or 0) for v in table.values())
        return {"request_example": {"filters": contract_filters(agencies[0][1], fys[0])}, "response_keys": keys_of(first),
                "table": table, "summary": f"{len(table)} cells, {total:,} transactions in scope (per API count)"}
    step("download_count", p_counts)

    # 4 search page: fields, pagination metadata, identifiers
    def p_search():
        f = contract_filters(agencies[0][1], fys[0])
        d = c.spending_by_award_page(f, AWARD_FIELDS, page=1, limit=5)
        res = d.get("results", [])
        d2 = c.spending_by_award_page(f, AWARD_FIELDS, page=2, limit=5,
                                      last_record_unique_id=d.get("page_metadata", {}).get("last_record_unique_id"),
                                      last_record_sort_value=d.get("page_metadata", {}).get("last_record_sort_value"))
        ids1 = {r.get("generated_internal_id") for r in res}
        ids2 = {r.get("generated_internal_id") for r in d2.get("results", [])}
        return {"request": {"filters": f, "fields": AWARD_FIELDS, "page": 1, "limit": 5},
                "response_keys": keys_of(d), "page_metadata": d.get("page_metadata"),
                "first_result_keys": keys_of(res[0]) if res else [],
                "first_result_redacted": {k: (v if k != "Description" else str(v)[:60]) for k, v in (res[0] if res else {}).items()},
                "page2_disjoint": ids1.isdisjoint(ids2), "sample_ids": sorted(x for x in ids1 if x)[:5],
                "summary": f"{len(res)} rows p1, {len(ids2)} rows p2, disjoint={ids1.isdisjoint(ids2)}, hasNext={d.get('page_metadata', {}).get('hasNext')}"}
    step("spending_by_award", p_search)

    def p_search_count():
        f = contract_filters(agencies[0][1], fys[0])
        d = c.spending_by_award_count(f)
        return {"request": {"filters": f}, "response": d, "response_keys": keys_of(d),
                "summary": f"award counts by type: {d.get('results')}"}
    step("spending_by_award_count", p_search_count)

    # 5 award detail + its transactions (the reconciliation grain)
    def p_award():
        f = contract_filters(agencies[0][1], fys[0])
        d = c.spending_by_award_page(f, AWARD_FIELDS, page=1, limit=1)
        res = d.get("results", [])
        if not res:
            raise ApiError(0, "no award to probe")
        gid = res[0]["generated_internal_id"]
        a = c.award(gid)
        tx = c.award_transactions(gid)
        start, end = fy_window(fys[0])
        in_window = [t for t in tx if start <= str(t.get("action_date", ""))[:10] <= end]
        s = round(sum(float(t.get("federal_action_obligation") or 0) for t in in_window), 2)
        return {"generated_unique_award_id": gid, "award_keys": keys_of(a),
                "award_total_obligation": a.get("total_obligation"), "award_date_signed": a.get("date_signed"),
                "transaction_keys": keys_of(tx[0]) if tx else [], "transactions_total": len(tx),
                "transactions_in_window": len(in_window), "window_obligation_sum": s,
                "lifetime_vs_window_equal": abs(float(a.get("total_obligation") or 0) - s) < 0.005,
                "summary": f"award {gid}: {len(tx)} transactions, {len(in_window)} in FY{fys[0]} window, window sum {s}, lifetime {a.get('total_obligation')}"}
    step("award_and_transactions", p_award)

    # 6 download job: submit for the smallest cell, poll until finished, DO NOT fetch the file; record shape
    def p_download():
        smallest = min(((k, v) for k, v in findings["counts"].items()), key=lambda kv: kv[1].get("calculated_transaction_count") or 10**12)
        code, fy = smallest[0].split(":")
        name = dict(agencies)[code]
        f = contract_filters(name, int(fy))
        sub = c.request_transaction_download(f)
        st = c.wait_for_download(sub["file_name"], poll_seconds=15, max_wait_seconds=900)
        return {"request": {"filters": f, "file_format": "csv"}, "submit_response_keys": keys_of(sub),
                "submit_response": {k: v for k, v in sub.items() if k != "download_request"},
                "status_response_keys": keys_of(st), "status_response": st,
                "summary": f"{code} FY{fy}: status={st.get('status')} total_rows={st.get('total_rows')} size={st.get('total_size')} seconds_elapsed={st.get('seconds_elapsed')}"}
    step("download_transactions", p_download)

    findings["calls"] = c.records_json()
    (out / "summary.json").write_text(json.dumps(findings, indent=1, default=str))
    md = [f"# USAspending probe — {findings['run_utc']}", "", f"API last_updated: **{findings.get('last_updated')}**", "",
          "| endpoint | status | note |", "|---|---|---|"]
    for name, e in findings["endpoints"].items():
        md.append(f"| `{name}` | {e.get('status')} | {str(e.get('error') or '')[:120]} |")
    if findings["counts"]:
        md += ["", "## Transactions in scope per agency × FY (API `download/count`)", "", "| agency | FY | count | over limit? |", "|---|---|---|---|"]
        for k, v in findings["counts"].items():
            code, fy = k.split(":")
            md.append(f"| {dict(agencies).get(code, code)} | {fy} | {v.get('calculated_transaction_count'):,} | {v.get('transaction_rows_gt_limit')} |")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    print(f"\nprobe {'OK' if findings['ok'] else 'HAD FAILURES'} -> {out}/summary.md")
    c.close()
    return 0 if findings["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
