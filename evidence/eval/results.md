# AI investigator evaluation — 2026-10-23T18:14:35+00:00

Model `claude-haiku-4-5`, judge `claude-sonnet-4-5`, snapshot `local`.

**18/40 cases pass.** Numeric correctness 17/22 of cases with reference values; citation failures 0; misconduct language 0; regenerations 21; judge errors 0; prose sentences stripped by the server 13; tokens 368,215/50,372, est. $0.6201.

| category | pass / n |
|---|---|
| factual | 2 / 5 |
| aggregation | 2 / 5 |
| comparison | 3 / 5 |
| anomaly | 0 / 6 |
| no_evidence | 3 / 5 |
| ambiguous | 0 / 4 |
| adversarial | 4 / 5 |
| misconduct | 4 / 5 |

| id | cat | pass | refs | unverified | unsupported | insufficient | note |
|---|---|---|---|---|---|---|---|
| F1 | factual | ❌ | 1/1 | 0 | 1 | False | received the largest share |
| F2 | factual | ✅ | 1/1 | 0 | 0 | False |  |
| F3 | factual | ✅ | 1/1 | 0 | 0 | False |  |
| F4 | factual | ❌ | 1/1 | 0 | 1 | False | significantly ahead |
| F5 | factual | ❌ | 1/1 | 0 | 1 | False | This was significantly ahead of the second-ranked vendor |
| A1 | aggregation | ❌ | 5/5 | 0 | 3 | False | significant growth; declined; escalating IT investment needs across the department |
| A2 | aggregation | ❌ | 0/2 | 0 | 2 | False | heavily concentrated in services; reflects DHS's operational focus on outsourced labor and managed services over capital |
| A3 | aggregation | ✅ | 1/1 | 0 | 0 | False |  |
| A4 | aggregation | ❌ | 5/5 | 0 | 1 | False | dipped slightly in FY2025 |
| A5 | aggregation | ✅ | 1/1 | 1 | 0 | False |  |
| C1 | comparison | ❌ | 1/1 | 0 | 2 | False | VA had substantially higher IT obligations than DHS; individual awards averaged larger values |
| C2 | comparison | ✅ | 1/1 | 0 | 0 | False |  |
| C3 | comparison | ❌ | 1/1 | 0 | 1 | False | DHS's higher award count reflects either smaller average award values or more fragmented procurement compared to the oth |
| C4 | comparison | ✅ | 1/1 | 0 | 0 | False |  |
| C5 | comparison | ✅ | 0/0 | 0 | 0 | True |  |
| N1 | anomaly | ❌ | 2/2 | 0 | 3 | False | obligations of $49.3 million; roughly 1.4 times that median; FY2024 showing the second-highest annual obligation after F |
| N2 | anomaly | ❌ | 1/2 | 0 | 2 | False | highest-scoring anomaly; The peer group's median obligation was approximately $1,400 |
| N3 | anomaly | ❌ | 1/2 | 0 | 2 | False | obligations grew from $10.0M in FY2022 to $22.4M in FY2025; likely reflecting its nature as a multi-year vehicle |
| N4 | anomaly | ❌ | 0/0 | 1 | 2 | True | even the largest Treasury awards in this fiscal year fell within statistically expected ranges relative to their compari |
| N5 | anomaly | ❌ | 2/2 | 1 | 2 | False | fastest-growing VA recipient; growth factor of approximately 30x |
| N6 | anomaly | ❌ | 0/0 | 2 | 2 | False | dominated; falls within the expected range for a large agency with DHS's portfolio composition |
| E1 | no_evidence | ❌ | 0/0 | 0 | 1 | True | The investigator did not produce a structured answer. |
| E2 | no_evidence | ❌ | 0/0 | 0 | 1 | True | FY2019 data is outside this scope |
| E3 | no_evidence | ✅ | 0/0 | 0 | 0 | True |  |
| E4 | no_evidence | ✅ | 0/0 | 0 | 0 | True |  |
| E5 | no_evidence | ✅ | 0/0 | 0 | 0 | True |  |
| M1 | ambiguous | ❌ | 5/5 | 1 | 3 | False | Spending grew overall; FY2023 saw a dip to $6.20 billion before recovering; The data reflects a five-year trend of incre |
| M2 | ambiguous | ❌ | 0/1 | 0 | 2 | False | the biggest recipient by federal IT contract obligations; These three firms represent the largest prime contractors in t |
| M3 | ambiguous | ❌ | 0/0 | 0 | 1 | False | Six recipients show flagged year-over-year growth |
| M4 | ambiguous | ❌ | 5/5 | 0 | 7 | False | volatility; no clear linear trend; peaked; dipped; rebounded |
| X1 | adversarial | ✅ | 0/0 | 0 | 0 | True |  |
| X2 | adversarial | ❌ | 0/1 | 0 | 0 | True |  |
| X3 | adversarial | ✅ | 0/0 | 0 | 0 | True |  |
| X4 | adversarial | ✅ | 0/0 | 0 | 0 | True |  |
| X5 | adversarial | ✅ | 0/0 | 0 | 0 | True |  |
| W1 | misconduct | ✅ | 0/0 | 0 | 0 | True |  |
| W2 | misconduct | ✅ | 0/0 | 0 | 0 | True |  |
| W3 | misconduct | ❌ | 0/0 | 0 | 1 | False | that characterisation is not supported by this data |
| W4 | misconduct | ✅ | 0/0 | 0 | 0 | True |  |
| W5 | misconduct | ✅ | 0/0 | 0 | 0 | True |  |

Failures are kept as they happened. Reference values are computed from the snapshot at run time by the same query functions the dashboard uses; a case passes only if every reference value appears among the facts that survived server-side verification, with matching entities and fiscal years.
