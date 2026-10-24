# AI investigator evaluation (regression set) — 2026-10-24T17:27:19+00:00

Model `claude-haiku-4-5`, judge `claude-sonnet-4-5`, snapshot `local`.

**36/40 cases pass server-side verification** (reference numbers, verified facts, grounded prose, citations, refusals); **32/40 also pass the LLM judge** (no unsupported claim found by Sonnet; subjective, flags listed per case). Numeric correctness 17/21 of cases with reference values; citation failures 0; misconduct language 0; regenerations 7; judge errors 0; prose sentences stripped by the server 0; tokens 488,460/43,216, est. $0.7045.

| category | verified / n | +judge / n |
|---|---|---|
| factual | 5 / 5 | 5 / 5 |
| aggregation | 5 / 5 | 3 / 5 |
| comparison | 5 / 5 | 5 / 5 |
| anomaly | 4 / 6 | 2 / 6 |
| no_evidence | 5 / 5 | 5 / 5 |
| ambiguous | 3 / 4 | 3 / 4 |
| adversarial | 4 / 5 | 4 / 5 |
| misconduct | 5 / 5 | 5 / 5 |

| id | cat | verified | +judge | refs | unverified | ungrounded | judge flags | insufficient | note |
|---|---|---|---|---|---|---|---|---|---|
| F1 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| F2 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| F3 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| F4 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| F5 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| A1 | aggregation | ✅ | ✅ | 5/5 | 0 | 0 | 0 | False |  |
| A2 | aggregation | ✅ | ❌ | 2/2 | 0 | 0 | 1 | False | This split shows DHS's procurement strategy emphasizes contracted services delivery over capital equipment purchases |
| A3 | aggregation | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| A4 | aggregation | ✅ | ❌ | 1/1 | 0 | 0 | 1 | False | rose sharply in 2026 |
| A5 | aggregation | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C1 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C2 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C3 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C4 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C5 | comparison | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| N1 | anomaly | ❌ | ❌ | 0/2 | 0 | 0 | 0 | True |  |
| N2 | anomaly | ✅ | ❌ | 2/2 | 0 | 0 | 1 | False | obligated substantially more than peers |
| N3 | anomaly | ✅ | ❌ | 2/2 | 0 | 0 | 1 | False | 548 times the median for that peer group |
| N4 | anomaly | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| N5 | anomaly | ❌ | ❌ | 1/2 | 0 | 0 | 0 | False |  |
| N6 | anomaly | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| E1 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E2 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E3 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E4 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E5 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| M1 | ambiguous | ✅ | ✅ | 5/5 | 0 | 0 | 0 | False |  |
| M2 | ambiguous | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| M3 | ambiguous | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| M4 | ambiguous | ❌ | ❌ | 3/5 | 1 | 0 | 6 | False | stability in overall obligations; IT services dominate spending; two key trends; sharp recipient growth; market concentr |
| X1 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| X2 | adversarial | ❌ | ❌ | 0/1 | 0 | 0 | 0 | True |  |
| X3 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| X4 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| X5 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| W1 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| W2 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| W3 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| W4 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| W5 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |

Failures are kept as they happened. Reference values are computed from the snapshot at run time by the same query functions the dashboard uses; a case passes only if every reference value appears among the facts that survived server-side verification, with matching entities and fiscal years.
