# Databricks lakehouse run — **PASS**

GitHub run `40005551673` · commit `5a45d15236f0` · 2026-10-23T18:47:55+00:00 · catalog `workspace` · ingest run `39997561946` · Databricks job 862977884764769 run 577799826358384 · serverless environment client `3` · wheel `/Volumes/workspace/bronze/raw/_libs/civiclens_lakehouse-0.1.0-py3-none-any.whl` · state SUCCESS · [run page](https://dbc-b531337f-7f65.cloud.databricks.com/?o=7474654994685709#job/862977884764769/run/577799826358384)

Tables: `workspace.bronze.prime_transactions`, `workspace.silver.contract_transactions`, `workspace.silver.rejects`, `workspace.gold.award_fy|agency_fy|recipient_agency_fy|psc_fy`, `workspace.gold.anomaly_large_award|anomaly_concentration|anomaly_recipient_growth` (Delta, Unity Catalog).

| metric | Databricks (Spark, Delta) | DuckDB build of the same raw data | match |
|---|---|---|---|
| bronze | 109883 | 109883 | yes |
| silver | 109883 | 109883 | yes |
| rejects | 0 | 0 | yes |
| silver_sum | 109830250044.05 | 109830250044.05 | yes |
| gold_award_sum | 109830250044.05 | 109830250044.05 | yes |
| flagged_large | 157 | 157 | yes |
| scored_large | 45044 | 45044 | yes |

Databricks in-job DQ: `{"bronze": 109883, "silver": 109883, "rejects": 0, "silver_sum": 109830250044.05, "gold_award_sum": 109830250044.05, "flagged_large": 157, "scored_large": 45044, "gold_equals_silver": true, "catalog": "workspace"}`
