# Anomaly engine validation — **FAIL**

Snapshot `None` · commit `81f6527d1154` · 2026-10-23T18:48:47+00:00 · GitHub run `40006331782`

## 1. Independent re-implementation (Python/NumPy vs the pipeline's SQL)

| detector | rows | flagged (pipeline) | flagged (recomputed) | identical flagged set | status mismatches | max rel. score diff | result |
|---|---|---|---|---|---|---|---|
| large_award | 46,458 | 157 | 157 | yes | 0 | 1.4e+00 | FAIL |
| concentration | 359 | 94 | 94 | yes | 0 | 6.7e-16 | PASS |
| recipient_growth | 21,017 | 219 | 219 | yes | 0 | 0.0e+00 | PASS |

Parameters: `{"baseline_fys": "2022,2023,2024,2025", "min_peer_n": 30, "z_threshold": 3.5, "hhi_threshold": 2500, "hhi_top_share": 50, "hhi_min_spend": 5000000, "growth_ratio": 3, "growth_min_delta": 2000000, "growth_min_base": 500000}`. Thresholds were not changed for this run.

## 2. Source trace of representative flagged records

Each flagged value is traced back through Silver to the deduplicated raw Bronze rows (the USAspending download). "Matches" means equal to the cent. Descriptors are read from the record; none of this is a finding about conduct.

### Large award-year obligations (highest-scoring flagged award per agency)

| agency | FY | recipient | PIID | value | score / thr | peer n | baseline median | silver txns → sum | bronze rows (raw/dedup) → sum | type · PSC | dates · mods · parent | years of this award | source | result |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Department of Veterans Affairs | 2022 | COLOSSAL CONTRACTING LLC | 36C10B20F0069 | $119,181,357.39 | 6.103 / 3.5 | 306 | $37,993 | 16 → $119,181,357.39 ✓ | 16/16 → $119,181,357.39 ✓ | DELIVERY ORDER · 7035 INFORMATION TECHNOLOGY SUPPORT EQUIPMENT | 2021-12-15→2022-09-27 · 16 mods · under NNG15SD72B | FY2022: $119.2M, FY2023: $-29.6M, FY2024: $0.0M, FY2025: $-4.1M | [usaspending](https://www.usaspending.gov/award/CONT_AWD_36C10B20F0069_3600_NNG15SD72B_8000/) | PASS |
| Social Security Administration | 2022 | INTERNATIONAL BUSINESS MACHINES CORPORATION | SS001730048 | $58,487,500.00 | 5.159 / 3.5 | 62 | $271,989 | 6 → $58,487,500.00 ✓ | 6/6 → $58,487,500.00 ✓ | DELIVERY ORDER · 7030 INFORMATION TECHNOLOGY SOFTWARE | 2021-12-22→2022-09-28 · 6 mods · under GS35F110DA | FY2022: $58.5M, FY2023: $48.9M, FY2024: $0.0M, FY2024: $41.4M, FY2025: $36.0M, FY2026: $36.0M | [usaspending](https://www.usaspending.gov/award/CONT_AWD_SS001730048_2800_GS35F110DA_4732/) | PASS |
| Department of Commerce | 2023 | PERATON INC. | 1332KP23CNEEJ0001 | $92,130,533.55 | 4.844 / 3.5 | 187 | $46,816 | 3 → $92,130,533.55 ✓ | 3/3 → $92,130,533.55 ✓ | DEFINITIVE CONTRACT · DG11 IT AND TELECOM - NETWORK: SATELLITE COMMUNICATIONS AND TELECOM ACCESS SERVICES | 2023-02-17→2023-08-09 · 3 mods · standalone | FY2023: $92.1M, FY2024: $88.6M, FY2025: $28.0M, FY2026: $144.5M | [usaspending](https://www.usaspending.gov/award/CONT_AWD_1332KP23CNEEJ0001_1330_-NONE-_-NONE-/) | PASS |
| Department of the Treasury | 2022 | MAXIMUS FEDERAL SERVICES, INC. | 2032H521F00374 | $30,539,724.33 | 4.483 / 3.5 | 58 | $84,752 | 16 → $30,539,724.33 ✓ | 16/16 → $30,539,724.33 ✓ | DELIVERY ORDER · DH10 IT AND TELECOM - PLATFORM AS A SERVICE: DATABASE, MAINFRAME, MIDDLEWARE | 2021-12-06→2022-09-28 · 16 mods · under 47QTCK18D0044 | FY2022: $30.5M, FY2023: $29.5M, FY2024: $22.5M, FY2025: $-2.8M | [usaspending](https://www.usaspending.gov/award/CONT_AWD_2032H521F00374_2050_47QTCK18D0044_4732/) | PASS |
| Department of Homeland Security | 2022 | CACI, INC. - FEDERAL | 70T03022F7667N011 | $68,513,984.09 | 3.982 / 3.5 | 408 | $1,715 | 7 → $68,513,984.09 ✓ | 7/7 → $68,513,984.09 ✓ | DELIVERY ORDER · DE01 IT AND TELECOM - END USER: HELP DESK; TIER 1-2, WORKSPACE, PRINT, OUTPUT, PRODUCTIVITY TOOLS (LABOR) | 2022-04-06→2022-09-26 · 7 mods · under 47QTCK18D0009 | FY2022: $68.5M, FY2023: $0.0M, FY2026: $-1.4M | [usaspending](https://www.usaspending.gov/award/CONT_AWD_70T03022F7667N011_7013_47QTCK18D0009_4732/) | PASS |
| Department of Health and Human Services | 2025 | DELOITTE & TOUCHE LLP | 75N92022F00065 | $22,436,356.90 | 3.592 / 3.5 | 168 | $40,969 | 6 → $22,436,356.90 ✓ | 6/6 → $22,436,356.90 ✓ | DELIVERY ORDER · DG01 IT AND TELECOM - NETWORK SUPPORT SERVICES (LABOR) | 2024-12-06→2025-08-22 · 6 mods · under GS00F029DA | FY2022: $10.0M, FY2023: $18.4M, FY2024: $18.7M, FY2025: $22.4M, FY2026: $18.0M | [usaspending](https://www.usaspending.gov/award/CONT_AWD_75N92022F00065_7529_GS00F029DA_4732/) | PASS |

### Vendor concentration (highest HHI cells)

| agency | PSC class | FY | cell total | recipients (table / silver) | HHI (table / silver) | top share | top recipient (table / silver) | prior HHI → change | result |
|---|---|---|---|---|---|---|---|---|---|
| Social Security Administration | DK | 2024 | $75,064,416.00 | 1 / 1 | 10000.0 / 10000.0 | 100.0% | FOUR POINTS TECHNOLOGY, L.L.C. / FOUR POINTS TECHNOLOGY, L.L.C. | 10000.0 → 0.0 | PASS |
| Social Security Administration | DC | 2023 | $49,558,257.30 | 1 / 1 | 10000.0 / 10000.0 | 100.0% | AVAYA FEDERAL SOLUTIONS, INC / AVAYA FEDERAL SOLUTIONS, INC | 9084.0 → 916.0 | PASS |
| Social Security Administration | DK | 2022 | $23,743,221.00 | 1 / 1 | 10000.0 / 10000.0 | 100.0% | FOUR POINTS TECHNOLOGY, L.L.C. / FOUR POINTS TECHNOLOGY, L.L.C. | None → None | PASS |
| Social Security Administration | DK | 2023 | $41,273,166.58 | 1 / 1 | 10000.0 / 10000.0 | 100.0% | FOUR POINTS TECHNOLOGY, L.L.C. / FOUR POINTS TECHNOLOGY, L.L.C. | 10000.0 → 0.0 | PASS |

### Recipient growth (largest year-over-year increases)

| agency | FY | recipient | prior FY | this FY | ratio | silver prior / current | awards | largest award this FY | result |
|---|---|---|---|---|---|---|---|---|---|
| Department of Veterans Affairs | 2023 | AT&T ENTERPRISES, LLC | $1,544,585.18 | $306,255,305.14 | 198.28× | $1,544,585.18 / $306,255,305.14 | 2 | [36C10A20F0309](https://www.usaspending.gov/award/CONT_AWD_36C10A20F0309_3600_GS00Q17NSD3000_4732/) $302,630,736 (C) | PASS |
| Department of Veterans Affairs | 2026 | THUNDERCAT TECHNOLOGY, LLC | $58,110,725.51 | $294,650,671.54 | 5.07× | $58,110,725.51 / $294,650,671.54 | 66 | [36C10B26F0287](https://www.usaspending.gov/award/CONT_AWD_36C10B26F0287_3600_NNG15SD26B_8000/) $221,952,278 (C) | PASS |
| Department of Veterans Affairs | 2026 | SPREZZATURA MANAGEMENT CONSULTING, LLC | $22,606,376.48 | $251,133,804.21 | 11.11× | $22,606,376.48 / $251,133,804.21 | 5 | [36C10B24F0365](https://www.usaspending.gov/award/CONT_AWD_36C10B24F0365_3600_47QTCA24D0013_4732/) $209,172,487 (C) | PASS |
| Department of the Treasury | 2025 | COUNTERTRADE PRODUCTS, INC. | $10,695,482.96 | $225,421,548.37 | 21.08× | $10,695,482.96 / $225,421,548.37 | 9 | [2032H325F00025](https://www.usaspending.gov/award/CONT_AWD_2032H325F00025_2001_NNG15SC05B_8000/) $197,640,415 (C) | PASS |

## Reading the sample

- A flagged large award-year is one whose log10 obligation sits ≥ 3.5 robust standard deviations above the median of awards at the same agency, in the same 2-character PSC class, in the same fiscal year, where that group has at least 30 award-years with non-zero spread. The table shows what the record is (type, PSC, number of actions, whether it is an order under a parent vehicle, how many years it runs): large multi-year vehicles and consolidated buys are expected to appear here.
- Concentration flags are cells where one or two recipients hold most of a category's dollars; small or sole-source categories are concentrated by nature, and the methodology page says so.
- Growth flags are recipients whose obligations at one agency rose ≥ 3× and ≥ $2M over the prior year from a base ≥ $500K; new vehicles and option-year exercises produce legitimate jumps.

Every value above can be checked on usaspending.gov through the linked award page; the permalinks come from the download itself.
