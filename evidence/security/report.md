# Security gate — **PASS**

GitHub run `40214110609` · commit `95900f2a6737` · 2026-10-25T16:57:46+00:00

- gitleaks over the full git history (`--log-opts=--all`): 0 finding(s)
- pip-audit (dependencies of api, lakehouse, ingest; 60 packages audited): 0 vulnerable package(s) 
- npm audit (web, production dependencies): {"info": 0, "low": 0, "moderate": 0, "high": 0, "critical": 0, "total": 0}
- all scanners produced a report: True

Rate limits in production: per-IP hourly and global daily caps on the investigator, a monthly token budget that switches to cached answers, read-only tools only (no SQL tool, no network, no writes), and all secrets provided via GitHub Actions secrets / Fly secrets — never in source.
