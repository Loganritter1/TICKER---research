# Current-Work Audit and Final Build Map

Audit date: October 6, 2026. This is a planning document, not final valuation evidence.

## Reusable work

| Existing artifact | What it provides | Final-project use |
|---|---|---|
| `tesla_proforma.py` | Five-year segment-driven forecast; income statement, balance sheet, cash-flow elements; balance-sheet and cash-floor assertions; one-at-a-time operating sensitivities | Reuse the opening history, segment drivers, and articulation logic; refactor valuation from FCFE to FCFF/WACC |
| `lab10.md` | Filing history, driver rationale, capex context, partner attack, and broken-balance failure test | Source evidence and challenge record input |
| `lab11.md` | Automotive and energy downside/upside paths, sensitivity rationale, and restored-base test | Rebuild as FCFF-based what-if/downside evidence after the student completes the new locked record |
| `lab08.md` and `tsla_pe_comps.py` | Written peer policy, GM qualification rationale, Tesla/GM GAAP diluted P/E reference, and leave-one-out logic | Equity-value multiple and policy starting point |
| `lab06.md` | Earlier DCF, WACC-source notes, training-case reconciliation notes, and reverse-DCF attempt | Reference material only; do not merge its disconnected assumptions into the final model without reconciliation |
| `sources.md` | Initial list of Tesla filings and company disclosures | Populate and expand the final source ledger |

## Material gaps that must be closed

| Priority | Gap | Why it matters | Final action |
|---:|---|---|---|
| 1 | Current valuation is FCFE discounted at cost of equity | Project 1 requires FCFF, WACC, enterprise value, then a sourced enterprise-to-equity bridge | Build the final FCFF engine and bridge; do not relabel FCFE output as FCFF |
| 1 | No final WACC calculation linked to the operating forecast | WACC and terminal convention are required DCF inputs | Create a dated WACC schedule with definitions, sources, and sensitivity grid |
| 1 | No final enterprise-value and equity-value reconciliation | Per-share conclusion must trace from operating value through cash, debt, and other claims | Build a bridge with every adjustment, source, as-of date, and check |
| 1 | Existing output and scripts sit outside `Project 1` | Final repository should be self-contained and runnable from its final project folder | Create the final application and visible output within `Project 1`; retain root lab files unchanged as source workpapers |
| 2 | Cash-flow presentation is abbreviated and the FCFE calculation aggregates operating working-capital movements | The final needs an auditable three-statement forecast, base-year reconciliation, and FCFF inputs | Explicitly calculate NOPAT, D&A, capex, and change in operating NWC; reconcile forecast cash to the balance sheet |
| 2 | Existing model dates, market prices, and valuation conventions vary across labs | Mixed-date inputs make results non-comparable | Freeze one final valuation date; document which facts are FY2025, forecast years, and market-date inputs |
| 2 | Comparable work has P/E only | The brief requires at least one equity-value and one enterprise-value multiple | Retain P/E and add a consistently defined EV multiple with policy and source checks |
| 2 | Low/base/high cases are not yet one final causal valuation range | The committee needs a defensible range and a downside case that may change action | Build integrated low/base/high cases from the final FCFF model and explain method disagreement |
| 2 | Base-year normalization/contamination catalog is not final | The forecast needs a stated clean starting point and treatment of one-time/basis-change items | Identify, source, and document material FY2025 normalizations or explicitly justify no adjustment |
| 3 | Validation evidence is incomplete | The 75-point criterion requires known answers, locked record, AI check, cold run, and highest-risk failure evidence | Add automated checks, a cold-run log, an AI-output disposition, and the student-authored locked record |
| 3 | Final memo, manifest, transcripts, and video evidence do not yet exist | Required final submission surfaces | Complete after the model and validation results are frozen |

## Build order

1. Freeze scope, valuation date, units, share convention, and evidence ledger.
2. Build the final Tesla three-statement forecast and FCFF engine inside `Project 1`.
3. Add WACC, enterprise-value bridge, sensitivity, reverse DCF, and low/base/high cases.
4. Add the EV multiple and reconcile the P/E reference under one peer policy.
5. Run and document validation. The student writes the locked AI-off prediction before the selected changed-input run.
6. Generate visible executed output, then write the memo and record the videos.

## Current conclusion

The earlier Tesla work is worth preserving, but its numeric valuation result is not final-project ready. The required final work is a transparent FCFF/WACC rebuild using the existing company-specific operating assumptions only after their definitions, dates, and sources are reconciled.
