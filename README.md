# CivicLens AI — Federal Spending Intelligence & Investigation Platform

Real U.S. federal IT procurement records from [USAspending.gov](https://www.usaspending.gov), transformed on
Databricks (Bronze → Silver → Gold Delta), scored by an explainable anomaly engine, published as a versioned
read-only snapshot behind a FastAPI service and a Next.js site, with an AI investigator that answers only from
SQL it ran and cites the award ids it used.

**Status: M1 (ingestion with verified provenance) in progress.** Nothing here is deployed yet. Every claim of
"works" in this repo is tied to a test result or a file under `evidence/`.

| Area | State | Evidence |
|---|---|---|
| USAspending client: retries, timeouts, pagination, download polling | mock-tested | `ingest/tests/test_client.py` (17 tests) |
| Worker: per agency × FY pull, provenance manifest, idempotent, atomic swap, prime-only count check | mock-tested | same |
| Live endpoint validation (schemas, counts, pagination, identifiers) | **live-validated 2026-10-23**: 7/7 endpoints, 42 calls, 0 retries; ~119k transactions in scope; found that the transaction download bundles sub-award rows (fixed in worker) | `evidence/probe/summary.md`, `evidence/probe/*.json` |
| Full MVP pull (30 cells) with per-cell manifests | workflow written; first run pending | `evidence/ingest/report.md` |
| Databricks unattended automation (Files + Jobs API from Actions) | proof workflow written, not yet run | `evidence/databricks/auth-proof.md` |
| Silver/Gold SQL (one set of files for DuckDB and Spark), DQ gate, 3 anomaly detectors | mock-tested on synthetic cells: FY boundaries, rejects accounted for, de-obligations, newest-run-wins, Gold = Silver to the cent, planted outlier flagged, small groups abstain, log-normal and Pareto flag rates bounded, concentration + growth rules, no misconduct vocabulary, deterministic | `lakehouse/tests/test_pipeline.py` (16 tests) |
| Databricks notebooks + job + Actions runner (`lakehouse-databricks`) | written, not yet run | `evidence/pipeline/databricks_run.json` |
| API, site, AI investigator, evaluation, deploy | not started (M4–M6) | |

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
