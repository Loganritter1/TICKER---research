# Research Evolution — Working Source

This Markdown file will become the source for the final `Research-Evolution.pdf`.

## Edition A status

This record preserves the research evolution without revising or relabeling later work as the original Edition A.

## Edition B

### Current decision question

Should a buy-side investment committee with no current Tesla position initiate, watch/defer, or not initiate TSLA at the stated valuation date, based on a defensible valuation range and explicit conditions?

### A-to-B change table

| Changed item | Edition A | Edition B | Primary driver of change | Evidence or test that justified the change |
|---|---|---|---|---|
| Thesis / recommendation | Baseline unavailable pending instructor guidance | Do not initiate at the September 30, 2026 price; retain TSLA on a watch list | Frozen DCF and qualified comparable evidence both remain far below the market reference | `docs/decision-memo.md`, frozen model output, and GM qualified references |
| Data / source choice | Baseline unavailable pending instructor guidance | Dated market closes are cross-checked; the risk-free rate uses the official Federal Reserve series; balance-sheet bridge inputs use Tesla's FY2025 10-K | Reconciliation replaced an unsupported preliminary rate and makes definitions traceable | `docs/freeze-2026-09-30.md` |
| Assumption / model design | Baseline unavailable pending instructor guidance | Linked FCFF/WACC model with EV-to-equity bridge, reverse DCF, WACC/terminal-growth sensitivity, and operating-cash reserve sensitivity | The final decision requires an enterprise-value framework rather than an FCFE relabeling | `tesla_fcff.py`, `tests/test_tesla_fcff.py` |
| Risk / limitation / uncertainty | Baseline unavailable pending instructor guidance | Terminal value represents 99.0% of enterprise value; GM is a qualified one-peer reference; all reported liquidity may not be excess cash | The limitations materially constrain confidence in a point estimate | `docs/decision-memo.md`, `docs/freeze-2026-09-30.md`, and `lab08.md` |

### What changed, and why?

Edition B moves the project from lab-stage valuation work to a linked FCFF/WACC framework with an explicit EV-to-equity bridge. The dated-input freeze corrected the preliminary risk-free rate from 5.26% to 5.29% using the Federal Reserve H.15 series, which recalculated WACC to 14.46% and base DCF value to USD 21.21 per share. The resulting conclusion is not a claim that the market is wrong: it is a conditional do-not-initiate/watch-list recommendation because the model is terminal-value dependent and the market price would require 14.06% terminal growth under the frozen explicit cash flows.

The comparable evidence was retained only as corroboration. The pre-existing policy admits GM as one qualified manufacturer reference but does not treat it as an interchangeable peer because of its ICE-heavy mix, dealer model, and GM Financial business. The final record also distinguishes facts checked against primary or independent market sources from judgments such as beta, ERP, cost of debt, terminal growth, and operating-cash treatment.

Edition A remains unavailable pending instructor guidance. This document does not recreate or relabel a later document as Edition A. Add a dated instructor response here if one becomes available.
