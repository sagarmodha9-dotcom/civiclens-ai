# Ingestion report — 2026-11-02T20:23:42+00:00

Cells in data set: **30** (pulled or re-checked this run: 30), failed: **0**, prime transactions: **109,885**, count mismatches: **4**

| agency | FY | status | prime rows | API count | match | sub-award rows | download job (UTC) | request | extracted | API last_updated |
|---|---|---|---|---|---|---|---|---|---|---|
| Department of Veterans Affairs | 2022 | complete | 5,197 | 5,197 | True | 1214 | 20261102T193419Z | standard | 20261102T193418Z | 11/02/2026 |
| Department of Veterans Affairs | 2023 | complete | 4,268 | 4,268 | True | 679 | 20261102T193544Z | standard | 20261102T193543Z | 11/02/2026 |
| Department of Veterans Affairs | 2024 | complete | 3,972 | 3,972 | True | 856 | 20261102T193658Z | standard | 20261102T193657Z | 11/02/2026 |
| Department of Veterans Affairs | 2025 | complete | 3,917 | 3,917 | True | 536 | 20261102T193824Z | standard | 20261102T193823Z | 11/02/2026 |
| Department of Veterans Affairs | 2026 | complete | 4,382 | 4,382 | True | 387 | 20261102T194040Z | standard | 20261102T194039Z | 11/02/2026 |
| Department of Homeland Security | 2022 | complete | 8,020 | 8,020 | True | 1076 | 20261102T194133Z | standard | 20261102T194132Z | 11/02/2026 |
| Department of Homeland Security | 2023 | complete | 6,654 | 6,654 | True | 987 | 20261102T194624Z | standard | 20261102T194623Z | 11/02/2026 |
| Department of Homeland Security | 2024 | complete | 5,502 | 5,502 | True | 952 | 20261102T194921Z | standard | 20261102T194920Z | 11/02/2026 |
| Department of Homeland Security | 2025 | complete | 5,040 | 5,040 | True | 708 | 20261102T195126Z | standard | 20261102T195125Z | 11/02/2026 |
| Department of Homeland Security | 2026 | complete | 4,451 | 4,451 | True | 647 | 20261102T195300Z | standard | 20261102T195259Z | 11/02/2026 |
| Department of Health and Human Services | 2022 | complete | 5,944 | 5,944 | True | 1300 | 20261102T195507Z | standard | 20261102T195506Z | 11/02/2026 |
| Department of Health and Human Services | 2023 | complete | 5,465 | 5,465 | True | 1419 | 20261102T195723Z | standard | 20261102T195722Z | 11/02/2026 |
| Department of Health and Human Services | 2024 | complete | 4,842 | 4,842 | True | 998 | 20261102T195919Z | standard | 20261102T195918Z | 11/02/2026 |
| Department of Health and Human Services | 2025 | complete | 4,310 | 4,310 | True | 591 | 20261102T200105Z | standard | 20261102T200104Z | 11/02/2026 |
| Department of Health and Human Services | 2026 | complete | 3,743 | 3,743 | True | 570 | 20261102T200340Z | standard | 20261102T200339Z | 11/02/2026 |
| Department of the Treasury | 2022 | complete | 3,822 | 3,822 | True | 657 | 20261102T200454Z | standard | 20261102T200453Z | 11/02/2026 |
| Department of the Treasury | 2023 | count_mismatch | 3,308 | 3,309 | False | 655 | 20261102T200638Z | standard | 20261102T200637Z | 11/02/2026 |
| Department of the Treasury | 2024 | count_mismatch | 3,372 | 3,375 | False | 782 | 20261102T200752Z | standard | 20261102T200751Z | 11/02/2026 |
| Department of the Treasury | 2025 | count_mismatch | 4,020 | 4,022 | False | 542 | 20261102T200926Z | standard | 20261102T200925Z | 11/02/2026 |
| Department of the Treasury | 2026 | count_mismatch | 2,865 | 2,871 | False | 319 | 20261102T201040Z | standard | 20261102T201039Z | 11/02/2026 |
| Department of Commerce | 2022 | complete | 3,898 | 3,898 | True | 403 | 20261102T201143Z | standard | 20261102T201142Z | 11/02/2026 |
| Department of Commerce | 2023 | complete | 3,463 | 3,463 | True | 498 | 20261102T201358Z | standard | 20261102T201357Z | 11/02/2026 |
| Department of Commerce | 2024 | complete | 2,907 | 2,907 | True | 448 | 20261102T201543Z | standard | 20261102T201542Z | 11/02/2026 |
| Department of Commerce | 2025 | complete | 2,638 | 2,638 | True | 358 | 20261102T201748Z | standard | 20261102T201747Z | 11/02/2026 |
| Department of Commerce | 2026 | complete | 2,152 | 2,152 | True | 279 | 20261102T201922Z | standard | 20261102T201921Z | 11/02/2026 |
| Social Security Administration | 2022 | complete | 438 | 438 | True | 84 | 20261102T202006Z | standard | 20261102T202005Z | 11/02/2026 |
| Social Security Administration | 2023 | complete | 378 | 378 | True | 108 | 20261102T202039Z | standard | 20261102T202038Z | 11/02/2026 |
| Social Security Administration | 2024 | complete | 369 | 369 | True | 35 | 20261102T202112Z | standard | 20261102T202111Z | 11/02/2026 |
| Social Security Administration | 2025 | complete | 313 | 313 | True | 28 | 20261102T202215Z | standard | 20261102T202214Z | 11/02/2026 |
| Social Security Administration | 2026 | complete | 235 | 235 | True | 58 | 20261102T202300Z | standard | 20261102T202257Z | 11/02/2026 |

`download job` is the generation time USAspending embeds in the zip name; `cached` means the API returned an earlier job for an identical request, in which case the worker re-requested with an equivalent split-window body (`request = split_time_period`) after proving both bodies count the same rows.
