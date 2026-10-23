# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze: load raw USAspending prime-transaction CSVs from the Volume, as received, with ingest metadata.
# MAGIC Idempotent per cell: a cell's rows are replaced by run_id (newest manifest wins); nothing is appended twice.

# COMMAND ----------
import json
from pyspark.sql import functions as F

# Free Edition cannot create catalogs (no metastore storage root -> 400 INVALID_STATE, see evidence/databricks/preflight.md),
# so the lakehouse lives in the catalog the workspace ships with (`workspace`), passed in as a job parameter.
dbutils.widgets.text("catalog", "workspace")
CATALOG = dbutils.widgets.get("catalog") or "workspace"
VOL = f"/Volumes/{CATALOG}/bronze/raw"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.bronze")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.silver")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.gold")

manifests = [p.path for p in dbutils.fs.ls(VOL) if p.name.startswith("agency=")]
cells = []
for agency_dir in manifests:
    for fy_dir in dbutils.fs.ls(agency_dir):
        files = {f.name: f.path for f in dbutils.fs.ls(fy_dir.path)}
        if "manifest.json" not in files:
            continue
        m = json.loads(dbutils.fs.head(files["manifest.json"], 10_000_000))
        prime = [f for f in m["files"] if f.get("kind") == "prime_transactions"]
        for f in prime:
            cells.append((m, f, files[f["name"]]))
print(f"{len(cells)} prime files across cells in {CATALOG}")

# COMMAND ----------
spark.sql(f"""CREATE TABLE IF NOT EXISTS {CATALOG}.bronze.prime_transactions_meta (
  agency_code STRING, fiscal_year INT, run_id STRING, file STRING, rows_manifest BIGINT, sha256 STRING, loaded_utc TIMESTAMP)""")
loaded = {(r.agency_code, r.fiscal_year): r.run_id for r in spark.table(f"{CATALOG}.bronze.prime_transactions_meta").collect()}
for m, f, path in cells:
    key = (m["agency_code"], int(m["fiscal_year"]))
    if loaded.get(key) == m["run_id"]:
        print("skip (already loaded)", key, m["run_id"]); continue
    df = (spark.read.option("header", True).option("multiLine", True).option("escape", '"').csv(path)
          .withColumn("_ingest_run_id", F.lit(m["run_id"]))
          .withColumn("_ingest_agency_code", F.lit(m["agency_code"]))
          .withColumn("_ingest_fiscal_year", F.lit(int(m["fiscal_year"])))
          .withColumn("_ingest_file", F.lit(f["name"])))
    n = df.count()
    if n != f["rows"]:
        raise RuntimeError(f"row count {n} != manifest {f['rows']} for {path}")
    if spark.catalog.tableExists(f"{CATALOG}.bronze.prime_transactions"):
        spark.sql(f"DELETE FROM {CATALOG}.bronze.prime_transactions WHERE _ingest_agency_code='{m['agency_code']}' AND _ingest_fiscal_year={int(m['fiscal_year'])}")
        df.write.mode("append").option("mergeSchema", "true").saveAsTable(f"{CATALOG}.bronze.prime_transactions")
    else:
        df.write.mode("overwrite").saveAsTable(f"{CATALOG}.bronze.prime_transactions")
    spark.sql(f"DELETE FROM {CATALOG}.bronze.prime_transactions_meta WHERE agency_code='{m['agency_code']}' AND fiscal_year={int(m['fiscal_year'])}")
    spark.createDataFrame([(m["agency_code"], int(m["fiscal_year"]), m["run_id"], f["name"], f["rows"], f["sha256"])],
                          "agency_code STRING, fiscal_year INT, run_id STRING, file STRING, rows_manifest BIGINT, sha256 STRING") \
        .withColumn("loaded_utc", F.current_timestamp()).write.mode("append").saveAsTable(f"{CATALOG}.bronze.prime_transactions_meta")
    print("loaded", key, n)
print(spark.table(f"{CATALOG}.bronze.prime_transactions").count(), "bronze rows")
