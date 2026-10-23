# Security gate — **FAIL**

GitHub run `40010952694` · commit `ad9b3c38c1a6` · 2026-10-23T19:23:34+00:00

- gitleaks over the full git history (`--log-opts=--all`): 0 finding(s)
- pip-audit (dependencies of api, lakehouse, ingest; 60 packages audited): 0 vulnerable package(s) 
- npm audit (web, production dependencies): {"info": 0, "low": 0, "moderate": 0, "high": 2, "critical": 1, "total": 3}
- all scanners produced a report: True

Rate limits in production: per-IP hourly and global daily caps on the investigator, a monthly token budget that switches to cached answers, read-only tools only (no SQL tool, no network, no writes), and all secrets provided via GitHub Actions secrets / Fly secrets — never in source.
