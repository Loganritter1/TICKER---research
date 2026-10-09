# Investment Committee Decision Memo — Draft Structure

## Recommendation and committee ask

**Recommendation: do not initiate at the September 30, 2026 reference price; retain TSLA on a watch list.** The frozen model produces a USD 19.02-25.43 per-share reference range, compared with a USD 354.81 market close. The committee is asked to decline an initial position until a refreshed, independently reconciled model supports a materially different conclusion.

This is a course-project valuation, not investment advice. The range is conditional on the source and policy limitations below and must not be represented as a final target price.

## Decision context

- Target/security: Tesla, Inc. common stock (`TSLA`)
- Valuation date: September 30, 2026
- Currency and units: U.S. dollars; model values are USD millions except per-share data
- Share-count basis: 3.528 billion FY2025 diluted weighted-average shares, used consistently across the DCF and comparable calculations
- Decision horizon: Five explicit forecast years (FY2026E-FY2030E), followed by a perpetuity-growth terminal value
- Included operations and explicit exclusions: Tesla automotive, energy, and services are forecast. The bridge adds reported year-end cash and short-term investments and deducts reported debt and finance leases; it excludes a separate valuation of optionality, future product launches, and unmodeled capital claims.

## Evidence and valuation range

The base FCFF DCF produces enterprise value of USD 39,158.52m, equity value of USD 74,841.52m, and USD 21.21 per diluted share. The WACC/terminal-growth sensitivity spans USD 19.02-24.34 per share using 15.5%/2.0% through 13.5%/4.0% assumptions.

The qualified one-peer references point in the same broad direction: applying GM's automotive EV/revenue multiple produces USD 20.38 per TSLA diluted share, while GM's GAAP P/E produces USD 25.43. GM is not a close economic peer because of its ICE-heavy mix, dealer model, and GM Financial business. These references are corroborative only and are not averaged mechanically with the DCF.

The frozen range is therefore USD 19.02-25.43 per diluted share. The range is far below the USD 354.81 September 30 close. A reverse DCF indicates that, holding explicit cash flows and the 14.46% WACC fixed, the market reference would require roughly 14.06% terminal growth-near the WACC and outside a credible perpetual-growth assumption.

## Material assumptions and scenarios

The DCF low/base/high sensitivity points are USD 19.02, USD 21.21, and USD 24.34 per share. The modeled FY2026-FY2027 capital-expenditure profile produces negative FCFF of USD 8,781.8m and USD 1,770.9m before FCFF becomes positive in FY2028. This creates meaningful execution risk and makes the terminal value 99.0% of base enterprise value. Retaining USD 10bn as operating cash in the bridge would reduce the DCF value to USD 18.38 per share.

The high terminal-value share is a material limitation: the valuation is highly dependent on conditions beyond the explicit forecast. The base case uses a frozen 14.46% WACC and 3.0% terminal growth. Beta, ERP, pre-tax cost of debt, and operating-cash treatment remain assumptions and policy judgments, so they remain subject to sensitivity.

## Risks, reversal conditions, and monitoring

The recommendation could be wrong if Tesla achieves sustainably higher operating margins, energy growth, capital efficiency, or cash generation than modeled, or if the selected WACC materially overstates required return. It could also be wrong if the model's treatment of all cash and short-term investments as non-operating liquidity is not economically appropriate.

Reconsider the decision after: (1) independently reconciling the September 30 WACC, close, shares, and bridge inputs; (2) observing sustained positive FCFF and capex efficiency above the base forecast; (3) evidence of durable automotive gross-margin expansion; or (4) a revised scenario that supports value closer to the market price without relying on terminal growth near WACC. Monitor quarterly automotive, energy, and services revenue; gross margin; capex; cash and investments; debt/leases; diluted shares; and updated guidance.

## AI-use and validation reference

`validation-and-ai-use.md` records the passing arithmetic, articulation, monotonicity, terminal-value failure, bridge sensitivity, and locked changed-input checks. The changed-input run increased FY2027 automotive growth from 4% to 6%, raised FY2027 FCFF by USD 7.40m, and increased DCF value by USD 0.25 per share; it did not alter the recommendation. The dated-input and bridge freeze is documented in `docs/freeze-2026-09-30.md`.
