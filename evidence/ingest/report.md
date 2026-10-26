# Ingestion report — 2026-10-26T17:05:33+00:00

Cells in data set: **30** (pulled or re-checked this run: 30), failed: **0**, prime transactions: **109,885**, count mismatches: **4**

| agency | FY | status | prime rows | API count | match | sub-award rows | download job (UTC) | request | extracted | API last_updated |
|---|---|---|---|---|---|---|---|---|---|---|
| Department of Veterans Affairs | 2022 | complete | 5,197 | 5,197 | True | 1214 | 20261026T161123Z | standard | 20261026T161122Z | 10/26/2026 |
| Department of Veterans Affairs | 2023 | complete | 4,270 | 4,270 | True | 679 | 20261026T161423Z | standard | 20261026T161422Z | 10/26/2026 |
| Department of Veterans Affairs | 2024 | complete | 3,974 | 3,974 | True | 856 | 20261026T161620Z | standard | 20261026T161619Z | 10/26/2026 |
| Department of Veterans Affairs | 2025 | complete | 3,919 | 3,919 | True | 536 | 20261026T161838Z | standard | 20261026T161837Z | 10/26/2026 |
| Department of Veterans Affairs | 2026 | complete | 4,385 | 4,385 | True | 385 | 20261026T162015Z | standard | 20261026T162014Z | 10/26/2026 |
| Department of Homeland Security | 2022 | complete | 8,020 | 8,020 | True | 1076 | 20261026T162144Z | standard | 20261026T162142Z | 10/26/2026 |
| Department of Homeland Security | 2023 | complete | 6,654 | 6,654 | True | 987 | 20261026T162455Z | standard | 20261026T162454Z | 10/26/2026 |
| Department of Homeland Security | 2024 | complete | 5,502 | 5,502 | True | 952 | 20261026T162754Z | standard | 20261026T162753Z | 10/26/2026 |
| Department of Homeland Security | 2025 | complete | 5,040 | 5,040 | True | 707 | 20261026T163117Z | standard | 20261026T163113Z | 10/26/2026 |
| Department of Homeland Security | 2026 | complete | 4,449 | 4,449 | True | 592 | 20261026T163345Z | standard | 20261026T163344Z | 10/26/2026 |
| Department of Health and Human Services | 2022 | complete | 5,944 | 5,944 | True | 1291 | 20261026T163552Z | standard | 20261026T163551Z | 10/26/2026 |
| Department of Health and Human Services | 2023 | complete | 5,465 | 5,465 | True | 1417 | 20261026T163841Z | standard | 20261026T163840Z | 10/26/2026 |
| Department of Health and Human Services | 2024 | complete | 4,841 | 4,841 | True | 998 | 20261026T164202Z | standard | 20261026T164201Z | 10/26/2026 |
| Department of Health and Human Services | 2025 | complete | 4,310 | 4,310 | True | 592 | 20261026T164512Z | standard | 20261026T164511Z | 10/26/2026 |
| Department of Health and Human Services | 2026 | complete | 3,743 | 3,743 | True | 541 | 20261026T164658Z | standard | 20261026T164657Z | 10/26/2026 |
| Department of the Treasury | 2022 | complete | 3,822 | 3,822 | True | 661 | 20261026T164814Z | standard | 20261026T164813Z | 10/26/2026 |
| Department of the Treasury | 2023 | count_mismatch | 3,308 | 3,309 | False | 655 | 20261026T164950Z | standard | 20261026T164949Z | 10/26/2026 |
| Department of the Treasury | 2024 | count_mismatch | 3,372 | 3,375 | False | 784 | 20261026T165137Z | standard | 20261026T165136Z | 10/26/2026 |
| Department of the Treasury | 2025 | count_mismatch | 4,020 | 4,022 | False | 541 | 20261026T165344Z | standard | 20261026T165343Z | 10/26/2026 |
| Department of the Treasury | 2026 | count_mismatch | 2,859 | 2,865 | False | 313 | 20261026T165613Z | standard | 20261026T165612Z | 10/26/2026 |
| Department of Commerce | 2022 | complete | 3,898 | 3,898 | True | 403 | 20261026T165707Z | standard | 20261026T165706Z | 10/26/2026 |
| Department of Commerce | 2023 | complete | 3,463 | 3,463 | True | 497 | 20261026T165802Z | standard | 20261026T165801Z | 10/26/2026 |
| Department of Commerce | 2024 | complete | 2,907 | 2,907 | True | 448 | 20261026T165938Z | standard | 20261026T165937Z | 10/26/2026 |
| Department of Commerce | 2025 | complete | 2,638 | 2,638 | True | 359 | 20261026T170046Z | standard | 20261026T170045Z | 10/26/2026 |
| Department of Commerce | 2026 | complete | 2,152 | 2,152 | True | 265 | 20261026T170211Z | standard | 20261026T170210Z | 10/26/2026 |
| Social Security Administration | 2022 | complete | 438 | 438 | True | 84 | 20261026T170255Z | standard | 20261026T170254Z | 10/26/2026 |
| Social Security Administration | 2023 | complete | 378 | 378 | True | 108 | 20261026T170330Z | standard | 20261026T170329Z | 10/26/2026 |
| Social Security Administration | 2024 | complete | 369 | 369 | True | 35 | 20261026T170403Z | standard | 20261026T170402Z | 10/26/2026 |
| Social Security Administration | 2025 | complete | 313 | 313 | True | 28 | 20261026T170437Z | standard | 20261026T170436Z | 10/26/2026 |
| Social Security Administration | 2026 | complete | 235 | 235 | True | 37 | 20261026T170501Z | standard | 20261026T170500Z | 10/26/2026 |

`download job` is the generation time USAspending embeds in the zip name; `cached` means the API returned an earlier job for an identical request, in which case the worker re-requested with an equivalent split-window body (`request = split_time_period`) after proving both bodies count the same rows.
