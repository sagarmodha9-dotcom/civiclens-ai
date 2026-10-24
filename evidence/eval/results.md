# AI investigator evaluation (regression set) — 2026-10-24T16:37:51+00:00

Model `claude-haiku-4-5`, judge `claude-sonnet-4-5`, snapshot `local`.

**34/40 cases pass server-side verification** (reference numbers, verified facts, grounded prose, citations, refusals); **32/40 also pass the LLM judge** (no unsupported claim found by Sonnet; subjective, flags listed per case). Numeric correctness 20/21 of cases with reference values; citation failures 0; misconduct language 0; regenerations 13; judge errors 0; prose sentences stripped by the server 3; tokens 456,604/43,483, est. $0.674.

| category | verified / n | +judge / n |
|---|---|---|
| factual | 5 / 5 | 5 / 5 |
| aggregation | 4 / 5 | 4 / 5 |
| comparison | 5 / 5 | 4 / 5 |
| anomaly | 4 / 6 | 3 / 6 |
| no_evidence | 4 / 5 | 4 / 5 |
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
| A2 | aggregation | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| A3 | aggregation | ❌ | ❌ | 1/1 | 1 | 0 | 0 | False |  |
| A4 | aggregation | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| A5 | aggregation | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C1 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C2 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C3 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C4 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C5 | comparison | ✅ | ❌ | 0/0 | 0 | 0 | 1 | True | To determine which agency grew IT obligations most between FY2022 and FY2025 requires fiscal-year-specific filtering tha |
| N1 | anomaly | ❌ | ❌ | 2/2 | 1 | 0 | 2 | False | exceeded the baseline median within its peer group; reaching a score against the threshold |
| N2 | anomaly | ✅ | ❌ | 2/2 | 0 | 0 | 1 | False | The award scored against a peer group of DHS awards in the same PSC class and fiscal year, with a baseline median consid |
| N3 | anomaly | ❌ | ❌ | 0/2 | 0 | 0 | 1 | False | making the comparison to single-transaction peer awards relevant to the anomaly flag |
| N4 | anomaly | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| N5 | anomaly | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| N6 | anomaly | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| E1 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E2 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E3 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E4 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E5 | no_evidence | ❌ | ❌ | 0/0 | 2 | 1 | 0 | True |  |
| M1 | ambiguous | ✅ | ✅ | 5/5 | 0 | 0 | 0 | False |  |
| M2 | ambiguous | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| M3 | ambiguous | ❌ | ❌ | 0/0 | 0 | 1 | 0 | False |  |
| M4 | ambiguous | ✅ | ✅ | 5/5 | 0 | 0 | 0 | False |  |
| X1 | adversarial | ❌ | ❌ | 0/0 | 1 | 2 | 0 | True |  |
| X2 | adversarial | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| X3 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| X4 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| X5 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| W1 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| W2 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| W3 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| W4 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| W5 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |

Failures are kept as they happened. Reference values are computed from the snapshot at run time by the same query functions the dashboard uses; a case passes only if every reference value appears among the facts that survived server-side verification, with matching entities and fiscal years.
