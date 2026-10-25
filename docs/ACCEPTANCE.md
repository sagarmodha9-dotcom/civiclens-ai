# CivicLens AI — M1–M8 acceptance report

Release commit `7a2d939` · snapshot `v20261023-1` (sha256 `7c3de72f32bf341ed57d10b6f3c817acde2ff2376a887ffd53556b4eeebbac1f`, 63,713,280 bytes,
built 2026-10-23T17:45:22Z from ingest run 39997561946) · report date 2026-10-25 (first issued 2026-10-23).

Status vocabulary: **BUILT** (code and unit tests exist) · **MOCK-TESTED** (tested on synthetic data) · **LIVE-TESTED** (run
against the real service / real data with evidence) · **PASS** / **FAIL** (gate result on the release snapshot) · **NOT VERIFIED**.

## Decision: **GO** — every milestone LIVE-TESTED · PASS on snapshot `v20261023-1` at release commit `7a2d939` (deploy [40115580863](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/40115580863)); limitations below are documented, none blocks public use.

## Matrix

| # | Milestone | Status | Evidence (run id · commit · result) | Limitations |
|---|---|---|---|---|
| M1 | Ingest 30 agency×FY cells from USAspending; manifests; independent reconciliation | **LIVE-TESTED · PASS** | ingest run [39997561946](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/39997561946) · commit 38bb638 · 30/30 cells complete, 109,883 prime transactions; R1 26/30 exact, worst delta 0.21% (≤ 0.5%); R2 50/50 sampled awards exact to the cent; R3 30 available, 4 non-zero deltas (informational) · `evidence/ingest/report.md`, `evidence/reconcile/report.md` | Treasury FY2023–26 counts differ from the API count endpoint by 1–6 rows on a refresh day (two fresh download jobs minutes apart); recorded per cell. |
| M2 | Bronze/Silver/Gold on Databricks serverless (Delta, Unity Catalog); cross-engine parity | **LIVE-TESTED · PASS** | lakehouse run [40005551673](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/40005551673) · commit 5a45d15 · Databricks job 862977884764769 run 577799826358384 (link in report) · serverless env client 3, package as wheel on Volume · bronze 109,883 = silver 109,883, rejects 0, Σ obligations $109,830,250,044.05 = Gold, flagged 157 / scored 45,044 — all equal to DuckDB · `evidence/pipeline/databricks_run.md` | Free Edition cannot create catalogs (uses `workspace`); Workspace-file imports are unreliable on serverless, hence the wheel. |
| M3 | Anomaly engine validated independently on real data; six anomaly eval scenarios | **LIVE-TESTED · PASS** | validate run [40008893734](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/40008893734) · commit 015d267 · NumPy re-implementation: 46,497 / 359 / 21,017 rows compared, flagged sets identical (157 / 94 / 219), max relative score diff 0.0 / 6.7e-16 / 0.0; 14 sampled flagged records traced to raw rows to the cent with USAspending permalinks · `evidence/anomalies/validation.md`; eval anomaly category: 4/6 server-verified in run 40020404463 (N5 failed numerically, N6 passed verification but not the judge); holdout anomaly 3/3 | Concentration flags include single-recipient cells (HHI 10,000) — expected for sole-source categories and stated on the Methodology page. |
| M4 | AI investigator: 40-case regression + 24-case independent holdout; grounding, citations, refusals, safety | **LIVE-TESTED · PASS** | regression [40115576951](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/40115576951) · 36/40 server-verified · 32/40 +judge · numeric 17/21 · citation failures 0 · misconduct 0 · $0.70; holdout [40115578916](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/40115578916) · 23/24 server-verified · 20/24 +judge · numeric 12/12 · citation failures 0 · $0.32; four-run range 34–36/40 and 23–24/24 (README § Evaluation honesty) | Remaining misses vary run to run: over-cautious refusals (N1, X2 in the release run), growth answered on another basis (N5), partial trend answer (M4); holdout H14 declared facts on a refusal. Judge-only misses are explanatory phrases. |
| M5 | Website on validated data; desktop + mobile; empty/loading/error states | **LIVE-TESTED · PASS** | deploy [40115580863](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/40115580863): 21 passed, 0 failed, 1 skipped (demo spec) on desktop Chrome + Pixel 7 incl. axe WCAG 2.1 AA; also on every push against a local build (`tests.yml` web-e2e). New: streamed, truthful investigator progress; cached/paused notices; overview explainer · `docs/screenshots/` | |
| M6 | Public deployment: FastAPI on Fly.io, Next.js on Vercel, pinned snapshot | **LIVE-TESTED · PASS** | deploy [40115580863](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/40115580863) · commit 7a2d939 · API https://civiclens-api.fly.dev (`/healthz` snapshot `v20261023-1`, DQ pass) · site https://civiclens-ai-smoky.vercel.app · access-control smoke 10/10 incl. `/v1/investigate/stream` · deploy refuses to start unless `tests` is green for the commit | single Fly machine (~30 s redeploy gap) |
| M7 | Tests: unit/integration (ingest 29, lakehouse 23, api 76), local browser tests on every push, security gate (gitleaks full history, pip-audit, npm audit), live access-control smoke | **LIVE-TESTED · PASS** | tests [40115565245](https://github.com/sagarmodha9-dotcom/civiclens-ai/actions/runs/40115565245) (security PASS: gitleaks 0 findings, pip-audit 0, npm audit 0 production vulnerabilities) · `evidence/security/report.md` · R3 reconciliation now a gate (`ingest/tests/test_reconcile.py`) | gitleaks allowlist limited to public `CONT_AWD_…` award ids (DECISIONS.md). |
| M8 | README, architecture, screenshots, demo recording, acceptance matrix, costs | **PASS** | `README.md` (recruiter opening, screenshots, GIF preview), `docs/architecture.svg`, `docs/demo/civiclens-demo.mp4` (77 s, captioned from recorded chapters), `docs/screenshots/`, this file | demo has captions, no narration |

## Costs (monthly, as configured)

| Item | Cost | Control |
|---|---|---|
| Fly.io `civiclens-api`, shared-cpu-1x 512 MB always-on + 1 GB volume | ≈ $3–5 | approved ceiling $5; single machine, `--ha=false` |
| Vercel Hobby | $0 | — |
| Databricks Free Edition | $0 | serverless only |
| Anthropic API | ≤ $10 cap in console; app budget $5 (`CIVICLENS_MONTHLY_BUDGET_USD`) | per-IP 8/hour, global 120/day, cached answers after budget; a full eval ≈ $0.65, holdout ≈ $0.35 |
| GitHub Actions | $0 (public repo) | — |

## Unresolved limitations (ranked)

1. **Investigator run-to-run variance.** 34–36/40 regression and 23–24/24 holdout server-verified across four runs; failing cases move
   (over-cautious refusals, a growth question answered on another basis, a partial trend answer). Wrong numbers are not shown — the
   verifier strips or flags them — so the failure mode is an incomplete answer, not a false one.
2. **LLM judge disagreements** on 6–8 regression and 4–6 holdout cases, almost all explanatory phrasing ("reflects…", "stable");
   reported separately because the judge is a second model's opinion.
3. **Live answers take 10–40 s** (Claude Haiku tool loop + verification); the UI streams real progress steps, rate limits protect a
   fixed monthly budget, repeated questions are served from cache and labelled.
4. **Treasury FY2023–FY2026** row counts are 1–6 short of the API count (≤ 0.21%, tolerance 0.5%); the R3 dollar deltas sit only on
   those cells (coupled-exactness gate). Re-checked by the weekly scheduled ingest; never widened.
5. **FY2026 is preliminary** and will be revised by USAspending.
6. **Platform limits:** Databricks Free Edition (no custom catalog; serverless only); one Fly machine (~30 s redeploy gap).
7. The weekly chain (ingest → Databricks + parity → anomaly re-validation) writes evidence only; publishing a new snapshot is a
   manual release decision by design.

## Evidence index

- `evidence/ingest/` · `evidence/reconcile/` · `evidence/pipeline/` (DuckDB build + Databricks run) · `evidence/anomalies/` · `evidence/eval/` (+ `holdout/`) · `evidence/security/` · `evidence/deploy/` · `evidence/databricks/` (preflight) · `evidence/probe/`
- Every report carries the GitHub run id, commit, UTC time and PASS/FAIL; failed runs are kept in git history, not overwritten.
