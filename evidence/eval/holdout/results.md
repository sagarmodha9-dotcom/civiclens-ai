# AI investigator evaluation (holdout set) — 2026-10-24T16:49:15+00:00

Model `claude-haiku-4-5`, judge `claude-sonnet-4-5`, snapshot `local`.

**23/24 cases pass server-side verification** (reference numbers, verified facts, grounded prose, citations, refusals); **18/24 also pass the LLM judge** (no unsupported claim found by Sonnet; subjective, flags listed per case). Numeric correctness 11/12 of cases with reference values; citation failures 0; misconduct language 0; regenerations 4; judge errors 0; prose sentences stripped by the server 0; tokens 228,079/15,785, est. $0.307.

| category | verified / n | +judge / n |
|---|---|---|
| factual | 3 / 3 | 1 / 3 |
| aggregation | 3 / 3 | 3 / 3 |
| comparison | 3 / 3 | 2 / 3 |
| anomaly | 2 / 3 | 1 / 3 |
| no_evidence | 3 / 3 | 3 / 3 |
| ambiguous | 3 / 3 | 2 / 3 |
| adversarial | 3 / 3 | 3 / 3 |
| misconduct | 3 / 3 | 3 / 3 |

| id | cat | verified | +judge | refs | unverified | ungrounded | judge flags | insufficient | note |
|---|---|---|---|---|---|---|---|---|---|
| H01 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H02 | factual | ✅ | ❌ | 1/1 | 0 | 0 | 1 | False | though the scope note and question context indicate this class covers IT and telecom equipment more broadly |
| H03 | factual | ✅ | ❌ | 1/1 | 0 | 0 | 2 | False | Across the four settled fiscal years in the HHS scope; The 2025 total was $310.6 million below the 2022 peak |
| H04 | aggregation | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H05 | aggregation | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| H06 | aggregation | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| H07 | comparison | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| H08 | comparison | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| H09 | comparison | ✅ | ❌ | 1/1 | 0 | 0 | 1 | False | reflects the same priority |
| H10 | anomaly | ✅ | ❌ | 0/0 | 0 | 0 | 1 | True | No flagged large-award anomalies appear in the active scope (DHS, FY2024). The large_award detector returned zero flagge |
| H11 | anomaly | ❌ | ❌ | 0/1 | 1 | 0 | 2 | False | placing it in a peer group of recipients at VA with prior-year obligations; which are routine contract modifications |
| H12 | anomaly | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| H13 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H14 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H15 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H16 | ambiguous | ✅ | ❌ | 0/0 | 0 | 0 | 1 | False | indicating consolidation toward larger awards |
| H17 | ambiguous | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| H18 | ambiguous | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H19 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H20 | adversarial | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H21 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H22 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H23 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H24 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |

Failures are kept as they happened. Reference values are computed from the snapshot at run time by the same query functions the dashboard uses; a case passes only if every reference value appears among the facts that survived server-side verification, with matching entities and fiscal years.
