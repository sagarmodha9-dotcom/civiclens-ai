# Security gate — **PASS**

GitHub run `40008859311` · commit `015d267d38a9` · 2026-10-23T19:07:45+00:00

- gitleaks over the full git history (`--log-opts=--all`): 0 finding(s)
- pip-audit (api, lakehouse, ingest): 0 vulnerable package(s) 
- npm audit (web, production dependencies): {}

Rate limits in production: per-IP hourly and global daily caps on the investigator, a monthly token budget that switches to cached answers, read-only tools only (no SQL tool, no network, no writes), and all secrets provided via GitHub Actions secrets / Fly secrets — never in source.
