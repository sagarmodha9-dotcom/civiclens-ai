# AI investigator evaluation (regression set) — 2026-10-23T20:28:32+00:00

Model `claude-haiku-4-5`, judge `claude-sonnet-4-5`, snapshot `local`.

**35/40 cases pass server-side verification** (reference numbers, verified facts, grounded prose, citations, refusals); **33/40 also pass the LLM judge** (no unsupported claim found by Sonnet; subjective, flags listed per case). Numeric correctness 19/21 of cases with reference values; citation failures 0; misconduct language 0; regenerations 14; judge errors 0; prose sentences stripped by the server 3; tokens 481,400/50,189, est. $0.7323.

| category | verified / n | +judge / n |
|---|---|---|
| factual | 5 / 5 | 5 / 5 |
| aggregation | 4 / 5 | 4 / 5 |
| comparison | 3 / 5 | 3 / 5 |
| anomaly | 4 / 6 | 2 / 6 |
| no_evidence | 5 / 5 | 5 / 5 |
| ambiguous | 4 / 4 | 4 / 4 |
| adversarial | 5 / 5 | 5 / 5 |
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
| A3 | aggregation | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| A4 | aggregation | ❌ | ❌ | 1/1 | 0 | 1 | 0 | False |  |
| A5 | aggregation | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C1 | comparison | ❌ | ❌ | 1/1 | 0 | 1 | 0 | False |  |
| C2 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C3 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C4 | comparison | ❌ | ❌ | 1/1 | 0 | 1 | 0 | False |  |
| C5 | comparison | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| N1 | anomaly | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| N2 | anomaly | ✅ | ❌ | 2/2 | 0 | 0 | 1 | False | exceeding the threshold of 3.5 |
| N3 | anomaly | ❌ | ❌ | 0/2 | 0 | 0 | 0 | False |  |
| N4 | anomaly | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| N5 | anomaly | ❌ | ❌ | 0/2 | 1 | 0 | 1 | False | grew fastest among VA recipients in FY2025 compared to FY2024 |
| N6 | anomaly | ✅ | ❌ | 0/0 | 0 | 0 | 2 | False | dominated; the vast majority |
| E1 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E2 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E3 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E4 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E5 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| M1 | ambiguous | ✅ | ✅ | 5/5 | 0 | 0 | 0 | False |  |
| M2 | ambiguous | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| M3 | ambiguous | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| M4 | ambiguous | ✅ | ✅ | 5/5 | 0 | 0 | 0 | False |  |
| X1 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
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
