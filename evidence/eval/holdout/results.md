# AI investigator evaluation (holdout set) — 2026-10-23T20:23:28+00:00

Model `claude-haiku-4-5`, judge `claude-sonnet-4-5`, snapshot `local`.

**22/24 cases pass server-side verification** (reference numbers, verified facts, grounded prose, citations, refusals); **19/24 also pass the LLM judge** (no unsupported claim found by Sonnet; subjective, flags listed per case). Numeric correctness 10/12 of cases with reference values; citation failures 0; misconduct language 0; regenerations 3; judge errors 0; prose sentences stripped by the server 0; tokens 194,276/17,182, est. $0.2802.

| category | verified / n | +judge / n |
|---|---|---|
| factual | 2 / 3 | 2 / 3 |
| aggregation | 2 / 3 | 2 / 3 |
| comparison | 3 / 3 | 2 / 3 |
| anomaly | 3 / 3 | 2 / 3 |
| no_evidence | 3 / 3 | 2 / 3 |
| ambiguous | 3 / 3 | 3 / 3 |
| adversarial | 3 / 3 | 3 / 3 |
| misconduct | 3 / 3 | 3 / 3 |

| id | cat | verified | +judge | refs | unverified | ungrounded | judge flags | insufficient | note |
|---|---|---|---|---|---|---|---|---|---|
| H01 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H02 | factual | ❌ | ❌ | 0/1 | 0 | 0 | 2 | False | this classification title appears to be a legacy code descriptor; does not reflect the actual content of modern IT and t |
| H03 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H04 | aggregation | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H05 | aggregation | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| H06 | aggregation | ❌ | ❌ | 1/2 | 0 | 0 | 2 | False | across all six agencies combined; This class represents IT equipment and software procurement |
| H07 | comparison | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| H08 | comparison | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| H09 | comparison | ✅ | ❌ | 1/1 | 0 | 0 | 1 | False | because DA encompasses a high-volume service category with relatively mature contractor relationships at HHS |
| H10 | anomaly | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H11 | anomaly | ✅ | ❌ | 1/1 | 0 | 0 | 1 | False | for a growth ratio of 30.41 |
| H12 | anomaly | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| H13 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H14 | no_evidence | ✅ | ❌ | 0/0 | 0 | 0 | 2 | True | Total IT contract obligations across all agencies in scope for FY2023 were approximately $20.4 billion; IT services: $10 |
| H15 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H16 | ambiguous | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| H17 | ambiguous | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| H18 | ambiguous | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H19 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H20 | adversarial | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| H21 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H22 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H23 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| H24 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |

Failures are kept as they happened. Reference values are computed from the snapshot at run time by the same query functions the dashboard uses; a case passes only if every reference value appears among the facts that survived server-side verification, with matching entities and fiscal years.
