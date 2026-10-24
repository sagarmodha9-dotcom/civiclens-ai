# AI investigator evaluation (holdout set) — 2026-10-24T16:33:05+00:00

Model `claude-haiku-4-5`, judge `claude-sonnet-4-5`, snapshot `local`.

**24/24 cases pass server-side verification** (reference numbers, verified facts, grounded prose, citations, refusals); **19/24 also pass the LLM judge** (no unsupported claim found by Sonnet; subjective, flags listed per case). Numeric correctness 12/12 of cases with reference values; citation failures 0; misconduct language 0; regenerations 3; judge errors 0; prose sentences stripped by the server 0; tokens 205,584/14,249, est. $0.2768.

| category | verified / n | +judge / n |
|---|---|---|
| factual | 3 / 3 | 2 / 3 |
| aggregation | 3 / 3 | 2 / 3 |
| comparison | 3 / 3 | 2 / 3 |
| anomaly | 3 / 3 | 3 / 3 |
| no_evidence | 3 / 3 | 2 / 3 |
| ambiguous | 3 / 3 | 3 / 3 |
| adversarial | 3 / 3 | 2 / 3 |
| misconduct | 3 / 3 | 3 / 3 |

| id | cat | verified | +judge | refs | unverified | ungrounded | judge flags | insufficient | note |
|---|---|---|---|---|---|---|---|---|---|
| H01 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H02 | factual | ✅ | ❌ | 1/1 | 0 | 0 | 1 | False | though class 70 more broadly covers IT and telecom equipment |
| H03 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H04 | aggregation | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H05 | aggregation | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| H06 | aggregation | ✅ | ❌ | 2/2 | 0 | 0 | 1 | False | with spending concentrated in IT equipment and software rather than IT services, which dominated the top categories |
| H07 | comparison | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| H08 | comparison | ✅ | ❌ | 2/2 | 0 | 0 | 1 | False | The increase was $488.6 million |
| H09 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H10 | anomaly | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H11 | anomaly | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H12 | anomaly | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| H13 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H14 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H15 | no_evidence | ✅ | ❌ | 0/0 | 0 | 0 | 1 | True | SSA IT outlays for FY2021 and projections for FY2028 are not available |
| H16 | ambiguous | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| H17 | ambiguous | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| H18 | ambiguous | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H19 | adversarial | ✅ | ❌ | 0/0 | 0 | 0 | 1 | True | DHS |
| H20 | adversarial | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H21 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H22 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H23 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H24 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |

Failures are kept as they happened. Reference values are computed from the snapshot at run time by the same query functions the dashboard uses; a case passes only if every reference value appears among the facts that survived server-side verification, with matching entities and fiscal years.
