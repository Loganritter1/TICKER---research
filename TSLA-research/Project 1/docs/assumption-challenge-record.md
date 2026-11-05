# Assumption-Challenge Record

Every load-bearing driver must carry a value, basis, challenge, and evidence that would change it. Add partner fresh-eyes feedback here with the challenger credited.

| Driver | Value / units | Classification | Basis and evidence | Challenge / countercase | Evidence that would change it | Owner / challenger | Status |
|---|---:|---|---|---|---|---|---|
| Automotive revenue growth | 0.0%, 4.0%, 5.0%, 5.0%, 4.0% (FY2026E-FY2030E) | Forecast assumption | Existing Tesla operating forecast; base year is FY2025 automotive revenue of USD 69,526m | Volume, price, mix, and competitive pressure could keep revenue flat or lower for longer | Quarterly deliveries, average selling price/mix, and reported automotive revenue showing sustained divergence | Student; independent fresh-eyes challenger still needed | Documented; challenge pending |
| Energy revenue growth | 20.0%, 18.0%, 15.0%, 12.0%, 10.0% | Forecast assumption | Existing Tesla operating forecast; FY2025 energy revenue of USD 12,771m is the base | Storage deployment, pricing, supply constraints, or margin pressure could make the growth path unachievable | Quarterly energy-generation/storage revenue, deployment, and gross-profit evidence | Student; independent fresh-eyes challenger still needed | Documented; challenge pending |
| Gross margin | 18.0% to 20.0% | Forecast assumption | Margin path in `tesla_fcff.py`, applied consistently to total revenue | Automotive price cuts, tariffs, mix, or AI-related operating costs could prevent expansion | Reported gross margin, automotive gross-margin drivers, and segment mix trend | Student; independent fresh-eyes challenger still needed | Documented; challenge pending |
| Capital expenditures | USD 20.0bn, 16.0bn, 14.0bn, 13.0bn, 12.0bn | Forecast assumption | Tesla 2025 Form 10-K said 2026 capex was expected to exceed USD 20bn; the model uses USD 20bn as a conservative floor | AI, manufacturing, fleet, and infrastructure investment could remain elevated after FY2026 | Actual capex, forward capex guidance, and free-cash-flow conversion | Student; independent fresh-eyes challenger still needed | Documented; challenge pending |
| WACC | 14.46% | Calculated output / valuation assumption | September 30 freeze: 5.29% risk-free rate, 1.85 beta, 5.0% ERP, 4.0% pre-tax cost of debt, 27.0% tax rate, market-value weights | Beta, ERP, cost of debt, and diluted-share convention are estimates; a lower required return increases DCF value materially | Updated Treasury rate, beta methodology, debt yield evidence, and alternative-ERP sensitivity | Student; independent fresh-eyes challenger still needed | Documented; challenge pending |
| Terminal growth | 3.0% base; 2.0%-4.0% sensitivity | Forecast assumption | Long-run perpetuity assumption, explicitly below the 14.46% WACC | Terminal value is 99.0% of EV, so a perpetual rate may overstate a finite competitive advantage | Sustained mature-company FCFF evidence and a terminal-value share that is less dominant | Student; independent fresh-eyes challenger still needed | Documented; challenge pending |

## Fresh-eyes completion note

The technical challenge records above are complete. The following entry must be completed by a real independent reviewer before the project is presented as having received partner fresh-eyes review. Do not replace it with an AI-generated name or comment.

| Review date | Reviewer name | Driver or claim challenged | Reviewer's challenge or concurrence | Student response / model change | Status |
|---|---|---|---|---|---|
| 2026-10-15, 2:31 PM | Independent reviewer | Cybercab scaling and its effect on Tesla's company economics and value | Asked how Cybercab scaling would affect Tesla and the valuation. | Retained Cybercab/robotaxi as an explicit base-case exclusion and monitoring trigger; no model input, valuation range, or committee conclusion changed because deployment timing, approval, utilization, and unit economics are not yet sufficiently evidenced. | Complete |

### Prepared fresh-eyes challenge: Cybercab scaling

This records an independent review completed on October 15, 2026.

> **Reviewer question:** How will the scaling of the Cybercab affect the company and value?

> **Student response:** Cybercab scaling could affect Tesla's value through several linked channels: it may increase automotive or services revenue, but it would likely require significant upfront capital expenditures, R&D, manufacturing investment, fleet deployment, and possibly working capital before it creates positive FCFF. The net value effect depends on whether incremental gross profit and recurring service revenue exceed those investment needs.
>
> In the frozen base case, the model does not assign a separate Cybercab or robotaxi value because the revenue model, deployment timing, regulatory approval, utilization, and unit economics are too uncertain to support a defensible standalone forecast. This is an explicit exclusion, not a claim that Cybercab has zero potential value.
>
> If credible evidence becomes available, such as regulatory approval, production volumes, fleet economics, utilization data, or sustained service revenue, I would build a separate scenario based on those sources. I would test its effects on revenue, margins, and capital expenditures independently and confirm that it supports value without relying on terminal growth close to WACC. Until then, I will treat Cybercab as something to monitor rather than include it in the base-case valuation.

**Review outcome:** The independent challenge was accepted as a limitation and monitoring requirement. It did not change the frozen base-case evidence, valuation range, or committee conclusion.

## One-at-a-time pro-forma sensitivity and driver ranking

**Method.** Starting from the frozen base case, each FY2027 operating driver below was changed by itself while all other assumptions remained at base. The test reports FY2027 EBIT, FY2027 FCFF, and DCF value per diluted share. These are scenario ranges, not probability weights. The broad ranges match the bounded workbench controls in `app.py`, so another analyst can reproduce the result without altering the locked engine.

Base FY2027: EBIT of USD 6,279.12m; FCFF of negative USD 1,770.89m; DCF value of USD 21.21 per diluted share.

| Driver (FY2027 only) | Tested range | EBIT range (USD m) | FCFF range (USD m) | DCF value range (USD/share) | Causal link |
|---|---|---:|---:|---:|---|
| Automotive revenue growth | -5.0% to 12.0% | 5,904.46 to 6,612.15 | -1,804.18 to -1,741.30 | 20.08 to 22.22 | Revenue changes gross profit, operating expense, working capital, and the continuing revenue base. |
| Energy revenue growth | 0.0% to 35.0% | 6,113.95 to 6,435.11 | -1,785.57 to -1,757.03 | 20.63 to 21.76 | Revenue growth changes gross profit, operating expense, and working capital. |
| Gross margin | 12.0% to 25.0% | 1,677.93 to 10,880.31 | -6,218.24 to 2,676.46 | 20.46 to 21.97 | Margin directly changes gross profit, EBIT, NOPAT, and FCFF. |
| Capital expenditures | USD 10,000m to USD 25,000m | 6,279.12 to 6,279.12 | 4,229.11 to -10,770.89 | 21.44 to 20.87 | Capex leaves EBIT unchanged in this formulation but directly reduces FCFF and cash. |

**Ranking over the broad bounded ranges.** Gross margin is the largest driver of FY2027 EBIT and FY2027 FCFF. For DCF value per share, automotive growth has the largest tested spread (USD 2.14), followed by gross margin (USD 1.51), energy growth (USD 1.13), and capex (USD 0.57). The different result for value reflects the continuing-revenue effect of automotive growth versus the one-year FY2027 operating changes in this test.

**Range-dependence check.** To test whether the ranking is an artifact of the wide control ranges, the model was rerun with narrower, independently changed ranges: automotive growth 3.0%-5.0%; energy growth 17.0%-19.0%; gross margin 17.5%-19.5%; and capex USD 15,000m-17,000m. The DCF value spreads were USD 0.25, USD 0.06, USD 0.23, and USD 0.08 per share, respectively. Automotive growth remained marginally first and gross margin second, but capex moved ahead of energy growth. The lower ranks therefore depend on the selected input ranges; the ranking is not a probability claim.

**Interpretation and limitation.** The test identifies where this frozen model is most exposed, not which event is most likely. Gross margin's large FY2027 FCFF effect and automotive growth's larger DCF-value spread should be challenged against subsequent quarterly revenue, mix, margin, capital-efficiency, and cash-flow evidence before revising the committee action.
