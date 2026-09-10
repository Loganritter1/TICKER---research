# Lab 06 — Tesla, Inc. (TSLA)

> **Disclaimer:** I am not a licensed financial professional. This lab work is for educational purposes only and is not investment advice.

**Source filing:** [Tesla 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm), filed January 29, 2026.  The companion [Tesla research report](Tesla_2026-09-03_report.md) is the starting workpaper for this lab.

| Input | Value | Unit | As-of | Exact filing locator / note |
|---|---:|---|---|---|
| Starting FCFF | 6,433.16 | USD millions | Dec. 31, 2025 | Consolidated Statements of Cash Flows, p. 53: $14,747 operating cash flow + $292 interest paid × (1 − 27% effective tax rate) − $8,527 capex. |
| Growth, Year 1 | 11.0 (estimate) | % | 2026 forecast | Tesla’s company-compiled analyst consensus: 2026 revenue $105,221M versus 2025 revenue $94,827M, or about 11%. Applied here as an FCFF-growth estimate. |
| Growth, Year 2 | 8.0 (estimate) | % | 2027 forecast | Forecast: growth moderates after the 2026 consensus recovery; based on Item 7’s automotive weakness and energy-storage growth. |
| Growth, Year 3 | 6.0 (estimate) | % | 2028 forecast | Forecast: continued moderation toward mature-company growth; Item 7, MD&A. |
| Growth, Year 4 | 5.0 (estimate) | % | 2029 forecast | Forecast: continued moderation toward mature-company growth; Item 7, MD&A. |
| Growth, Year 5 | 4.0 (estimate) | % | 2030 forecast | Forecast: approaches the 3% terminal-growth assumption; Item 7, MD&A. |
| WACC | 16.1 (estimate) | % | Sept. 10, 2026 | Cost of equity = 4.844% 10-year Treasury yield + 2.26 beta × 5.0% equity-risk premium = 16.144%. Cost of debt assumed at 3.0% pre-tax; after 27% tax = 2.19%. Market-value weights: $1.45T equity and $8.177B debt; WACC = 16.07%, rounded. |
| Terminal growth | 3.0 | % | Long-run assumption | Estimate representing long-run economic growth, not Tesla-specific growth. |
| Non-operating cash | 44,059 | USD millions | Dec. 31, 2025 | Note 3, Cash, Cash Equivalents and Investments, p. 67: total cash, cash equivalents, and short-term investments at fair value. |
| Debt | 8,177 | USD millions | Dec. 31, 2025 | Note 9, Debt, p. 73: total debt; finance leases excluded by this convention. |
| Diluted shares | 3,528 | millions | FY 2025 | Note 2, Earnings per Share, p. 62: diluted weighted-average shares. |
| TSLA price | 367.81 | USD/share | Sept. 10, 2026, 2:08 PM EDT | [Investing.com TSLA quote](https://www.investing.com/equities/tesla-motors), captured at the stated time. |

The FCFF convention used here follows the lab instruction: operating cash flow plus after-tax interest paid, less capital expenditure. Tesla reported $14,747M operating cash flow, $292M cash interest paid, $8,527M capital expenditure, and a 27% effective tax rate. Thus, starting FCFF = $14,747 + ($292 × (1 − 0.27)) − $8,527 = **$6,433.16M**. This resolves the discrepancy with the supplied research report’s $6,219M simplified operating-cash-flow-less-capex figure.

## Assumption sources and calculation notes

- The official [Tesla Q2 2026 analyst-consensus release](https://ir.tesla.com/press-release/earnings-consensus-second-quarter-2026) reports average 2026 revenue of $105,221 million. The Year 1 11.0% estimate uses that revenue growth as a transparent proxy for FCFF growth; Years 2–5 are my labelled judgmental estimates, not company guidance or analyst consensus.
- The [Federal Reserve H.15 release](https://www.federalreserve.gov/releases/h15/) reported a 4.844% 10-year Treasury yield for September 10, 2026. TSLA’s beta was 2.26 in the [beta source](https://wallstreetnumbers.com/stocks/tsla/beta). The 5.0% equity-risk premium and 3.0% pre-tax cost of debt are labelled assumptions. Tesla’s 2025 effective tax rate was 27% in Item 7 / Note 12; its debt-note rates range by facility, so 3.0% is a simplified estimate rather than a quoted all-in borrowing cost.
- The current quote was captured on September 10, 2026 at 2:08 PM EDT. It is the reverse-DCF target; it is not a valuation input.

## Model status

The labelled growth estimates, 16.1% WACC, sensitivity grid, and reverse-DCF target are entered in `dcf.py`. Run `python dcf.py` from the project folder to reproduce the Tesla output below.

## Training-case verification

Before entering the Tesla case, `dcf.py` was run with the required training inputs. The twelve original lines reproduced the known $27.4974 value per diluted share. The training sensitivity-grid cells were $28.5989, $32.9426, $39.0238; $24.3564, $27.4974, $31.6853; and $21.0579, $23.4140, $26.4433. The reverse DCF, using a $30.00 target and a -5% to +10% bracket, solved a **+1.7779 percentage-point** uniform shift to all five explicit growth rates.

## Tesla model output

`python dcf.py` with the Tesla inputs produces a **$26.9864 value per diluted share**. The base case is the center sensitivity-grid cell (16.1% WACC and 3.0% terminal growth).

| WACC \\ Terminal growth | 2.0% | 3.0% | 4.0% |
|---|---:|---:|---:|
| 15.1% | $27.4902 | $28.3997 | $29.4731 |
| 16.1% | $26.2324 | **$26.9864** | $27.8650 |
| 17.1% | $25.1420 | $25.7741 | $26.5026 |

Value falls as WACC rises and rises as terminal growth rises. The sensitivity range read from the corners is **$25.1420 to $29.4731 per share**.

### Reverse DCF

The target price is **$367.81**. The solved variable is a uniform shift to all five explicit growth rates, using the required -5.0% to +10.0% search bracket. The program reports **no solution in that bracket**; it does not report a bound as a solution.

Inputs held fixed: starting FCFF $6,433.16M; WACC 16.1%; terminal growth 3.0%; non-operating cash $44,059M; debt $8,177M; diluted shares 3,528M; and base growth rates of 11%, 8%, 6%, 5%, and 4%.

### Reasonableness

The $26.9864 base value is compared with a $367.81 TSLA share price captured on September 10, 2026 at 2:08 PM EDT. It is **outside** the 0.5x–2x band: the price is about 13.6 times the DCF value. The input I distrust most is the explicit FCFF-growth path, because Year 1 applies revenue-consensus growth as a proxy for FCFF growth while Tesla has guided to substantially higher 2026 capital expenditure; revenue growth need not convert into FCFF growth.

### Conditional recommendation

**Watch/defer. Initiate if** TSLA trades at or below the model’s $29.4731 high-corner value, or Tesla provides sourced evidence that supports a materially higher FCFF path after its AI and manufacturing investment. **Otherwise** defer. **Monitor:** operating cash flow and capital expenditures in the next quarterly filing.
