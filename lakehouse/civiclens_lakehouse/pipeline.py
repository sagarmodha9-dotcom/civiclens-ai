"""Bronze -> Silver -> Gold -> anomalies -> DQ, as one runner that executes the same SQL files on DuckDB (local
tests and the published snapshot) or on Spark (Databricks job). The SQL is the single source of truth; the two
engines differ only in how a statement is executed and how Bronze is loaded.

    python -m civiclens_lakehouse.pipeline --raw data/raw --db build/civiclens.duckdb

Schema contract: Bronze must expose the REQUIRED_COLUMNS below (names from the USAspending transaction download,
confirmed against the first live cell). Missing columns fail the run with the full list, never a silent remap.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

SQL_DIR = Path(__file__).parent / "sql"

REQUIRED_COLUMNS = [
    "contract_transaction_unique_key", "contract_award_unique_key", "award_id_piid", "parent_award_id_piid",
    "modification_number", "action_date", "federal_action_obligation", "base_and_exercised_options_value",
    "base_and_all_options_value", "awarding_agency_code", "awarding_agency_name", "awarding_sub_agency_code",
    "awarding_sub_agency_name", "funding_agency_code", "funding_agency_name", "recipient_uei", "recipient_name",
    "recipient_parent_uei", "recipient_parent_name", "product_or_service_code", "product_or_service_code_description",
    "naics_code", "naics_description", "award_type_code", "award_type", "action_type_code", "action_type",
    "period_of_performance_start_date", "period_of_performance_current_end_date", "last_modified_date",
    "usaspending_permalink",
]
INGEST_COLUMNS = ["_ingest_run_id", "_ingest_agency_code", "_ingest_fiscal_year", "_ingest_file"]

PARAMS = {"baseline_fys": "2022,2023,2024,2025", "min_peer_n": 30, "z_threshold": 3.5, "hhi_threshold": 2500,
          "hhi_top_share": 50, "hhi_min_spend": 5_000_000, "growth_ratio": 3, "growth_min_delta": 2_000_000,
          "growth_min_base": 500_000}


class SchemaDriftError(Exception):
    pass


def render(name: str, params: dict | None = None) -> str:
    text = (SQL_DIR / name).read_text()
    for k, v in (params or PARAMS).items():
        text = text.replace("{" + k + "}", str(v))
    return text


def statements(name: str, params: dict | None = None) -> list[str]:
    return [s.strip() for s in render(name, params).split(";") if s.strip() and not s.strip().startswith("--") or
            (s.strip() and "CREATE" in s.upper())]


def check_schema(columns: list[str]) -> None:
    missing = [c for c in REQUIRED_COLUMNS + INGEST_COLUMNS if c not in columns]
    if missing:
        raise SchemaDriftError(f"bronze is missing {len(missing)} required columns: {missing}")


# ---------------------------------------------------------------- DuckDB engine (tests + snapshot)
def load_bronze_duckdb(con, raw_root: Path) -> dict:
    """Load every cell's prime-transactions CSV(s) listed in its manifest, tagging rows with ingest metadata.
    Files are unioned BY NAME so a column added or dropped by USAspending in one cell cannot shift data between
    columns; the schema contract check then decides whether the result is usable."""
    import duckdb  # noqa: F401
    cells, selects = [], []
    manifests = sorted(raw_root.rglob("manifest.json"))
    manifests = [m for m in manifests if m.parent.name.startswith("fy=") and m.parent.parent.name.startswith("agency=")]
    if not manifests:
        raise FileNotFoundError(f"no agency=*/fy=*/manifest.json under {raw_root} (searched recursively; artifact downloads nest one folder deeper)")
    for manifest in manifests:
        m = json.loads(manifest.read_text())
        for f in m["files"]:
            if f.get("kind") != "prime_transactions":
                continue
            path = manifest.parent / f["name"]
            selects.append(f"SELECT *, '{m['run_id']}' AS _ingest_run_id, '{m['agency_code']}' AS _ingest_agency_code, "
                           f"{int(m['fiscal_year'])} AS _ingest_fiscal_year, '{f['name']}' AS _ingest_file "
                           f"FROM read_csv('{path}', header=true, all_varchar=true, sample_size=-1)")
            cells.append({"agency_code": m["agency_code"], "fiscal_year": m["fiscal_year"], "file": f["name"],
                          "rows_manifest": f["rows"], "run_id": m["run_id"]})
    if not selects:
        raise FileNotFoundError(f"no prime-transactions files under {raw_root}")
    con.execute("CREATE OR REPLACE TABLE bronze_prime_transactions AS " + " UNION ALL BY NAME ".join(selects))
    cols = [r[0] for r in con.execute("DESCRIBE bronze_prime_transactions").fetchall()]
    check_schema(cols)
    loaded = con.execute("SELECT COUNT(*) FROM bronze_prime_transactions").fetchone()[0]
    expected = sum(c["rows_manifest"] for c in cells)
    if loaded != expected:
        raise ValueError(f"bronze rows {loaded} != manifests total {expected}: a CSV did not parse to its manifest row count")
    return {"cells": cells, "columns": len(cols), "rows": loaded}


def run_sql_duckdb(con, name: str, params: dict | None = None) -> None:
    for stmt in render(name, params).split(";\n"):
        s = stmt.strip()
        if s and not all(line.strip().startswith("--") for line in s.splitlines()):
            con.execute(s)


def dq_checks(con) -> dict:
    """Data-quality gate. Every check returns pass/fail with the numbers; publish refuses on any fail."""
    q = lambda sql: con.execute(sql).fetchone()[0]  # noqa: E731
    bronze = q("SELECT COUNT(*) FROM bronze_prime_transactions")
    silver = q("SELECT COUNT(*) FROM silver_contract_transactions")
    rejects = q("SELECT COUNT(*) FROM silver_rejects")
    dup_keys = q("SELECT COUNT(*) - COUNT(DISTINCT contract_transaction_unique_key) FROM bronze_prime_transactions "
                 "WHERE contract_transaction_unique_key IS NOT NULL AND contract_transaction_unique_key <> ''")
    silver_sum = q("SELECT COALESCE(SUM(obligation),0) FROM silver_contract_transactions")
    gold_award_sum = q("SELECT COALESCE(SUM(obligations),0) FROM gold_award_fy")
    gold_agency_sum = q("SELECT COALESCE(SUM(obligations),0) FROM gold_agency_fy")
    bad_fy = q("SELECT COUNT(*) FROM silver_contract_transactions WHERE fiscal_year <> _ingest_fiscal_year")
    checks = {
        "silver_unique_keys": {"pass": q("SELECT COUNT(*) - COUNT(DISTINCT transaction_key) FROM silver_contract_transactions") == 0},
        "bronze_accounted_for": {"pass": bronze == silver + rejects + dup_keys, "bronze": bronze, "silver": silver,
                                 "rejects": rejects, "duplicate_keys": dup_keys},
        "gold_award_equals_silver": {"pass": abs(float(silver_sum) - float(gold_award_sum)) < 0.005,
                                     "silver": float(silver_sum), "gold_award_fy": float(gold_award_sum)},
        "gold_agency_equals_silver": {"pass": abs(float(silver_sum) - float(gold_agency_sum)) < 0.005,
                                      "gold_agency_fy": float(gold_agency_sum)},
        "fiscal_year_matches_cell": {"pass": bad_fy == 0, "rows_outside_their_cell_fy": bad_fy},
        "flag_rate_large_award": {},
    }
    scored = q("SELECT COUNT(*) FROM anomaly_large_award WHERE status IN ('flagged','normal')")
    flagged = q("SELECT COUNT(*) FROM anomaly_large_award WHERE status = 'flagged'")
    rate = (flagged / scored) if scored else 0.0
    # design rate ~2% on log-normal peers; the gate fails only past 5%, which would mean the peer grouping is wrong
    checks["flag_rate_large_award"] = {"pass": rate <= 0.05, "scored": scored, "flagged": flagged, "rate": round(rate, 4),
                                       "note": "design <=2% on log-normal peers; >2% is reviewed, >5% fails"}
    # FY derived from action_date must equal the file's own action_date_fiscal_year column wherever it is present
    has_src_fy = "action_date_fiscal_year" in [r[0] for r in con.execute("DESCRIBE bronze_prime_transactions").fetchall()]
    bad_src_fy = 0 if not has_src_fy else q("SELECT COUNT(*) FROM silver_contract_transactions s JOIN bronze_prime_transactions b "
                   "ON b.contract_transaction_unique_key = s.transaction_key "
                   "WHERE TRY_CAST(b.action_date_fiscal_year AS INTEGER) IS NOT NULL AND TRY_CAST(b.action_date_fiscal_year AS INTEGER) <> s.fiscal_year")
    checks["fiscal_year_matches_source_column"] = {"pass": bad_src_fy == 0, "mismatches_vs_action_date_fiscal_year": bad_src_fy,
                                                   "source_column_present": has_src_fy}
    checks["_all_pass"] = all(v.get("pass", False) for k, v in checks.items() if not k.startswith("_"))
    return checks


def anomaly_summary(con) -> dict:
    """Rows vs scored vs FLAGGED per detector, with abstention reasons. Reports and dashboards must show flagged
    counts, never table row counts, as 'anomalies'."""
    out = {}
    for t in ("anomaly_large_award", "anomaly_concentration", "anomaly_recipient_growth"):
        rows = con.execute(f"SELECT status, COUNT(*) FROM {t} GROUP BY status ORDER BY 2 DESC").fetchall()
        by = {st: n for st, n in rows}
        out[t.replace("anomaly_", "")] = {"rows": sum(by.values()), "flagged": by.get("flagged", 0), "normal": by.get("normal", 0),
                                          "scored": by.get("flagged", 0) + by.get("normal", 0),
                                          "not_scored": {st: n for st, n in by.items() if st.startswith("not scored")}}
    return out


def build_duckdb(raw_root: Path, db_path: Path, params: dict | None = None) -> dict:
    import duckdb
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    con = duckdb.connect(str(db_path))
    bronze = load_bronze_duckdb(con, raw_root)
    for name in ("silver_rejects.sql", "silver_contract_transactions.sql", "gold.sql", "anomalies.sql"):
        run_sql_duckdb(con, name, params)
    dq = dq_checks(con)
    meta = {"built_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "bronze": bronze,
            "params": params or PARAMS, "dq": dq, "anomaly_summary": anomaly_summary(con),
            "tables": {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in
                       ("bronze_prime_transactions", "silver_contract_transactions", "silver_rejects", "gold_award_fy",
                        "gold_agency_fy", "gold_recipient_agency_fy", "gold_psc_fy", "anomaly_large_award",
                        "anomaly_concentration", "anomaly_recipient_growth")}}
    con.execute("CREATE OR REPLACE TABLE _meta AS SELECT ? AS meta_json", [json.dumps(meta, default=str)])
    con.close()
    return meta


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="data/raw")
    ap.add_argument("--db", default="build/civiclens.duckdb")
    ap.add_argument("--report", default="evidence/pipeline/local_build.json")
    a = ap.parse_args()
    meta = build_duckdb(Path(a.raw), Path(a.db))
    Path(a.report).parent.mkdir(parents=True, exist_ok=True)
    Path(a.report).write_text(json.dumps(meta, indent=1, default=str))
    print(json.dumps(meta["tables"], indent=1))
    print("grains: gold_award_fy = award x FY; gold_agency_fy = agency x FY x IT category (services | equipment); "
          "gold_recipient_agency_fy = recipient x agency x FY; gold_psc_fy = agency x FY x PSC class")
    print("anomalies (flagged / scored / rows):", {k: f"{v['flagged']} / {v['scored']} / {v['rows']}" for k, v in meta["anomaly_summary"].items()})
    for k, v in meta["anomaly_summary"].items():
        if v["not_scored"]:
            print(f"  {k} not scored: {v['not_scored']}")
    print("DQ all pass:", meta["dq"]["_all_pass"])
    return 0 if meta["dq"]["_all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
