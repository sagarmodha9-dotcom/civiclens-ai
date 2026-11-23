# Ingestion report — 2026-11-23T22:12:28+00:00

Cells in data set: **30** (pulled or re-checked this run: 30), failed: **0**, prime transactions: **109,935**, count mismatches: **4**

| agency | FY | status | prime rows | API count | match | sub-award rows | download job (UTC) | request | extracted | API last_updated |
|---|---|---|---|---|---|---|---|---|---|---|
| Department of Veterans Affairs | 2022 | complete | 5,197 | 5,197 | True | 1214 | 20261123T213028Z | standard | 20261123T213027Z | 11/23/2026 |
| Department of Veterans Affairs | 2023 | complete | 4,265 | 4,265 | True | 679 | 20261123T213222Z | standard | 20261123T213221Z | 11/23/2026 |
| Department of Veterans Affairs | 2024 | complete | 3,966 | 3,966 | True | 856 | 20261123T213346Z | standard | 20261123T213345Z | 11/23/2026 |
| Department of Veterans Affairs | 2025 | complete | 3,917 | 3,917 | True | 555 | 20261123T213520Z | standard | 20261123T213519Z | 11/23/2026 |
| Department of Veterans Affairs | 2026 | complete | 4,377 | 4,377 | True | 388 | 20261123T213636Z | standard | 20261123T213635Z | 11/23/2026 |
| Department of Homeland Security | 2022 | complete | 8,020 | 8,020 | True | 1076 | 20261123T213800Z | standard | 20261123T213759Z | 11/23/2026 |
| Department of Homeland Security | 2023 | complete | 6,654 | 6,654 | True | 987 | 20261123T214045Z | standard | 20261123T214044Z | 11/23/2026 |
| Department of Homeland Security | 2024 | complete | 5,502 | 5,502 | True | 954 | 20261123T214300Z | standard | 20261123T214259Z | 11/23/2026 |
| Department of Homeland Security | 2025 | complete | 5,043 | 5,043 | True | 709 | 20261123T214505Z | standard | 20261123T214504Z | 11/23/2026 |
| Department of Homeland Security | 2026 | complete | 4,459 | 4,459 | True | 651 | 20261123T214722Z | standard | 20261123T214719Z | 11/23/2026 |
| Department of Health and Human Services | 2022 | complete | 5,944 | 5,944 | True | 1300 | 20261123T214929Z | standard | 20261123T214928Z | 11/23/2026 |
| Department of Health and Human Services | 2023 | complete | 5,465 | 5,465 | True | 1422 | 20261123T215143Z | standard | 20261123T215142Z | 11/23/2026 |
| Department of Health and Human Services | 2024 | complete | 4,842 | 4,842 | True | 999 | 20261123T215358Z | standard | 20261123T215357Z | 11/23/2026 |
| Department of Health and Human Services | 2025 | complete | 4,311 | 4,311 | True | 592 | 20261123T215542Z | standard | 20261123T215541Z | 11/23/2026 |
| Department of Health and Human Services | 2026 | complete | 3,743 | 3,743 | True | 571 | 20261123T215706Z | standard | 20261123T215705Z | 11/23/2026 |
| Department of the Treasury | 2022 | complete | 3,822 | 3,822 | True | 657 | 20261123T215830Z | standard | 20261123T215829Z | 11/23/2026 |
| Department of the Treasury | 2023 | count_mismatch | 3,308 | 3,309 | False | 655 | 20261123T220024Z | standard | 20261123T220023Z | 11/23/2026 |
| Department of the Treasury | 2024 | count_mismatch | 3,372 | 3,375 | False | 784 | 20261123T220142Z | standard | 20261123T220138Z | 11/23/2026 |
| Department of the Treasury | 2025 | count_mismatch | 4,020 | 4,022 | False | 542 | 20261123T220306Z | standard | 20261123T220304Z | 11/23/2026 |
| Department of the Treasury | 2026 | count_mismatch | 2,868 | 2,875 | False | 327 | 20261123T220419Z | standard | 20261123T220418Z | 11/23/2026 |
| Department of Commerce | 2022 | complete | 3,905 | 3,905 | True | 405 | 20261123T220505Z | standard | 20261123T220501Z | 11/23/2026 |
| Department of Commerce | 2023 | complete | 3,469 | 3,469 | True | 498 | 20261123T220610Z | standard | 20261123T220608Z | 11/23/2026 |
| Department of Commerce | 2024 | complete | 2,925 | 2,925 | True | 448 | 20261123T220713Z | standard | 20261123T220712Z | 11/23/2026 |
| Department of Commerce | 2025 | complete | 2,653 | 2,653 | True | 359 | 20261123T220819Z | standard | 20261123T220818Z | 11/23/2026 |
| Department of Commerce | 2026 | complete | 2,155 | 2,155 | True | 280 | 20261123T220902Z | standard | 20261123T220901Z | 11/23/2026 |
| Social Security Administration | 2022 | complete | 438 | 438 | True | 84 | 20261123T220945Z | standard | 20261123T220944Z | 11/23/2026 |
| Social Security Administration | 2023 | complete | 378 | 378 | True | 108 | 20261123T221018Z | standard | 20261123T221017Z | 11/23/2026 |
| Social Security Administration | 2024 | complete | 369 | 369 | True | 35 | 20261123T221111Z | standard | 20261123T221109Z | 11/23/2026 |
| Social Security Administration | 2025 | complete | 313 | 313 | True | 28 | 20261123T221143Z | standard | 20261123T221142Z | 11/23/2026 |
| Social Security Administration | 2026 | complete | 235 | 235 | True | 58 | 20261123T221207Z | standard | 20261123T221206Z | 11/23/2026 |

`download job` is the generation time USAspending embeds in the zip name; `cached` means the API returned an earlier job for an identical request, in which case the worker re-requested with an equivalent split-window body (`request = split_time_period`) after proving both bodies count the same rows.
