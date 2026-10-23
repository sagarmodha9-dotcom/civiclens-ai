# CivicLens AI — M1–M8 acceptance report

Release commit `e24b1a2` · snapshot `v20261023-1` (sha256 `7c3de72f32bf341ed57d10b6f3c817acde2ff2376a887ffd53556b4eeebbac1f`, 63,713,280 bytes,
built 2026-10-23T17:45:22Z from ingest run 39997561946) · report date 2026-10-23.

Status vocabulary: **BUILT** (code and unit tests exist) · **MOCK-TESTED** (tested on synthetic data) · **LIVE-TESTED** (run
against the real service / real data with evidence) · **PASS** / **FAIL** (gate result on the release snapshot) · **NOT VERIFIED**.

## Decision: **GO** — every milestone LIVE-TESTED · PASS on snapshot `v20261023-1` at commit `e24b1a2`; limitations below are documented, none blocks public use.

## Matrix

| # | Milestone | Status | Evidence (run id · commit · result) | Limitations |
|---|---|---|---|---|
| M1 | Ingest 30 agency×FY cells from USAspending; manifests; independent reconciliation | **LIVE-TESTED · PASS** | ingest run [39997561946](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/39997561946) · commit 38bb638 · 30/30 cells complete, 109,883 prime transactions; R1 26/30 exact, worst delta 0.21% (≤ 0.5%); R2 50/50 sampled awards exact to the cent; R3 30 available, 4 non-zero deltas (informational) · `evidence/ingest/report.md`, `evidence/reconcile/report.md` | Treasury FY2023–26 counts differ from the API count endpoint by 1–6 rows on a refresh day (two fresh download jobs minutes apart); recorded per cell. |
| M2 | Bronze/Silver/Gold on Databricks serverless (Delta, Unity Catalog); cross-engine parity | **LIVE-TESTED · PASS** | lakehouse run [40005551673](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/40005551673) · commit 5a45d15 · Databricks job 862977884764769 run 577799826358384 (link in report) · serverless env client 3, package as wheel on Volume · bronze 109,883 = silver 109,883, rejects 0, Σ obligations $109,830,250,044.05 = Gold, flagged 157 / scored 45,044 — all equal to DuckDB · `evidence/pipeline/databricks_run.md` | Free Edition cannot create catalogs (uses `workspace`); Workspace-file imports are unreliable on serverless, hence the wheel. |
| M3 | Anomaly engine validated independently on real data; six anomaly eval scenarios | **LIVE-TESTED · PASS** | validate run [40008893734](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/40008893734) · commit 015d267 · NumPy re-implementation: 46,497 / 359 / 21,017 rows compared, flagged sets identical (157 / 94 / 219), max relative score diff 0.0 / 6.7e-16 / 0.0; 14 sampled flagged records traced to raw rows to the cent with USAspending permalinks · `evidence/anomalies/validation.md`; eval anomaly category: 4/6 server-verified in run 40020404463 (N5 failed numerically, N6 passed verification but not the judge); holdout anomaly 3/3 | Concentration flags include single-recipient cells (HHI 10,000) — expected for sole-source categories and stated on the Methodology page. |
| M4 | AI investigator: 40-case regression + 24-case independent holdout; grounding, citations, refusals, safety | **LIVE-TESTED · PASS** | regression run [[40020404463](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/40020404463)] · commit e24b1a2 · 35/40 server-verified · 32/40 +judge · numeric 20/21 · citation failures 0 · misconduct language 0 · $0.63 · `evidence/eval/results.md`; holdout run [[40020407844](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/40020407844)] · 24/24 server-verified · 19/24 +judge · numeric 12/12 · citation failures 0 · $0.32 (never used for tuning) · `evidence/eval/holdout/results.md` | Regression misses: N5 (fastest-growing recipient: model picked a different growth basis), E3/M3/W3 (a sentence with an untraceable number was stripped, leaving the answer short of a reference or with a flagged phrase), W5 (declined with insufficient evidence where a measured answer existed). Judge-only misses are explanatory sentences (e.g. 'outlays are cash paid out') the judge treats as unsupported; the server column is the provable one. |
| M5 | Website on validated data; desktop + mobile; empty/loading/error states | **LIVE-TESTED · PASS** | e2e in deploy run [[40020401068](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/40020401068)]: 17 passed, 0 failed, 1 skipped (demo spec) on desktop Chrome + Pixel 7 incl. axe WCAG 2.1 AA; empty, loading and error states covered · screenshots `docs/screenshots/` | |
| M6 | Public deployment: FastAPI on Fly.io, Next.js on Vercel, pinned snapshot | **LIVE-TESTED · PASS** | deploy run [[40020401068](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/40020401068)] · API https://civiclens-api.fly.dev (`/healthz` snapshot `v20261023-1`, DQ pass; `X-Snapshot-Version` header) · site https://civiclens-ai-smoky.vercel.app · `evidence/deploy/report.md` | |
| M7 | Tests: unit/integration (ingest 26, lakehouse 23, api 65), security gate (gitleaks history, pip-audit, npm audit), live access-control smoke, live browser tests | **LIVE-TESTED · PASS** | tests run [40020378630](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/40020378630) (security gate PASS: gitleaks 0, pip-audit 0, npm audit 0 prod vulns) · `evidence/security/report.md`; live API access checks in deploy report | gitleaks allowlist limited to public `CONT_AWD_…` award ids (DECISIONS.md). |
| M8 | README, architecture, screenshots, demo recording, acceptance matrix, costs | **PASS** | `README.md`, `docs/architecture.svg`, `docs/demo/civiclens-demo.mp4`, `docs/screenshots/`, this file | |

## Costs (monthly, as configured)

| Item | Cost | Control |
|---|---|---|
| Fly.io `civiclens-api`, shared-cpu-1x 512 MB always-on + 1 GB volume | ≈ $3–5 | approved ceiling $5; single machine, `--ha=false` |
| Vercel Hobby | $0 | — |
| Databricks Free Edition | $0 | serverless only |
| Anthropic API | ≤ $10 cap in console; app budget $5 (`CIVICLENS_MONTHLY_BUDGET_USD`) | per-IP 8/hour, global 120/day, cached answers after budget; a full eval ≈ $0.65, holdout ≈ $0.35 |
| GitHub Actions | $0 (public repo) | — |

## Unresolved limitations

- Treasury FY2023–FY2026 cell counts differ from the API count endpoint by 1–6 rows (≤ 0.21%, tolerance 0.5%) on the refresh day; recorded per cell.
- FY2026 is preliminary and will be revised by USAspending; labelled as such everywhere.
- Investigator: 5/40 regression cases still fail server verification (listed in M4); the LLM judge disagrees on explanatory prose in 8 more. Next fixes are investigator behaviour, not scoring.
- Live Claude answers take 10–40 s; the UI shows progress and the e2e test allows 90 s.
- Databricks Free Edition: no custom catalog (uses `workspace`), serverless only; job runs are re-created per release.
- Fly.io single machine (`--ha=false`) to stay within the approved $5/month; a redeploy causes ~30 s of downtime.
- The demo video is recorded automatically by Playwright against the public site; it has no narration.

## Evidence index

- `evidence/ingest/` · `evidence/reconcile/` · `evidence/pipeline/` (DuckDB build + Databricks run) · `evidence/anomalies/` · `evidence/eval/` (+ `holdout/`) · `evidence/security/` · `evidence/deploy/` · `evidence/databricks/` (preflight) · `evidence/probe/`
- Every report carries the GitHub run id, commit, UTC time and PASS/FAIL; failed runs are kept in git history, not overwritten.
