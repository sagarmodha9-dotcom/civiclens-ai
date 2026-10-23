# Databricks preflight — **FAIL**

GitHub run `39982507928` · commit `be3c52636d5d` · 2026-10-23T15:56:15+00:00 · host `https://dbc-b531337f-7f65.cloud.databricks.com/settings/user/developer/access-tokens?o=7474654994685709` · working catalog `None`

Free Edition has no metastore storage root, so `CREATE CATALOG` is not supported (400 INVALID_STATE on 2026-10-23); the lakehouse uses the built-in `workspace` catalog. Each row below is tested on its own; nothing is inferred.

| step | result | HTTP | note |
|---|---|---|---|
| script crashed | FAIL |  | JSONDecodeError: Expecting value: line 1 column 1 (char 0) |
