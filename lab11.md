# Lab 11 — Pro-Forma Sensitivity: Find Tesla's Drivers

> Educational exercise only; not investment advice. Dollar amounts are USD millions except per-share data.

## D — Question

Which assumptions drive Tesla's forecast and value, and what explains their effects?

The existing Lab 10 model is a five-year FCFE model. Its base case forecasts FY2030 operating income of $1,371.6 million, FY2030 FCFE of $1,015.4 million, and value per share of $2.62. The original base-case balance-sheet gaps are $0.0 million in every forecast year.

## R — Drivers, ranges, and locked record

The two independent operating inputs are automotive revenue growth and energy revenue growth. They are existing model assumptions, not calculated statement totals. Each lower and higher path moves every forecast-year rate by five percentage points from base, so the comparison uses the same-width range for both drivers.

| Driver | FY2026E–FY2030E base | Lower | Higher | Unit and reason for range |
|---|---|---|---|---|
| Automotive revenue growth | 0%, 4%, 5%, 5%, 4% | -5%, -1%, 0%, 0%, -1% | 5%, 9%, 10%, 10%, 9% | Percentage points. Judgment range around a base case that begins at 0% after Tesla's reported 10% automotive-revenue decline in 2025. |
| Energy revenue growth | 20%, 18%, 15%, 12%, 10% | 15%, 13%, 10%, 7%, 5% | 25%, 23%, 20%, 17%, 15% | Percentage points. Judgment range around a base case informed by Tesla's reported 27% energy-generation-and-storage growth in 2025. |

Outputs are the same for each run: FY2030 operating income, FY2030 **FCFE**, and value per share only when the terminal FCFE supports a defensible perpetuity-growth valuation. All FCFE amounts remain signed.

### Locked Changed-Input Record

This record states the timestamped prediction, changed input, expected result, and partner unit/one-change check made before the sensitivity run.

| Timestamp | Input old → new, with units | Predicted direction and rough size | Why | Partner unit/one-change check |
|---|---|---|---|---|
| September 29, 2026, 2:14 PM | Automotive growth FY2026E–FY2030E: 0%, 4%, 5%, 5%, 4% → -5%, -1%, 0%, 0%, -1% (five-percentage-point decrease each year) | I predict FY2030 operating income and FCFE will decrease substantially. I expect automotive growth to have a larger effect than energy growth, and FY2030 FCFE may become negative, making value per share unavailable. | Automotive is Tesla's largest revenue segment, so lower growth should reduce revenue, gross profit, operating income, and FCFE. | Partner confirmed these are percentage-point changes and that only automotive growth changes; all other independent assumptions stay at base. |

## I/V — One-at-a-time sensitivity results and verification

Every run starts from a fresh independent copy of the base assumptions. Only the named driver changes; the linked income statement, balance sheet, cash flow, cash, and accounting checks recalculate. `tesla_proforma.py` restores a fresh base input set and reruns it after the analysis.

### Automotive revenue growth

| Case | Actual FY2026E–FY2030E inputs | FY2030 operating income | Change from base | FY2030 FCFE | Change from base | Value/share | Change from base |
|---|---|---:|---:|---:|---:|---:|---:|
| Lower | -5%, -1%, 0%, 0%, -1% | -173.0 | -1,544.6 | -528.1 | -1,543.5 | Unavailable | Unavailable |
| Base | 0%, 4%, 5%, 5%, 4% | 1,371.6 | 0.0 | 1,015.4 | 0.0 | 2.62 | 0.00 |
| Higher | 5%, 9%, 10%, 10%, 9% | 3,245.1 | 1,873.5 | 2,693.1 | 1,677.8 | 6.95 | 4.33 |
| **Span** | **Maximum minus minimum** | **3,418.1** |  | **3,221.3** |  | **4.33** | **valid valuation cases only** |

The lower case keeps the signed $528.1 million negative FCFE. Its FY2030 terminal FCFE is negative, so no perpetuity-growth terminal value or value per share is reported. That is a valuation limitation, not a zero or discarded cash flow.

FY2030 trace for the higher run: total revenue $147,329.7; gross profit $29,465.9; SG&A $8,839.8; R&D $8,103.1; depreciation $9,278.0; operating income $3,245.1. Higher automotive growth increases revenue and gross profit, while SG&A and R&D rise with the linked model; the remaining operating-profit increase flows through to FCFE.

### Energy revenue growth

| Case | Actual FY2026E–FY2030E inputs | FY2030 operating income | Change from base | FY2030 FCFE | Change from base | Value/share | Change from base |
|---|---|---:|---:|---:|---:|---:|---:|
| Lower | 15%, 13%, 10%, 7%, 5% | 937.2 | -434.4 | 631.8 | -383.6 | 1.63 | -0.99 |
| Base | 20%, 18%, 15%, 12%, 10% | 1,371.6 | 0.0 | 1,015.4 | 0.0 | 2.62 | 0.00 |
| Higher | 25%, 23%, 20%, 17%, 15% | 1,888.6 | 517.0 | 1,458.7 | 443.4 | 3.77 | 1.14 |
| **Span** | **Maximum minus minimum** | **951.4** |  | **826.9** |  | **2.13** |  |

FY2030 trace for the higher run: total revenue $131,371.1; gross profit $26,274.2; SG&A $7,882.3; R&D $7,225.4; depreciation $9,278.0; operating income $1,888.6. Higher energy growth raises revenue and gross profit; linked operating expenses rise as well, producing the stated operating-income and FCFE changes.

### Checks

Every usable lower, base, and higher run passed: maximum absolute balance-sheet gap was $0.0 million and the minimum cash-floor surplus was $0.0 million. Signed changes recompute as changed output minus base output. The final restored-base check passed: it reproduced the original base outputs and accounting checks within the model's $0.005 million/$0.01 per-share rounding tolerance.

## E — Main driver and interpretation

**Over these stated equal-width ranges, automotive revenue growth is the larger driver** of FY2030 operating profit and FCFE: its spans are $3,418.1 million and $3,221.3 million, versus $951.4 million and $826.9 million for energy growth. It is also the larger value driver over valid valuation cases, with a $4.33 per-share span compared with $2.13 for energy.

This is not a claim that automotive growth is universally more important than energy growth. Sensitivity rankings depend on the chosen ranges; a wider range could produce a larger span. Here, the same five-percentage-point shifts were used for both drivers, but automotive begins from a substantially larger revenue base, which explains the larger result.

The result changes the research priority rather than the conservative base-case conclusion: Tesla's automotive delivery, pricing, and mix assumptions deserve the closest follow-up because the low automotive case leaves FY2030 FCFE negative and makes the terminal value unavailable. Energy remains meaningful but does not move these outputs as much over the tested ranges.

## Partner exchange and prediction reconciliation

These notes record the three partner exchanges and the reconciliation of the locked prediction to the actual result.

- Partner exchange 1 — My partner asked why I used a five-percentage-point range for automotive growth. I explained that the equal ±5-percentage-point shifts make the automotive and energy tests comparable and remain a labelled judgment around Tesla's base case. My partner confirmed that the figures are percentage-point changes and that only automotive growth changes while all other independent assumptions remain at base.
- Partner exchange 2 — I showed my partner the lower automotive-growth result and the base result. They recomputed the FY2030 FCFE change as -$528.1 million minus $1,015.4 million, or -$1,543.5 million. They asked why FCFE fell so sharply; I traced the effect from lower automotive revenue to lower gross profit, operating income, and FCFE. On my partner's model, I checked that their selected driver alone changed and that their reported change equaled changed output minus base output.
- Partner exchange 3 — My partner asked whether automotive growth ranked first only because of the selected range. I answered that the selected range always affects a sensitivity ranking, but both Tesla drivers here use equal ±5-percentage-point shifts, so automotive's larger result mainly reflects its much larger revenue base. Our companies may have different main drivers because their segment mix, starting revenue base, margins, and assumptions differ.
- Prediction reconciliation — My prediction was directionally correct: reducing automotive growth materially lowered FY2030 operating income and FCFE. I expected automotive to be the larger driver and anticipated that FCFE might become negative; the result confirmed this, with FY2030 FCFE of -$528.1 million and value per share unavailable because a negative terminal FCFE cannot support a defensible perpetuity-growth valuation. This does not change the conservative base-case valuation conclusion, but it changes my research priority toward automotive deliveries, pricing, and vehicle mix.

## Sensitivity — Learn on your own

1. **One-at-a-time sensitivity** changes one independent assumption while holding the other independent assumptions at base and allowing linked accounting quantities to recalculate. It isolates that input's effect over the stated range.
2. **Input ranges affect ranking** because the span measures movement from the stated lower to higher case. A larger range can generate a larger output span even if the underlying economic driver is not inherently more important.
3. **A sensitivity table is not a forecast probability** because it does not estimate the likelihood of the lower, base, or higher cases. It shows conditional model outcomes if each specified assumption occurs.
