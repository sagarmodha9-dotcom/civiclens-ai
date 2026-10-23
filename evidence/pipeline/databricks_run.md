# Databricks lakehouse run — **FAIL**

GitHub run `39996200492` · commit `c4b7b8ebfd42` · 2026-10-23T17:43:14+00:00 · catalog `workspace` · ingest run `39995114903` · Databricks job 862977884764769 run 438986202905306 · state FAILED · [run page](https://dbc-b531337f-7f65.cloud.databricks.com/?o=7474654994685709#job/862977884764769/run/438986202905306)

Tables: `workspace.bronze.prime_transactions`, `workspace.silver.contract_transactions`, `workspace.silver.rejects`, `workspace.gold.award_fy|agency_fy|recipient_agency_fy|psc_fy`, `workspace.gold.anomaly_large_award|anomaly_concentration|anomaly_recipient_growth` (Delta, Unity Catalog).

| metric | Databricks (Spark, Delta) | DuckDB build of the same raw data | match |
|---|---|---|---|
| (no DuckDB snapshot supplied; Databricks DQ only) | | | |

Databricks in-job DQ: `{}`

Task silver_gold_anomalies error: `OSError: [Errno 5] Input/output error: '/Workspace/Users/sagarmodha9@gmail.com/civiclens-ai/lakehouse/civiclens_lakehouse/pipeline.py'
[Trace ID: 00-0c5a363a4cbe81b8ab2c0ec1c9bb1b3d-a22908abc9924f6c-00]`

Task silver_gold_anomalies error: `[DATATYPE_MISSING_SIZE] DataType "VARCHAR" requires a length parameter, for example "VARCHAR"(10). Please specify the length. SQLSTATE: 42K01`
