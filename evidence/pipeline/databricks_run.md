# Databricks lakehouse run — **FAIL**

GitHub run `39998030675` · commit `43dc0057ef6b` · 2026-10-23T17:52:14+00:00 · catalog `workspace` · ingest run `39997561946` · Databricks job 862977884764769 run 145677054756609 · state FAILED · [run page](https://dbc-b531337f-7f65.cloud.databricks.com/?o=7474654994685709#job/862977884764769/run/145677054756609)

Tables: `workspace.bronze.prime_transactions`, `workspace.silver.contract_transactions`, `workspace.silver.rejects`, `workspace.gold.award_fy|agency_fy|recipient_agency_fy|psc_fy`, `workspace.gold.anomaly_large_award|anomaly_concentration|anomaly_recipient_growth` (Delta, Unity Catalog).

| metric | Databricks (Spark, Delta) | DuckDB build of the same raw data | match |
|---|---|---|---|
| (no DuckDB snapshot supplied; Databricks DQ only) | | | |

Databricks in-job DQ: `{}`

Task silver_gold_anomalies error: `OSError: [Errno 5] Input/output error: '/Workspace/Users/sagarmodha9@gmail.com/civiclens-ai/lakehouse/civiclens_lakehouse/sql/silver_contract_transactions.sql'
Error(message=403 Forbidden: 
AccessDeniedRequests specifying Server Side Encryption with Customer provided keys must provide the correct secret key.5HSDZAYYCSECW6DYHhgpxyM9SZ+GFmHb7C/Y84XwwX02WfmE5XGzgwVy2HPWglw8TmdcIaum5mdz5O1Lo/t9u7YgDKA=, errorCode=system/Blob.SignedUrl.RequestError, errno=permission denied, statusCode=403)
 -> 403 Fo`

Task silver_gold_anomalies error: `OSError: [Errno 5] Input/output error: '/Workspace/Users/sagarmodha9@gmail.com/civiclens-ai/lakehouse/civiclens_lakehouse/sql/silver_contract_transactions.sql'
Error(message=403 Forbidden: 
AccessDeniedRequests specifying Server Side Encryption with Customer provided keys must provide the correct secret key.N0TEEY5GDF0M76P9BIs6eJkuBmnrAkI6N7zsG05APhKAu8B2dpWrEYbyWtcuabmC/i4Vit773V0g4t9FFzXqc8OXh1zdT5tYK4zJpkrFXSSbbEUo, errorCode=system/Blob.SignedUrl.RequestError, errno=permission denied, status`
