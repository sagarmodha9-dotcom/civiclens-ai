# Security gate — **FAIL**

GitHub run `40005517016` · commit `fe31ee605671` · 2026-10-23T18:42:47+00:00

- gitleaks over the full git history (`--log-opts=--all`): 40 finding(s)
- pip-audit (api, lakehouse, ingest): 0 vulnerable package(s) 
- npm audit (web, production dependencies): {}

Rate limits in production: per-IP hourly and global daily caps on the investigator, a monthly token budget that switches to cached answers, read-only tools only (no SQL tool, no network, no writes), and all secrets provided via GitHub Actions secrets / Fly secrets — never in source.
