# CivicLens AI — Federal Spending Intelligence & Investigation Platform

Real U.S. federal IT procurement records from [USAspending.gov](https://www.usaspending.gov), transformed on
Databricks (Bronze → Silver → Gold Delta), scored by an explainable anomaly engine, published as a versioned
read-only snapshot behind a FastAPI service and a Next.js site, with an AI investigator that answers only from
SQL it ran and cites the award ids it used.

**Status: M1–M5 built; live evidence for M1 partial (6 of 30 cells), M2 on Databricks pending, M4 eval pending, M6 deploy pending.** Nothing here is deployed yet. Every claim of
"works" in this repo is tied to a test result or a file under `evidence/`.

| Area | State | Evidence |
|---|---|---|
| USAspending client (retries, timeouts, pagination, download polling, retrying file fetch) | mock-tested, 21 tests | `ingest/tests/test_client.py` |
| Live endpoint validation | **live 2026-10-23**: 7/7 endpoints, ~119k transactions in scope, sub-award bundling found and handled | `evidence/probe/` |
| Single-cell ingest (SSA FY2026) | **live**: 235 prime rows = API count; idempotent re-run skipped the download (same run id, same sha) | `evidence/ingest/manifests/028_fy2026.json` |
| Five VA cells (FY2022–FY2026) | **live**: all exact vs API count; first full run then failed on a dropped file download (fixed, regression-tested) | `evidence/ingest/manifests/036_*.json` |
| Silver/Gold SQL (one set of files for DuckDB and Spark), DQ gate, 3 detectors, status breakdown | mock-tested, 19 tests; **run on real SSA cell**: 235→235, 0 rejects, Gold = Silver at $1,057,911,411.10, all DQ pass, detector correctly abstained (no PSC class ≥ 30 peers in one small agency-year) | `lakehouse/tests/`, local build output |
| Independent reconciliation at matching grain (R1 counts, R2 sampled award window sums vs the award's own transactions, R3 spending_over_time) | written; runs after every full pull | `evidence/reconcile/` once run |
| Databricks notebooks + job + Actions runner | written; Free Edition auth proven (SCIM 200, Jobs 200); **not yet run** (Volume pending) | `evidence/databricks/auth-proof.md` |
| API (FastAPI): overview, agency, anomalies + detail, awards, search, published SQL, health | mock-tested, 8 tests over a pipeline-built synthetic snapshot | `api/tests/test_api.py` |
| AI investigator: scoped tools, structured output, server-side fact verification, citations, injection handling, misconduct scrub, rate limits, ledger, cache | mock-tested, 7 tests with a scripted fake model; **no live model run yet** | `api/tests/test_investigator.py` |
| AI evaluation harness (40 cases, reference values computed by SQL at run time, Sonnet judge) | written; **not yet run** (needs key) | `api/civiclens_api/evaluate.py` |
| Snapshot stamping + publish (immutable release asset, DQ-gated, promote-after-release) | tested on synthetic build | `scripts/stamp_snapshot.py`, `.github/workflows/publish-snapshot.yml` |
| Website (Next.js 15, five pages, dark-first, responsive) | built; **17 Playwright e2e tests** pass on desktop + mobile Chromium incl. axe WCAG 2.1 AA, error/empty states, scope propagation | `web/tests/site.spec.ts` |
| Public deployment (Fly.io API image + Vercel site) | Dockerfile, fly.toml, vercel.json written; **not deployed** (needs approval) | |

Architecture and decisions: see `docs/M0.md` (mirrors the M0 assessment) and `docs/DECISIONS.md`.

## Scope (MVP)
Six civilian agencies (VA, DHS, HHS, Treasury, Commerce, SSA), fiscal years 2022–2026, prime contract
transactions (award types A, B, C, D) whose PSC starts with `D` (IT and telecom services) or `70` (IT
equipment and software). FY2022–FY2025 is the settled baseline; FY2026 ended Sep 30, 2026 and is labelled
preliminary (reporting lag and revisions) until the first snapshot after Jan 1, 2027.

## Run the tests
```
pip install -e "ingest[test]" -e "lakehouse[test]"
(cd ingest && pytest -q) && (cd lakehouse && PYTHONPATH=tests pytest -q)
```
## Build the local snapshot from raw cells (same SQL Databricks runs)
```
python -m civiclens_lakehouse.pipeline --raw data/raw --db build/civiclens.duckdb
```
## Run the live probe (needs internet access to api.usaspending.gov)
```
python -m civiclens_ingest.probe --out evidence/probe --quick
```
