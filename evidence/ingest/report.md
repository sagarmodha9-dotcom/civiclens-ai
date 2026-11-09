# Ingestion report — 2026-11-09T20:40:39+00:00

Cells in data set: **30** (pulled or re-checked this run: 30), failed: **0**, prime transactions: **109,883**, count mismatches: **4**

| agency | FY | status | prime rows | API count | match | sub-award rows | download job (UTC) | request | extracted | API last_updated |
|---|---|---|---|---|---|---|---|---|---|---|
| Department of Veterans Affairs | 2022 | complete | 5,197 | 5,197 | True | 1214 | 20261109T195339Z | standard | 20261109T195338Z | 11/06/2026 |
| Department of Veterans Affairs | 2023 | complete | 4,268 | 4,268 | True | 679 | 20261109T195536Z | standard | 20261109T195535Z | 11/06/2026 |
| Department of Veterans Affairs | 2024 | complete | 3,970 | 3,970 | True | 856 | 20261109T195702Z | standard | 20261109T195701Z | 11/06/2026 |
| Department of Veterans Affairs | 2025 | complete | 3,917 | 3,917 | True | 536 | 20261109T195901Z | standard | 20261109T195900Z | 11/06/2026 |
| Department of Veterans Affairs | 2026 | complete | 4,380 | 4,380 | True | 387 | 20261109T200031Z | standard | 20261109T200028Z | 11/06/2026 |
| Department of Homeland Security | 2022 | complete | 8,020 | 8,020 | True | 1076 | 20261109T200130Z | standard | 20261109T200126Z | 11/06/2026 |
| Department of Homeland Security | 2023 | complete | 6,654 | 6,654 | True | 987 | 20261109T200358Z | standard | 20261109T200357Z | 11/06/2026 |
| Department of Homeland Security | 2024 | complete | 5,502 | 5,502 | True | 952 | 20261109T200606Z | standard | 20261109T200605Z | 11/06/2026 |
| Department of Homeland Security | 2025 | complete | 5,042 | 5,042 | True | 708 | 20261109T200844Z | standard | 20261109T200843Z | 11/06/2026 |
| Department of Homeland Security | 2026 | complete | 4,451 | 4,451 | True | 648 | 20261109T201052Z | standard | 20261109T201051Z | 11/06/2026 |
| Department of Health and Human Services | 2022 | complete | 5,944 | 5,944 | True | 1300 | 20261109T201239Z | standard | 20261109T201237Z | 11/06/2026 |
| Department of Health and Human Services | 2023 | complete | 5,465 | 5,465 | True | 1419 | 20261109T201529Z | standard | 20261109T201528Z | 11/06/2026 |
| Department of Health and Human Services | 2024 | complete | 4,842 | 4,842 | True | 998 | 20261109T201828Z | standard | 20261109T201827Z | 11/06/2026 |
| Department of Health and Human Services | 2025 | complete | 4,310 | 4,310 | True | 591 | 20261109T202007Z | standard | 20261109T202006Z | 11/06/2026 |
| Department of Health and Human Services | 2026 | complete | 3,743 | 3,743 | True | 571 | 20261109T202144Z | standard | 20261109T202143Z | 11/06/2026 |
| Department of the Treasury | 2022 | complete | 3,822 | 3,822 | True | 657 | 20261109T202321Z | standard | 20261109T202320Z | 11/06/2026 |
| Department of the Treasury | 2023 | count_mismatch | 3,308 | 3,309 | False | 655 | 20261109T202448Z | standard | 20261109T202446Z | 11/06/2026 |
| Department of the Treasury | 2024 | count_mismatch | 3,372 | 3,375 | False | 782 | 20261109T202614Z | standard | 20261109T202613Z | 11/06/2026 |
| Department of the Treasury | 2025 | count_mismatch | 4,020 | 4,022 | False | 542 | 20261109T202740Z | standard | 20261109T202739Z | 11/06/2026 |
| Department of the Treasury | 2026 | count_mismatch | 2,865 | 2,871 | False | 322 | 20261109T203051Z | standard | 20261109T203048Z | 11/06/2026 |
| Department of Commerce | 2022 | complete | 3,898 | 3,898 | True | 403 | 20261109T203209Z | standard | 20261109T203208Z | 11/06/2026 |
| Department of Commerce | 2023 | complete | 3,463 | 3,463 | True | 498 | 20261109T203426Z | standard | 20261109T203425Z | 11/06/2026 |
| Department of Commerce | 2024 | complete | 2,907 | 2,907 | True | 448 | 20261109T203542Z | standard | 20261109T203541Z | 11/06/2026 |
| Department of Commerce | 2025 | complete | 2,638 | 2,638 | True | 358 | 20261109T203646Z | standard | 20261109T203645Z | 11/06/2026 |
| Department of Commerce | 2026 | complete | 2,152 | 2,152 | True | 279 | 20261109T203751Z | standard | 20261109T203750Z | 11/06/2026 |
| Social Security Administration | 2022 | complete | 438 | 438 | True | 84 | 20261109T203835Z | standard | 20261109T203834Z | 11/06/2026 |
| Social Security Administration | 2023 | complete | 378 | 378 | True | 108 | 20261109T203909Z | standard | 20261109T203908Z | 11/06/2026 |
| Social Security Administration | 2024 | complete | 369 | 369 | True | 35 | 20261109T203932Z | standard | 20261109T203931Z | 11/06/2026 |
| Social Security Administration | 2025 | complete | 313 | 313 | True | 28 | 20261109T203955Z | standard | 20261109T203954Z | 11/06/2026 |
| Social Security Administration | 2026 | complete | 235 | 235 | True | 58 | 20261109T204018Z | standard | 20261109T204017Z | 11/06/2026 |

`download job` is the generation time USAspending embeds in the zip name; `cached` means the API returned an earlier job for an identical request, in which case the worker re-requested with an equivalent split-window body (`request = split_time_period`) after proving both bodies count the same rows.
