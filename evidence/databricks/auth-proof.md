# Databricks unattended-auth proof — 2026-10-23T13:11Z

host used: https://dbc-b531337f-7f65.cloud.databricks.com
token shape: ok (dapi…)
host shape: ok

| step | HTTP | note |
|---|---|---|
| whoami (SCIM Me) | 200 | sagarmodha9@gmail.com |
| list catalogs | 200 | |
| Files API PUT to Volume | 404 | needs catalog civiclens, schema bronze, volume raw to exist |
| Files API GET | 404 | |
| Files API DELETE | 404 | |
| Jobs API list | 200 | |
