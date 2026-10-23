# CivicLens AI — Federal Spending Intelligence & Investigation Platform

Real U.S. federal IT procurement records from [USAspending.gov](https://www.usaspending.gov), transformed on
Databricks (Bronze → Silver → Gold Delta), scored by an explainable anomaly engine, published as a versioned
read-only snapshot behind a FastAPI service and a Next.js site, with an AI investigator that answers only from
SQL it ran and cites the award ids it used.

**Status: M1 (ingestion with verified provenance) in progress.** Nothing here is deployed yet. Every claim of
"works" in this repo is tied to a test result or a file under `evidence/`.

| Area | State | Evidence |
|---|---|---|
| USAspending client: retries, timeouts, pagination, download polling | mock-tested | `ingest/tests/test_client.py` (15 tests) |
| Worker: per agency × FY pull, provenance manifest, idempotent, atomic swap, count check | mock-tested | same |
| Live endpoint validation (schemas, counts, pagination, identifiers) | runs on GitHub Actions | `evidence/probe/summary.md` once the first run lands |
| Databricks unattended automation (Files + Jobs API from Actions) | proof workflow written, not yet run | `evidence/databricks/auth-proof.md` |
| Bronze/Silver/Gold, anomaly engine, API, site, AI investigator, evaluation, deploy | not started (M2–M6) | |

Architecture and decisions: see `docs/M0.md` (mirrors the M0 assessment) and `docs/DECISIONS.md`.

## Scope (MVP)
Six civilian agencies (VA, DHS, HHS, Treasury, Commerce, SSA), fiscal years 2022–2026, prime contract
transactions (award types A, B, C, D) whose PSC starts with `D` (IT and telecom services) or `70` (IT
equipment and software). FY2022–FY2025 is the settled baseline; FY2026 ended Sep 30, 2026 and is labelled
preliminary (reporting lag and revisions) until the first snapshot after Jan 1, 2027.

## Run the tests
```
pip install -e "ingest[test]" && (cd ingest && pytest -q)
```
## Run the live probe (needs internet access to api.usaspending.gov)
```
python -m civiclens_ingest.probe --out evidence/probe --quick
```
