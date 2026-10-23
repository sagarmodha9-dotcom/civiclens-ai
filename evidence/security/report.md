# Security gate — **PASS**

GitHub run `40007621718` · commit `bf633757d939` · 2026-10-23T18:58:28+00:00

- gitleaks over the full git history (`--log-opts=--all`): 0 finding(s)
- pip-audit (api, lakehouse, ingest): 0 vulnerable package(s) 
- npm audit (web, production dependencies): {}

Rate limits in production: per-IP hourly and global daily caps on the investigator, a monthly token budget that switches to cached answers, read-only tools only (no SQL tool, no network, no writes), and all secrets provided via GitHub Actions secrets / Fly secrets — never in source.
