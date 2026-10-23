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
