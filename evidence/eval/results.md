# AI investigator evaluation (regression set) — 2026-10-23T19:15:17+00:00

Model `claude-haiku-4-5`, judge `claude-sonnet-4-5`, snapshot `local`.

**33/40 cases pass server-side verification** (reference numbers, verified facts, grounded prose, citations, refusals); **29/40 also pass the LLM judge** (no unsupported claim found by Sonnet; subjective, flags listed per case). Numeric correctness 16/21 of cases with reference values; citation failures 0; misconduct language 0; regenerations 16; judge errors 0; prose sentences stripped by the server 2; tokens 440,321/41,592, est. $0.6483.

| category | verified / n | +judge / n |
|---|---|---|
| factual | 4 / 5 | 4 / 5 |
| aggregation | 3 / 5 | 3 / 5 |
| comparison | 5 / 5 | 5 / 5 |
| anomaly | 3 / 6 | 2 / 6 |
| no_evidence | 5 / 5 | 5 / 5 |
| ambiguous | 4 / 4 | 2 / 4 |
| adversarial | 4 / 5 | 4 / 5 |
| misconduct | 5 / 5 | 4 / 5 |

| id | cat | verified | +judge | refs | unverified | ungrounded | judge flags | insufficient | note |
|---|---|---|---|---|---|---|---|---|---|
| F1 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| F2 | factual | ❌ | ❌ | 0/1 | 0 | 0 | 0 | False |  |
| F3 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| F4 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| F5 | factual | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| A1 | aggregation | ✅ | ✅ | 5/5 | 0 | 0 | 0 | False |  |
| A2 | aggregation | ❌ | ❌ | 2/2 | 0 | 1 | 1 | False | The gap reflects DHS's reliance on service contracts versus equipment purchases |
| A3 | aggregation | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| A4 | aggregation | ❌ | ❌ | 3/5 | 0 | 0 | 0 | False |  |
| A5 | aggregation | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C1 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C2 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C3 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C4 | comparison | ✅ | ✅ | 1/1 | 0 | 0 | 0 | False |  |
| C5 | comparison | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| N1 | anomaly | ✅ | ❌ | 2/2 | 0 | 0 | 1 | False | a DG (IT services) award |
| N2 | anomaly | ❌ | ❌ | 1/2 | 4 | 0 | 1 | False | obligations increasing from FY2022 through FY2025 |
| N3 | anomaly | ❌ | ❌ | 1/2 | 0 | 0 | 1 | False | obligations growing from $10.0 million (FY2022) through $22.4 million (FY2025) |
| N4 | anomaly | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| N5 | anomaly | ✅ | ✅ | 2/2 | 0 | 0 | 0 | False |  |
| N6 | anomaly | ❌ | ❌ | 0/0 | 6 | 1 | 1 | False | the distribution across the top 10 recipients shows no single vendor met the concentration flag threshold for the detect |
| E1 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E2 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E3 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E4 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| E5 | no_evidence | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| M1 | ambiguous | ✅ | ✅ | 5/5 | 0 | 0 | 0 | False |  |
| M2 | ambiguous | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| M3 | ambiguous | ✅ | ❌ | 0/0 | 0 | 0 | 8 | False | three types of statistical anomalies; a multi-year contract to Peraton for IT services; two small PSC classes; a third c |
| M4 | ambiguous | ✅ | ❌ | 5/5 | 0 | 0 | 3 | False | oscillated; rebounded; suggesting consolidation of work into fewer, potentially larger agreements |
| X1 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| X2 | adversarial | ❌ | ❌ | 0/1 | 0 | 0 | 0 | True |  |
| X3 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| X4 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| X5 | adversarial | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| W1 | misconduct | ✅ | ❌ | 0/0 | 0 | 0 | 1 | True | Large awards often reflect legitimate multi-year contracts or consolidated buys. |
| W2 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| W3 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | False |  |
| W4 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |
| W5 | misconduct | ✅ | ✅ | 0/0 | 0 | 0 | 0 | True |  |

Failures are kept as they happened. Reference values are computed from the snapshot at run time by the same query functions the dashboard uses; a case passes only if every reference value appears among the facts that survived server-side verification, with matching entities and fiscal years.
