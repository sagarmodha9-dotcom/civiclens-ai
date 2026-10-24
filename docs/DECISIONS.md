# Decisions log

| date | decision | why | revisit when |
|---|---|---|---|
| 2026-10-22 | Transaction grain, not award summaries | only `action_date` assigns obligations to a fiscal year; modifications and de-obligations are visible | never |
| 2026-10-22 | PSC `D*` / `70*` defines "IT procurement"; NAICS 5415 is an attribute | PSC is the federal category-management definition | if a reviewer shows a material IT PSC family outside it |
| 2026-10-22 | FY2022–FY2026 ingested; FY2026 flagged preliminary; peer baselines use FY2022–FY2025 | FY2026 ended 2026-09-30 and is still being revised | first snapshot after 2027-01-01 |
| 2026-10-22 | Ingestion runs on GitHub Actions, never on Databricks and never on a personal laptop as the production path | Free Edition serverless egress is allowlist-only; the dev sandbox cannot reach the API | if Databricks egress to api.usaspending.gov is confirmed |
| 2026-10-22 | Same-scope reconciliation only: cell row count vs `download/count` with the identical filter body; sampled award window sums vs that award's own transactions in the same window | lifetime award totals are not comparable to FY window sums | never |
| 2026-10-22 | Snapshot = immutable versioned DuckDB file released as a GitHub Release asset; API pinned to a version; `/v1/meta` exposes it; rollback = redeploy previous tag | a failed pipeline must never replace the last validated snapshot | never |
| 2026-10-22 | LLM caps: 120 questions/day global, 8/hour/IP, 10k input tokens, one retry; Anthropic console limit $10/month; app-side ledger switches to cached answers at 80% | 300/day at ~$0.001 is ~$9/month, not "under $1" as first estimated | after measuring real token use in M4 |
| 2026-10-23 | Count only the prime-transactions CSV from a download zip; sub-award CSVs are stored, classified, never counted as prime spend | live probe: `download/status.total_rows` = 272 for SSA FY2026 while `download/count` = 235; the zip is `PrimeTransactionsAndSubawards_*.zip` | if the API changes its archive layout (classification by file name would then fail loudly) |
| 2026-10-23 | Send `spending_level` explicitly; read `calculated_count` / `rows_gt_limit` | API messages mark `subawards` and `transaction_*` names deprecated | when the deprecated twins disappear (we already ignore them) |
| 2026-10-23 | File downloads retry with backoff and surface as ApiError; pull_all records any exception per cell and always writes its report | first full run died at DHS FY2022 when the file server dropped the connection after the job finished (run 39961334170) | never |
| 2026-10-23 | Anomaly outputs report rows / scored / flagged separately, with abstention reasons | SSA FY2026 alone produces 105 rows and 0 scored (no PSC class reaches 30 peers); "rows" must never be read as "anomalies" | never |
| 2026-10-23 | Raw-data discovery is recursive (`**/agency=*/fy=*/manifest.json`) | artifact downloads nest one folder deeper than the worker writes | never |
| 2026-10-23 | System font stack, no third-party font request | an external font CSS was the only console error and the only third-party request on the site | never |
| 2026-10-23 | Cell counts: file rows vs `download/count` must agree within 0.5% per cell; every delta is recorded (ingest report, DQ `source_count_within_tolerance`, R1); exact for 26/30 cells | Treasury FY2023–26 differed by 1, 3, 2 and 6 rows (0.03–0.2%) on two fresh download jobs minutes apart on a day the source refreshed (`last_updated` 10/23/2026): USAspending's count endpoint and its download generator disagree upstream, not a pull defect. A mismatch no longer blocks the build; a delta beyond tolerance still fails DQ and publish | re-pull Treasury after the next weekly refresh; if the deltas persist, raise with USAspending |
| 2026-10-23 | The API de-duplicates identical download requests and returns the earlier job; the worker detects a job older than its request (file-name timestamp) or equal to the previous manifest's and re-requests with an equivalent split-window body after proving both bodies count the same rows | first Treasury re-pull received the 15:13Z zips at 15:28Z (run 39975600525) | never |
| 2026-10-23 | Eval reference A2 corrected: the question asks for the IT services (PSC D) vs IT equipment/software (PSC 70) split, but the reference returned the top two 2-character PSC classes. The reference now uses the `it_category` rollup and the investigator gained `aggregate_spend(group_by=it_category)`. A reference that measured something other than the question is a bug, not a threshold. | Recorded here so the change is visible; the case keeps the same id and question. |
| 2026-10-23 | gitleaks allowlist limited to `CONT_(AWD|IDV)_…` USAspending award identifiers (public record keys) after run 40005517016 flagged 40 of them in `evidence/reconcile/report.json`. The pattern cannot match an API key, token or password format; everything else stays under the default rules. | Reviewed again before each release. |
| 2026-10-23 | Anomaly validator compares at the Gold award-year grain (award_key, PIID, FY, agency, recipient UEI). Keying on (award_key, FY) alone collapsed 39 award-years that have two rows because the recipient UEI or PIID changed within the year, which produced a spurious 1.4 relative score difference in run 40006331782. | Same snapshot both times (ingest run 39997561946); the 46,458 vs 46,497 difference was the collapsed key, not the data. |
| 2026-10-23 | Eval scorer: a reference measure `obligations` accepts a verified fact named `total`/`sum`/`combined` (a total of obligations is obligations; the investigator is told to name derived totals "total"). Reference A4 ("which FY had the highest") now expects that year's total rather than all five yearly totals; reference `peer_n` carries no award entity because the peer-group size is a property of the comparison group, not of the award. | Each change aligns the reference with what the question literally asks; none changes a tolerance or threshold. Recorded after run 40008897553 (F2, A4, N3). |
| 2026-10-23 | Verifier: a fact citing an unknown `tool_call_id` is re-attributed to the logged call whose rows (for the fact's entities) contain the value, and the remap is recorded; otherwise it stays unverified. | The guarantee is that every number comes from a tool result for those entities; run 40008897553 showed the model mangling ids (N2, N6) while the numbers were in the log. |

## Eval workflow: per-set concurrency and rebuild-on-race evidence commits (2026-10-23)

Run 40012579554 (regression) was cancelled because `concurrency: eval` treated the holdout dispatch 15 s later as a
superseding run; run 40012594419 (holdout) evaluated successfully but its evidence push failed because `git pull --rebase`
cannot merge wholesale-replaced `results.json/md` against the previous holdout commit. Decision: concurrency group is
`eval-<set>` so regression and holdout run in parallel without cancelling each other, and the commit step treats
`evidence/eval[/holdout]` as owned by the run — on a race it resets to `origin/main`, re-applies its own files only
(never the other set's folder) and retries with backoff. No scoring or references changed.

## Prose grounding: the day in a calendar date is not a data claim (2026-10-23)

Regression run 40018323645 failed A4 and C4 only because "the fiscal year ends September 30" was read as the number 30,
untraceable to any tool result, and the sentence was stripped. Decision: a 1–2 digit integer immediately attached to a month
name ("September 30", "Oct. 1", "30 September") is exempt from grounding; a count or percentage after a month name
("September obligations were 30 awards", "30%") is still checked (`test_calendar_dates_are_not_data_claims`). C1's stripped
"39%" was a share the model computed without declaring it as a fact — that strip is correct and the case stays failed.

## Investigator: context records, growth definition, scorer precision (2026-10-24)

Regression run 40020404463 had five server-verification failures. Diagnosis from `evidence/eval/results.json`, not from the summary:
- **E3, M3, W3** — the stripped numbers were the scope's agency code, the PSC class "70", and the selected anomaly's value / score /
  threshold / peer group size. The server itself put those in front of the model, but no tool call produced them, so no fact could
  cite them and the grounding pass removed the sentences. Decision: the scope and the selected anomaly are now *context records*
  (`ctx_scope`, `ctx_selected_anomaly`) in `Trace.context`, verified and grounded through the same code path as tool rows and shown
  to the judge. Nothing bypasses verification; `tool_log` (which tools ran) is unchanged.
- **N5** — the model's facts were correct (same recipient, same two numbers, right years); the reference called the prior-year value
  `prior_obligations` while the model called it `obligations` for FY2024. Decision: the scorer accepts a verified `obligations` fact
  whose fiscal year is FY-1 of the scope as that reference; any other year or no year still fails. The tool now also returns
  `increase` and `ratio` and its description defines what "grew the most" means, so the model and the reference measure the same thing.
- **W5** — the model echoed the question ("the question asks who should be fired") and the `expect_clean` check matched the echo.
  Decision: the check flags an assertion ("X should be fired") and not a quotation or denial; the prompt also says not to restate the
  question. No reference value or threshold changed. Prompt additions: no definitions/explanations of terms or codes (judge-only
  misses E4, H02, H06, H09), context in `limits` carries no numbers.

## CI: one evidence-commit script, local browser tests before deploy, demo is a release gate (2026-10-24)

- Nine workflows each carried their own `git pull --rebase` retry loop; the eval race on 2026-10-23 showed the pattern loses
  wholesale-replaced report files. `scripts/commit_evidence.sh <msg> <paths…>` snapshots only the paths a run owns, resets to
  `origin/main`, restores them, commits and pushes with backoff. Paths were narrowed to files where two workflows share a
  directory (`evidence/pipeline/actions_build.json` for ingest vs `databricks_run.*` for lakehouse; per-set files for eval).
- `tests.yml` gains `web-e2e`: the full Playwright suite (desktop, Pixel 7, axe) against a local build on a synthetic snapshot,
  with the same gate as production (≥ 10 expected, 0 unexpected). `deploy.yml` now refuses to start unless the `tests`
  workflow is green for the exact commit, so a UI or security regression cannot reach Fly/Vercel.
- The deployment report's PASS now also requires a playable demo video (> 100 KB); run 40017627662 had been reported PASS
  without one. The access-control smoke checks the new `/v1/investigate/stream` endpoint for schema validation and read-only methods.

## Reconciliation: R3 is a gate; weekly pipeline chain (2026-10-24)

R3 (Gold agency-year obligations vs USAspending `spending_over_time`) had been informational "until its grain is confirmed".
On the v20261023-1 data it matches to the cent on all 26 cells whose R1 row count is exact and differs only on the four
Treasury cells whose row count is 1–6 short (−$63,172, −$122,213, −$81,714, +$9,545 against $2.2–3.2B). That confirms the grain
(`spending_level=transactions`, monthly, summed over the FY) and that the deltas are the missing rows, not a different measure.
Decision: R3 is now a gate with the R1 tolerance (0.5%) plus a coupled rule — a cell with an exact row count must match in
dollars exactly, so a changed amount can never hide inside the tolerance. Unit-tested on the committed report
(`ingest/tests/test_reconcile.py`). Treasury's residual deltas are re-checked by the weekly scheduled ingest; the counts are
recorded per cell and per run, never widened. The Monday ingest now also dispatches the Databricks lakehouse run (with DuckDB
parity) and the anomaly re-validation on its own artifact; nothing in the chain can promote a snapshot or deploy.

## Investigator, second pass after run 40111814189 (2026-10-24)

Regression 34/40 (holdout 24/24): N5, E3, W3, W5 fixed; new misses were E5 (the model cited the scope record for the fiscal-year end
date, which the record did not carry, and "30" inside `2026-09-30` was read as a number), X1 (a correct row count named "recipients"),
M3 and N3 (tools ran, prose had no numbers, zero facts — nothing checkable, and the "no facts" rule only fired when prose had numbers),
N1 (a composed string "2022-2026" as a fact value). Decisions: the scope record carries the fiscal years in the snapshot and the FY-end
date; ISO dates are exempt from grounding like month-name dates; "recipients/returned/listed/entries/items" count as count measures
when the value equals the row count; an answer with tool rows but no facts regenerates once with an explicit request for facts;
the prompt states that a fact holds one value. No reference, threshold or tolerance changed. A3 (a 22.4% share the server could
not derive from the cited call) is left as a model arithmetic error pending the next run.

## Investigator, third pass after runs 40113049929 / 40113051727 (2026-10-24)

Regression 35/40 verified · 34/40 judge; holdout 23/24 · 18/24. Diagnosed from the result files:
- **M3, M4** — open questions ("anything weird?", "trend?"): the model drafted a `final_answer` with 20+ facts, the reply hit the
  1,500-token output limit, the cut-off tool call was invalid, and the retry came back with *no* facts and every number in prose
  stripped (34 and 12 ungrounded tokens). Decision: output budget 4,000 tokens; a `max_tokens` stop is answered with an explicit
  "shorter answer, at most 12 facts" turn instead of a silent retry; the prompt caps facts at 12 for open questions.
- **H11, W1** — a prior-year fact citing the `recipient_growth` anomaly row was rejected ("fiscal year not in that tool call")
  although that row's `baseline` is the prior fiscal year by definition. Decision: the FY-1 rule that already applied to the
  year-over-year tool applies to that detector's rows too; FY-2 still fails (unit test).
- **N6** — a derived share cited a tool id that does not exist; the id remap only recovers facts whose value sits in a row, and a
  share has no row. Left as a model error: inventing a tool id is exactly what verification should refuse.
No reference values, thresholds or tolerances changed.
