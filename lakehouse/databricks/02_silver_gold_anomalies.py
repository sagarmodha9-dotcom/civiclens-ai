# Databricks notebook source
# MAGIC %md
# MAGIC # Silver → Gold → anomalies → DQ, running the SAME SQL files as the local DuckDB build.
# MAGIC The SQL lives in the repo (`lakehouse/civiclens_lakehouse/sql`); this notebook only maps table names into
# MAGIC Unity Catalog and substitutes parameters. Any divergence between engines is a bug, caught by comparing the
# MAGIC DQ numbers here with the DuckDB snapshot's `_meta`.

# COMMAND ----------
import json, re, sys
from pathlib import Path
repo_root = Path(dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()).parents[2]
sys.path.insert(0, f"/Workspace{repo_root}/lakehouse")
from civiclens_lakehouse.pipeline import PARAMS, REQUIRED_COLUMNS, INGEST_COLUMNS, render

dbutils.widgets.text("catalog", "workspace")
CATALOG = dbutils.widgets.get("catalog") or "workspace"   # Free Edition: see 01_bronze.py
NAMES = {"bronze_prime_transactions": f"{CATALOG}.bronze.prime_transactions",
         "silver_rejects": f"{CATALOG}.silver.rejects", "silver_contract_transactions": f"{CATALOG}.silver.contract_transactions",
         "gold_award_fy": f"{CATALOG}.gold.award_fy", "gold_agency_fy": f"{CATALOG}.gold.agency_fy",
         "gold_recipient_agency_fy": f"{CATALOG}.gold.recipient_agency_fy", "gold_psc_fy": f"{CATALOG}.gold.psc_fy",
         "anomaly_large_award": f"{CATALOG}.gold.anomaly_large_award", "anomaly_concentration": f"{CATALOG}.gold.anomaly_concentration",
         "anomaly_recipient_growth": f"{CATALOG}.gold.anomaly_recipient_growth"}

def to_uc(sql: str) -> str:
    for k, v in NAMES.items():
        sql = re.sub(rf"\b{k}\b", v, sql)
    return sql

cols = [f.name for f in spark.table(NAMES["bronze_prime_transactions"]).schema]
missing = [c for c in REQUIRED_COLUMNS + INGEST_COLUMNS if c not in cols]
assert not missing, f"schema drift: bronze missing {missing}"

# COMMAND ----------
for name in ("silver_rejects.sql", "silver_contract_transactions.sql", "gold.sql", "anomalies.sql"):
    for stmt in render(name, PARAMS).split(";\n"):
        s = stmt.strip()
        if s and not all(l.strip().startswith("--") for l in s.splitlines()):
            spark.sql(to_uc(s))
    print("ran", name)

# COMMAND ----------
q = lambda sql: spark.sql(to_uc(sql)).collect()[0][0]
dq = {
  "bronze": q("SELECT COUNT(*) FROM bronze_prime_transactions"),
  "silver": q("SELECT COUNT(*) FROM silver_contract_transactions"),
  "rejects": q("SELECT COUNT(*) FROM silver_rejects"),
  "silver_sum": float(q("SELECT COALESCE(SUM(obligation),0) FROM silver_contract_transactions")),
  "gold_award_sum": float(q("SELECT COALESCE(SUM(obligations),0) FROM gold_award_fy")),
  "flagged_large": q("SELECT COUNT(*) FROM anomaly_large_award WHERE status='flagged'"),
  "scored_large": q("SELECT COUNT(*) FROM anomaly_large_award WHERE status IN ('flagged','normal')"),
}
dq["gold_equals_silver"] = abs(dq["silver_sum"] - dq["gold_award_sum"]) < 0.005
print(json.dumps(dq, indent=1))
assert dq["gold_equals_silver"], "Gold does not reconcile to Silver"
dq["catalog"] = CATALOG
dbutils.notebook.exit(json.dumps(dq))
