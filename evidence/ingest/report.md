# Ingestion report — 2026-10-23T17:34:16+00:00

Cells complete: **4**, failed: **0**, prime transactions: **13,559**, count mismatches: **4**

| agency | FY | status | prime rows | API count | match | sub-award rows | download job (UTC) | request | extracted | API last_updated |
|---|---|---|---|---|---|---|---|---|---|---|
| Department of the Treasury | 2023 | count_mismatch | 3,308 | 3,309 | False | 655 | 20261023T172707Z cached | split_time_period | 20261023T172705Z | 10/23/2026 |
| Department of the Treasury | 2024 | count_mismatch | 3,372 | 3,375 | False | 782 | 20261023T173015Z cached | split_time_period | 20261023T173013Z | 10/23/2026 |
| Department of the Treasury | 2025 | count_mismatch | 4,020 | 4,022 | False | 541 | 20261023T173220Z cached | split_time_period | 20261023T173218Z | 10/23/2026 |
| Department of the Treasury | 2026 | count_mismatch | 2,859 | 2,865 | False | 308 | 20261023T173335Z cached | split_time_period | 20261023T173333Z | 10/23/2026 |

`download job` is the generation time USAspending embeds in the zip name; `cached` means the API returned an earlier job for an identical request, in which case the worker re-requested with an equivalent split-window body (`request = split_time_period`) after proving both bodies count the same rows.
