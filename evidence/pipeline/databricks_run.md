# Databricks lakehouse run — **FAIL**

GitHub run `40000440021` · commit `612e7aee7576` · 2026-10-23T18:07:55+00:00 · catalog `workspace` · ingest run `39997561946` · Databricks job 862977884764769 run 498821750520803 · state FAILED · [run page](https://dbc-b531337f-7f65.cloud.databricks.com/?o=7474654994685709#job/862977884764769/run/498821750520803)

Tables: `workspace.bronze.prime_transactions`, `workspace.silver.contract_transactions`, `workspace.silver.rejects`, `workspace.gold.award_fy|agency_fy|recipient_agency_fy|psc_fy`, `workspace.gold.anomaly_large_award|anomaly_concentration|anomaly_recipient_growth` (Delta, Unity Catalog).

| metric | Databricks (Spark, Delta) | DuckDB build of the same raw data | match |
|---|---|---|---|
| (no DuckDB snapshot supplied; Databricks DQ only) | | | |

Databricks in-job DQ: `{}`

Task bronze error: `Run failed with error message
 Cannot launch the cluster. Cause: Invalid platform channel Client-1. INVALID_PARAMETER_VALUE: INVALID_PARAMETER_VALUE: Workspace doesn't support Client-1 channel for REPL. (requestId=27c777da-fb54-4746-9222-052fd435248f)`

Task silver_gold_anomalies error: `Run result unavailable: The task was skipped because not all its dependencies were executed and succeeded.`
