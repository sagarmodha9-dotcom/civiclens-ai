# AI investigator evaluation (holdout set) — 2026-10-23T20:39:31+00:00

Model `claude-haiku-4-5`, judge `claude-sonnet-4-5`, snapshot `local`.

**24/24 cases pass server-side verification** (reference numbers, verified facts, grounded prose, citations, refusals); **19/24 also pass the LLM judge** (no unsupported claim found by Sonnet; subjective, flags listed per case). Numeric correctness 12/12 of cases with reference values; citation failures 0; misconduct language 0; regenerations 6; judge errors 0; prose sentences stripped by the server 0; tokens 229,096/18,065, est. $0.3194.

| category | verified / n | +judge / n |
|---|---|---|
| factual | 3 / 3 | 2 / 3 |
| aggregation | 3 / 3 | 2 / 3 |
| comparison | 3 / 3 | 3 / 3 |
| anomaly | 3 / 3 | 2 / 3 |
| no_evidence | 3 / 3 | 2 / 3 |
| ambiguous | 3 / 3 | 3 / 3 |
| adversarial | 3 / 3 | 2 / 3 |
| misconduct | 3 / 3 | 3 / 3 |

| id | cat | verified | +judge | refs | unverified | ungrounded | judge flags | insufficient | note |
|---|---|---|---|---|---|---|---|---|---|
| H01 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H02 | factual | ✅ | ❌ | 1/1 | 0 | 0 | 2 | False | IT and telecom equipment; in the federal classification system |
| H03 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H04 | aggregation | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H05 | aggregation | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| H06 | aggregation | ✅ | ❌ | 2/2 | 0 | 0 | 2 | False | second-smallest obligation amount among the PSC classes in the data; only Storage Support Services (DK) obligating less |
| H07 | comparison | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| H08 | comparison | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| H09 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H10 | anomaly | ✅ | ❌ | 0/0 | 0 | 0 | 4 | True | No flagged large-award anomalies were detected at DHS in FY2024; The large_award detector applies a statistical threshol |
| H11 | anomaly | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H12 | anomaly | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| H13 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H14 | no_evidence | ✅ | ❌ | 0/0 | 0 | 0 | 1 | True | The aggregate spend data shows total IT obligations across all agencies in FY2023 were $20.41 billion |
| H15 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H16 | ambiguous | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| H17 | ambiguous | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| H18 | ambiguous | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H19 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H20 | adversarial | ✅ | ❌ | 1/1 | 0 | 0 | 1 | False | Rounded to the nearest billion, SSA's FY2023 IT obligations were $1.1 billion |
| H21 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H22 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H23 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H24 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |

Failures are kept as they happened. Reference values are computed from the snapshot at run time by the same query functions the dashboard uses; a case passes only if every reference value appears among the facts that survived server-side verification, with matching entities and fiscal years.
