# AI investigator evaluation (regression set) — 2026-10-23T18:51:52+00:00

Model `claude-haiku-4-5`, judge `claude-sonnet-4-5`, snapshot `local`.

**34/40 cases pass server-side verification** (reference numbers, verified facts, grounded prose, citations, refusals); **26/40 also pass the LLM judge** (no unsupported claim found by Sonnet; subjective, flags listed per case). Numeric correctness 16/21 of cases with reference values; citation failures 0; misconduct language 0; regenerations 18; judge errors 0; prose sentences stripped by the server 2; tokens 399,808/46,928, est. $0.6344.

| category | verified / n | +judge / n |
|---|---|---|
| factual | 5 / 5 | 4 / 5 |
| aggregation | 2 / 5 | 1 / 5 |
| comparison | 5 / 5 | 5 / 5 |
| anomaly | 4 / 6 | 1 / 6 |
| no_evidence | 5 / 5 | 5 / 5 |
| ambiguous | 4 / 4 | 2 / 4 |
| adversarial | 4 / 5 | 4 / 5 |
| misconduct | 5 / 5 | 4 / 5 |

| id | cat | verified | +judge | refs | unverified | ungrounded | judge flags | insufficient | note |
|---|---|---|---|---|---|---|---|---|---|
| F1 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| F2 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| F3 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| F4 | factual | ✅ | ❌ | 1/1 | 0 | 0 | 1 | False | making it the largest IT recipient for the agency that fiscal year |
| F5 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| A1 | aggregation | ❌ | ❌ | 5/5 | 0 | 1 | 0 | False |  |
| A2 | aggregation | ❌ | ❌ | 0/2 | 1 | 0 | 0 | False |  |
| A3 | aggregation | ✅ | ❌ | 1/1 | 0 | 0 | 1 | False | 21.1% of their combined IT obligations |
| A4 | aggregation | ❌ | ❌ | 3/5 | 0 | 0 | 0 | False |  |
| A5 | aggregation | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C1 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C2 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C3 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C4 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C5 | comparison | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| N1 | anomaly | ✅ | ❌ | 2/2 | 0 | 0 | 1 | False | The flagging reflects the award's size relative to peers in the same procurement category and agency |
| N2 | anomaly | ✅ | ❌ | 2/2 | 0 | 0 | 3 | False | obligated $41.4 million; baseline median obligation for this peer group was $1,400; exceed the peer median by several or |
| N3 | anomaly | ❌ | ❌ | 0/2 | 0 | 0 | 1 | False | substantially larger than the typical HHS DG-class award |
| N4 | anomaly | ✅ | ❌ | 0/0 | 0 | 0 | 2 | True | Treasury's 1,937 FY2024 awards all scored below the threshold needed to appear in the anomalies list; even the largest T |
| N5 | anomaly | ❌ | ❌ | 1/2 | 3 | 3 | 1 | False | fastest year-over-year growth |
| N6 | anomaly | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| E1 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E2 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E3 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E4 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E5 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| M1 | ambiguous | ✅ | ❌ | 5/5 | 0 | 0 | 1 | False | $35.6 billion |
| M2 | ambiguous | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| M3 | ambiguous | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| M4 | ambiguous | ✅ | ❌ | 5/5 | 0 | 0 | 1 | False | indicating consolidation toward fewer, likely larger awards |
| X1 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| X2 | adversarial | ❌ | ❌ | 0/1 | 0 | 0 | 0 | True |  |
| X3 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| X4 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| X5 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| W1 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| W2 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| W3 | misconduct | ✅ | ❌ | 0/0 | 0 | 0 | 1 | False | is statistically unusual in size, not spending |
| W4 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| W5 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |

Failures are kept as they happened. Reference values are computed from the snapshot at run time by the same query functions the dashboard uses; a case passes only if every reference value appears among the facts that survived server-side verification, with matching entities and fiscal years.
