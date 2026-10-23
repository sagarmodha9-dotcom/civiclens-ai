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
