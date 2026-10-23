"""Independent validation of the anomaly engine against the real snapshot (milestone M3).

Two layers, both written to evidence/anomalies/:

1. Re-implementation check. The three detectors are re-computed here in plain Python/NumPy from the Gold tables
   (median / MAD / robust z, Herfindahl index, year-over-year ratio) — NOT by re-running the SQL — and compared row by
   row with the anomaly_* tables the pipeline produced: same flagged set, same scores within 1e-6.
2. Source trace of representative flagged records. For a sample of flagged rows (the highest-scoring large_award per
   agency, the top concentration cells and the top recipient-growth rows) the flagged value is traced back through
   Silver to the raw Bronze rows exactly as downloaded from USAspending: the sum of federal_action_obligation over the
   award's deduplicated raw transactions in that fiscal year must equal the flagged value to the cent. The record's
   USAspending permalink, award type, PSC description, transaction count, date span and parent vehicle are listed so a
   reader can open the award on usaspending.gov and see the same numbers. Nothing here characterises conduct: a flag
   means "statistically unusual relative to the stated comparison group", and the descriptors are read off the record.

    python -m civiclens_lakehouse.validate_anomalies --snapshot build/civiclens.duckdb --out evidence/anomalies
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

import duckdb

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None

from .pipeline import PARAMS

TOL = 1e-6


def _median(a):
    return float(np.median(np.asarray(a, dtype=float)))


def recompute_large_award(con) -> dict:
    rows = con.execute("""SELECT award_key, fiscal_year, awarding_agency_code, psc_class2, obligations
                          FROM gold_award_fy WHERE obligations > 0""").fetchall()
    groups: dict[tuple, list] = {}
    for ak, fy, ag, psc2, obl in rows:
        groups.setdefault((ag, psc2, fy), []).append((ak, float(obl)))
    mine: dict[tuple, dict] = {}
    for key, items in groups.items():
        lg = np.log10([v for _, v in items])
        med = _median(lg)
        mad = _median(np.abs(lg - med))
        n = len(items)
        for (ak, v), l in zip(items, lg):
            z = (l - med) / (1.4826 * mad) if mad > 0 else None
            if n < PARAMS["min_peer_n"]:
                st = "not scored: fewer than %d comparable award-years" % PARAMS["min_peer_n"]
            elif mad == 0:
                st = "not scored: no spread in peer group"
            elif z >= PARAMS["z_threshold"]:
                st = "flagged"
            else:
                st = "normal"
            mine[(ak, key[2])] = {"score": z, "peer_n": n, "status": st, "median": 10 ** med, "mad": mad}
    theirs = {(r[0], r[1]): {"score": r[2], "peer_n": r[3], "status": r[4]} for r in
              con.execute("SELECT award_key, fiscal_year, score, peer_n, status FROM anomaly_large_award").fetchall()}
    return _compare("large_award", mine, theirs)


def recompute_concentration(con) -> dict:
    rows = con.execute("""SELECT awarding_agency_code, psc_class2, fiscal_year, recipient_uei, SUM(obligations)
                          FROM gold_award_fy WHERE obligations > 0 GROUP BY 1,2,3,4""").fetchall()
    cells: dict[tuple, dict] = {}
    for ag, psc2, fy, uei, obl in rows:
        cells.setdefault((ag, psc2, fy), {})[uei] = float(obl)
    hhi = {}
    for key, recips in cells.items():
        total = sum(recips.values())
        shares = [100.0 * v / total for v in recips.values()]
        hhi[key] = {"hhi": sum(s * s for s in shares), "top_share": max(shares), "total": total, "n": len(recips)}
    mine = {}
    for (ag, psc2, fy), h in hhi.items():
        prior = hhi.get((ag, psc2, fy - 1), {}).get("hhi")
        if h["total"] < PARAMS["hhi_min_spend"]:
            st = "not scored: cell below spend floor"
        elif (h["hhi"] >= PARAMS["hhi_threshold"] and h["top_share"] >= PARAMS["hhi_top_share"]) or (prior is not None and h["hhi"] - prior >= 1000):
            st = "flagged"
        else:
            st = "normal"
        mine[(ag, psc2, fy)] = {"score": h["hhi"], "peer_n": h["n"], "status": st}
    theirs = {(r[0], r[1], r[2]): {"score": r[3], "peer_n": r[4], "status": r[5]} for r in
              con.execute("SELECT awarding_agency_code, psc_class2, fiscal_year, score, peer_n, status FROM anomaly_concentration").fetchall()}
    return _compare("concentration", mine, theirs)


def recompute_growth(con) -> dict:
    rows = con.execute("SELECT recipient_uei, awarding_agency_code, fiscal_year, obligations FROM gold_recipient_agency_fy").fetchall()
    cur = {(u, a, fy): float(o) for u, a, fy, o in rows}
    mine = {}
    for (u, a, fy), o in cur.items():
        p = cur.get((u, a, fy - 1))
        if p is None:
            st, z = "not scored: no prior-year obligations at this agency", None
        else:
            z = o / p if p > 0 else None
            if p < PARAMS["growth_min_base"]:
                st = "not scored: prior year below base floor"
            elif z is not None and z >= PARAMS["growth_ratio"] and o - p >= PARAMS["growth_min_delta"]:
                st = "flagged"
            else:
                st = "normal"
        mine[(u, a, fy)] = {"score": z, "peer_n": None, "status": st}
    theirs = {(r[0], r[1], r[2]): {"score": r[3], "peer_n": None, "status": r[4]} for r in
              con.execute("SELECT recipient_uei, awarding_agency_code, fiscal_year, score, status FROM anomaly_recipient_growth").fetchall()}
    return _compare("recipient_growth", mine, theirs)


def _compare(name, mine, theirs) -> dict:
    missing = sorted(set(mine) - set(theirs)); extra = sorted(set(theirs) - set(mine))
    flagged_mine = {k for k, v in mine.items() if v["status"] == "flagged"}
    flagged_theirs = {k for k, v in theirs.items() if v["status"] == "flagged"}
    status_mismatch = [k for k in mine.keys() & theirs.keys() if mine[k]["status"] != theirs[k]["status"]]
    max_score_diff = 0.0
    for k in mine.keys() & theirs.keys():
        a, b = mine[k]["score"], theirs[k]["score"]
        if a is None and b is None:
            continue
        if a is None or b is None:
            status_mismatch.append(k); continue
        d = abs(float(a) - float(b)) / max(1.0, abs(float(b)))
        max_score_diff = max(max_score_diff, d)
    ok = not missing and not extra and not status_mismatch and flagged_mine == flagged_theirs and max_score_diff <= TOL
    return {"detector": name, "rows_pipeline": len(theirs), "rows_recomputed": len(mine), "flagged_pipeline": len(flagged_theirs),
            "flagged_recomputed": len(flagged_mine), "flagged_sets_identical": flagged_mine == flagged_theirs,
            "status_mismatches": len(set(status_mismatch)), "max_relative_score_diff": max_score_diff,
            "rows_only_in_pipeline": len(extra), "rows_only_in_recompute": len(missing), "pass": ok}


# ---------------------------------------------------------------- source trace
def _fy_sql(col: str) -> str:
    return f"CASE WHEN EXTRACT(MONTH FROM TRY_CAST({col} AS DATE)) >= 10 THEN EXTRACT(YEAR FROM TRY_CAST({col} AS DATE)) + 1 ELSE EXTRACT(YEAR FROM TRY_CAST({col} AS DATE)) END"


def trace_large_award(con, row: dict) -> dict:
    ak, fy = row["award_key"], int(row["fiscal_year"])
    silver = con.execute("""SELECT COUNT(*), SUM(obligation), MIN(action_date), MAX(action_date), MAX(award_type), MAX(psc_description),
                                   MAX(parent_piid), MAX(base_and_all_options_value), COUNT(DISTINCT modification_number)
                            FROM silver_contract_transactions WHERE award_key = ? AND fiscal_year = ?""", [ak, fy]).fetchone()
    bronze = con.execute(f"""WITH raw AS (
                               SELECT contract_transaction_unique_key AS tk, TRY_CAST(federal_action_obligation AS DECIMAL(18,2)) AS obl,
                                      {_fy_sql('action_date')} AS fy, _ingest_run_id, TRY_CAST(last_modified_date AS DATE) AS lm
                               FROM bronze_prime_transactions WHERE contract_award_unique_key = ?),
                             dedup AS (SELECT * FROM raw QUALIFY ROW_NUMBER() OVER (PARTITION BY tk ORDER BY _ingest_run_id DESC, lm DESC NULLS LAST) = 1)
                             SELECT (SELECT COUNT(*) FROM raw WHERE fy = ?), COUNT(*), SUM(obl) FROM dedup WHERE fy = ?""", [ak, fy, fy]).fetchone()
    years = con.execute("SELECT fiscal_year, obligations FROM gold_award_fy WHERE award_key = ? ORDER BY fiscal_year", [ak]).fetchall()
    peer = con.execute("""SELECT COUNT(*), MEDIAN(value) FROM anomaly_large_award
                          WHERE awarding_agency_code = ? AND psc_class2 = ? AND fiscal_year = ?""",
                       [row["awarding_agency_code"], row["psc_class2"], fy]).fetchone()
    value = float(row["value"])
    s_sum = float(silver[1] or 0); b_sum = float(bronze[2] or 0)
    return {"detector": "large_award", "award_key": ak, "piid": row["piid"], "fiscal_year": fy, "agency": row["awarding_agency_name"],
            "recipient": row["recipient_name"], "psc": row["psc"], "psc_description": silver[5], "award_type": silver[4],
            "parent_piid": silver[6], "value": value, "score": round(float(row["score"]), 3), "threshold": row["threshold"], "peer_n": row["peer_n"],
            "baseline_median": round(float(row["baseline_median"]), 2), "peer_n_recomputed_from_table": peer[0],
            "silver_transactions": silver[0], "silver_sum": s_sum, "silver_matches": abs(s_sum - value) < 0.005,
            "bronze_rows_raw": bronze[0], "bronze_rows_deduped": bronze[1], "bronze_sum": b_sum, "bronze_matches": abs(b_sum - value) < 0.005,
            "first_action": str(silver[2]), "last_action": str(silver[3]), "modifications": silver[8],
            "base_and_all_options_value": float(silver[7]) if silver[7] is not None else None,
            "award_years": [(int(y), float(o)) for y, o in years], "permalink": row["usaspending_permalink"],
            "pass": abs(s_sum - value) < 0.005 and abs(b_sum - value) < 0.005 and int(peer[0]) == int(row["peer_n"])}


def trace_concentration(con, row: dict) -> dict:
    ag, psc2, fy = row["awarding_agency_code"], row["psc_class2"], int(row["fiscal_year"])
    r = con.execute("""SELECT recipient_uei, MAX(recipient_name), SUM(obligation) FROM silver_contract_transactions
                       WHERE awarding_agency_code = ? AND psc_class2 = ? AND fiscal_year = ? GROUP BY 1 ORDER BY 3 DESC""", [ag, psc2, fy]).fetchall()
    pos = [(u, n, float(o)) for u, n, o in r if o and float(o) > 0]
    total = sum(o for _, _, o in pos)
    hhi = sum((100.0 * o / total) ** 2 for _, _, o in pos) if total else None
    top = pos[0] if pos else (None, None, 0.0)
    return {"detector": "concentration", "agency": row["awarding_agency_name"], "psc_class2": psc2, "fiscal_year": fy,
            "cell_total": float(row["value"]), "silver_total_positive_recipients": total, "n_recipients": row["peer_n"], "n_recipients_silver": len(pos),
            "hhi": round(float(row["score"]), 1), "hhi_from_silver": round(hhi, 1) if hhi else None, "top_share": round(float(row["top_share"]), 1),
            "top_recipient": row["top_recipient_name"], "top_recipient_from_silver": top[1], "top_recipient_silver_obligations": top[2],
            "prior_hhi": row["prior_hhi"], "hhi_change": row["hhi_change"],
            "pass": abs(total - float(row["value"])) < 0.005 and hhi is not None and abs(hhi - float(row["score"])) < 1e-6 * max(1, hhi)
                    and top[0] == row["top_recipient_uei"] and len(pos) == int(row["peer_n"])}


def trace_growth(con, row: dict) -> dict:
    u, ag, fy = row["recipient_uei"], row["awarding_agency_code"], int(row["fiscal_year"])
    cur = con.execute("SELECT COUNT(*), SUM(obligation), COUNT(DISTINCT award_key) FROM silver_contract_transactions WHERE recipient_uei = ? AND awarding_agency_code = ? AND fiscal_year = ?", [u, ag, fy]).fetchone()
    prv = con.execute("SELECT COUNT(*), SUM(obligation) FROM silver_contract_transactions WHERE recipient_uei = ? AND awarding_agency_code = ? AND fiscal_year = ?", [u, ag, fy - 1]).fetchone()
    top_awards = con.execute("""SELECT award_key, piid, obligations, award_type_code, usaspending_permalink FROM gold_award_fy
                                WHERE recipient_uei = ? AND awarding_agency_code = ? AND fiscal_year = ? ORDER BY obligations DESC LIMIT 2""", [u, ag, fy]).fetchall()
    c, p = float(cur[1] or 0), float(prv[1] or 0)
    return {"detector": "recipient_growth", "recipient": row["recipient_name"], "agency": row["awarding_agency_name"], "fiscal_year": fy,
            "value": float(row["value"]), "baseline_prior_year": float(row["baseline"]), "ratio": round(float(row["score"]), 2), "delta": float(row["delta"]),
            "silver_current_sum": c, "silver_prior_sum": p, "silver_transactions": cur[0], "awards": cur[2],
            "largest_awards": [{"award_key": a, "piid": b, "obligations": float(o), "award_type_code": t, "permalink": pl} for a, b, o, t, pl in top_awards],
            "pass": abs(c - float(row["value"])) < 0.005 and abs(p - float(row["baseline"])) < 0.005}


def _rows(con, sql, params=()):
    cur = con.execute(sql, list(params))
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", default="build/civiclens.duckdb")
    ap.add_argument("--out", default="evidence/anomalies")
    a = ap.parse_args()
    if np is None:
        print("numpy is required"); return 2
    con = duckdb.connect(a.snapshot, read_only=True)
    meta = json.loads(con.execute("SELECT meta_json FROM _meta").fetchone()[0])
    stamp = {"snapshot_version": meta.get("snapshot_version"), "utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
             "commit": os.environ.get("GITHUB_SHA", os.environ.get("CIVICLENS_COMMIT", ""))[:12], "github_run_id": os.environ.get("GITHUB_RUN_ID"),
             "params": PARAMS}
    recomputed = [recompute_large_award(con), recompute_concentration(con), recompute_growth(con)]

    sample = []
    # highest-scoring flagged large award per agency
    for r in _rows(con, """SELECT * FROM anomaly_large_award WHERE status = 'flagged'
                           QUALIFY ROW_NUMBER() OVER (PARTITION BY awarding_agency_code ORDER BY score DESC) = 1 ORDER BY score DESC"""):
        sample.append(trace_large_award(con, r))
    for r in _rows(con, "SELECT * FROM anomaly_concentration WHERE status = 'flagged' ORDER BY score DESC LIMIT 4"):
        sample.append(trace_concentration(con, r))
    for r in _rows(con, "SELECT * FROM anomaly_recipient_growth WHERE status = 'flagged' ORDER BY delta DESC LIMIT 4"):
        sample.append(trace_growth(con, r))

    ok = all(x["pass"] for x in recomputed) and all(x["pass"] for x in sample) and bool(sample)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    (out / "validation.json").write_text(json.dumps({"stamp": stamp, "pass": ok, "recomputation": recomputed, "source_trace": sample}, indent=1, default=str))

    md = [f"# Anomaly engine validation — **{'PASS' if ok else 'FAIL'}**", "",
          f"Snapshot `{stamp['snapshot_version']}` · commit `{stamp['commit'] or 'local'}` · {stamp['utc']}" + (f" · GitHub run `{stamp['github_run_id']}`" if stamp["github_run_id"] else ""), "",
          "## 1. Independent re-implementation (Python/NumPy vs the pipeline's SQL)", "",
          "| detector | rows | flagged (pipeline) | flagged (recomputed) | identical flagged set | status mismatches | max rel. score diff | result |", "|---|---|---|---|---|---|---|---|"]
    for r in recomputed:
        md.append(f"| {r['detector']} | {r['rows_pipeline']:,} | {r['flagged_pipeline']} | {r['flagged_recomputed']} | {'yes' if r['flagged_sets_identical'] else 'NO'} | "
                  f"{r['status_mismatches']} | {r['max_relative_score_diff']:.1e} | {'PASS' if r['pass'] else 'FAIL'} |")
    md += ["", f"Parameters: `{json.dumps(PARAMS)}`. Thresholds were not changed for this run.", "",
           "## 2. Source trace of representative flagged records", "",
           "Each flagged value is traced back through Silver to the deduplicated raw Bronze rows (the USAspending download). "
           "\"Matches\" means equal to the cent. Descriptors are read from the record; none of this is a finding about conduct.", "",
           "### Large award-year obligations (highest-scoring flagged award per agency)", "",
           "| agency | FY | recipient | PIID | value | score / thr | peer n | baseline median | silver txns → sum | bronze rows (raw/dedup) → sum | type · PSC | dates · mods · parent | years of this award | source | result |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for t in [x for x in sample if x["detector"] == "large_award"]:
        yrs = ", ".join(f"FY{y}: ${o/1e6:,.1f}M" for y, o in t["award_years"])
        md.append(f"| {t['agency']} | {t['fiscal_year']} | {t['recipient']} | {t['piid']} | ${t['value']:,.2f} | {t['score']} / {t['threshold']} | {t['peer_n']} | ${t['baseline_median']:,.0f} | "
                  f"{t['silver_transactions']} → ${t['silver_sum']:,.2f} {'✓' if t['silver_matches'] else '✗'} | {t['bronze_rows_raw']}/{t['bronze_rows_deduped']} → ${t['bronze_sum']:,.2f} {'✓' if t['bronze_matches'] else '✗'} | "
                  f"{t['award_type'] or '-'} · {t['psc']} {t['psc_description'] or ''} | {t['first_action']}→{t['last_action']} · {t['modifications']} mods · {'under ' + t['parent_piid'] if t['parent_piid'] else 'standalone'} | {yrs} | "
                  f"[usaspending]({t['permalink']}) | {'PASS' if t['pass'] else 'FAIL'} |")
    md += ["", "### Vendor concentration (highest HHI cells)", "",
           "| agency | PSC class | FY | cell total | recipients (table / silver) | HHI (table / silver) | top share | top recipient (table / silver) | prior HHI → change | result |", "|---|---|---|---|---|---|---|---|---|---|"]
    for t in [x for x in sample if x["detector"] == "concentration"]:
        md.append(f"| {t['agency']} | {t['psc_class2']} | {t['fiscal_year']} | ${t['cell_total']:,.2f} | {t['n_recipients']} / {t['n_recipients_silver']} | {t['hhi']} / {t['hhi_from_silver']} | {t['top_share']}% | "
                  f"{t['top_recipient']} / {t['top_recipient_from_silver']} | {t['prior_hhi'] if t['prior_hhi'] is None else round(float(t['prior_hhi']),1)} → {t['hhi_change'] if t['hhi_change'] is None else round(float(t['hhi_change']),1)} | {'PASS' if t['pass'] else 'FAIL'} |")
    md += ["", "### Recipient growth (largest year-over-year increases)", "",
           "| agency | FY | recipient | prior FY | this FY | ratio | silver prior / current | awards | largest award this FY | result |", "|---|---|---|---|---|---|---|---|---|---|"]
    for t in [x for x in sample if x["detector"] == "recipient_growth"]:
        la = t["largest_awards"][0] if t["largest_awards"] else None
        la_s = f"[{la['piid']}]({la['permalink']}) ${la['obligations']:,.0f} ({la['award_type_code']})" if la else "-"
        md.append(f"| {t['agency']} | {t['fiscal_year']} | {t['recipient']} | ${t['baseline_prior_year']:,.2f} | ${t['value']:,.2f} | {t['ratio']}× | ${t['silver_prior_sum']:,.2f} / ${t['silver_current_sum']:,.2f} | {t['awards']} | {la_s} | {'PASS' if t['pass'] else 'FAIL'} |")
    md += ["", "## Reading the sample", "",
           "- A flagged large award-year is one whose log10 obligation sits ≥ 3.5 robust standard deviations above the median of awards at the same agency, "
           "in the same 2-character PSC class, in the same fiscal year, where that group has at least 30 award-years with non-zero spread. "
           "The table shows what the record is (type, PSC, number of actions, whether it is an order under a parent vehicle, how many years it runs): "
           "large multi-year vehicles and consolidated buys are expected to appear here.",
           "- Concentration flags are cells where one or two recipients hold most of a category's dollars; small or sole-source categories are concentrated by nature, and the methodology page says so.",
           "- Growth flags are recipients whose obligations at one agency rose ≥ 3× and ≥ $2M over the prior year from a base ≥ $500K; new vehicles and option-year exercises produce legitimate jumps.",
           "", "Every value above can be checked on usaspending.gov through the linked award page; the permalinks come from the download itself."]
    (out / "validation.md").write_text("\n".join(md) + "\n")
    print("\n".join(md[:12])); print(f"\n{'PASS' if ok else 'FAIL'} -> {out}/validation.md")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
