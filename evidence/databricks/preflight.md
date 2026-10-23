# Databricks preflight — **PASS**

GitHub run `39995111579` · commit `7e92b3957701` · 2026-10-23T17:26:52+00:00 · host `https://dbc-b531337f-7f65.cloud.databricks.com` · working catalog `workspace`

Free Edition has no metastore storage root, so `CREATE CATALOG` is not supported (400 INVALID_STATE on 2026-10-23); the lakehouse uses the built-in `workspace` catalog. Each row below is tested on its own; nothing is inferred.

| step | result | HTTP | note |
|---|---|---|---|
| identity | PASS | 200 | sagarmodha9@gmail.com |
| catalogs | PASS | 200 | catalogs=['workspace', 'samples', 'system']; chosen=workspace |
| schema workspace.bronze | PASS | 200 | created |
| schema workspace.silver | PASS | 200 | created |
| schema workspace.gold | PASS | 200 | created |
| volume workspace.bronze.raw | PASS | 200 | s3://dbstorage-prod-39ifewllok/uc/1393fe35-48d3-4c51-bced-acda1e2fc702/aebdc954-fade-4f36-95c4-8a7470eda8ba/__unitystorage/catalogs/1c662f1f-c096-4e76-8076-7267c5e68e2d/volumes/277c7e13-9c31-4569-8e9d-747ac6625ffc |
| files PUT | PASS | 204 |  |
| files GET round-trip | PASS | 200 | content matches |
| files DELETE | PASS | 204 |  |
| jobs list | PASS | 200 | 0 job(s) visible |
| notebook import | PASS | 200 | /Users/sagarmodha9@gmail.com/civiclens-ai/_preflight |
| job execution (serverless notebook, Delta table write+count) | PASS | 200 | state=SUCCESS output=run_id=39995111579 rows=1 user=sagarmodha9@gmail.com url=https://dbc-b531337f-7f65.cloud.databricks.com/?o=7474654994685709#job/782112135411924/run/1106591618996542 |

Job run page: https://dbc-b531337f-7f65.cloud.databricks.com/?o=7474654994685709#job/782112135411924/run/1106591618996542
