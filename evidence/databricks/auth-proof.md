# Databricks unattended-auth proof — 2026-10-23T02:33Z

| step | HTTP | note |
|---|---|---|
| whoami (SCIM Me) | 303 |  |
| list catalogs | 303 | |
| Files API PUT to Volume | 404 | needs catalog civiclens, schema bronze, volume raw to exist |
| Files API GET | 303 | |
| Files API DELETE | 404 | |
| Jobs API list | 303 | |
