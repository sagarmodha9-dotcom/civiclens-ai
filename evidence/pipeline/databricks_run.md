# Databricks lakehouse run — **PASS**

GitHub run `40365555689` · commit `6b5f05aabf91` · 2026-10-26T17:18:18+00:00 · catalog `workspace` · ingest run `40356624310` · Databricks job 862977884764769 run 359749917343233 · serverless environment client `3` · wheel `/Volumes/workspace/bronze/raw/_libs/civiclens_lakehouse-0.1.0-py3-none-any.whl` · state SUCCESS · [run page](https://dbc-b531337f-7f65.cloud.databricks.com/?o=7474654994685709#job/862977884764769/run/359749917343233)

Tables: `workspace.bronze.prime_transactions`, `workspace.silver.contract_transactions`, `workspace.silver.rejects`, `workspace.gold.award_fy|agency_fy|recipient_agency_fy|psc_fy`, `workspace.gold.anomaly_large_award|anomaly_concentration|anomaly_recipient_growth` (Delta, Unity Catalog).

| metric | Databricks (Spark, Delta) | DuckDB build of the same raw data | match |
|---|---|---|---|
| bronze | 109885 | 109885 | yes |
| silver | 109885 | 109885 | yes |
| rejects | 0 | 0 | yes |
| silver_sum | 109830518939.19 | 109830518939.19 | yes |
| gold_award_sum | 109830518939.19 | 109830518939.19 | yes |
| flagged_large | 157 | 157 | yes |
| scored_large | 45044 | 45044 | yes |

Databricks in-job DQ: `{"bronze": 109885, "silver": 109885, "rejects": 0, "silver_sum": 109830518939.19, "gold_award_sum": 109830518939.19, "flagged_large": 157, "scored_large": 45044, "gold_equals_silver": true, "catalog": "workspace"}`
