# Validation and AI-Use Record

This is the working source for the final frozen `Validation-and-AI-Use.pdf`. It must match the submitted PDF at the final submission timestamp.

## AI-use disclosure

| Tool | Use | Output used as | Independent verification / disposition |
|---|---|---|---|
| Codex | Project structuring, code assistance, research leads, and explanatory support | Lead or draft only | To be completed with source and model checks |

## Required validation register

| Check | Highest-risk claim targeted | Prediction / pass criterion | Evidence artifact | Result | Status |
|---|---|---|---|---|---|
| Known-answer reconciliation | Core valuation arithmetic | Base-case EV = USD 39,158.52m; equity value = USD 74,841.52m; value/share = USD 21.21, each within USD 0.01m or USD 0.01/share | `tests/test_tesla_fcff.py::test_known_answer_base_case` | Pass on 2026-10-08 after market-input freeze | Complete |
| Independent source / definition check | Load-bearing input | Same definition and units in a second source or calculation | `docs/freeze-2026-09-30.md` | TSLA/GM closes cross-checked; Treasury rate checked against the official Fed series; filed cash, investments, debt, leases, and diluted shares reconciled | Complete |
| Three-statement articulation | Forecast integrity | Balance sheet balances; cash flow ties to cash; base year reconciles | `tests/test_tesla_fcff.py::test_three_statement_articulation_and_bridge` | Pass on 2026-10-08; each forecast-year gap = USD 0.00m | Complete |
| DCF monotonicity | DCF logic | Value falls as WACC rises and rises as terminal growth rises | `tests/test_tesla_fcff.py::test_dcf_monotonicity` | Pass on 2026-10-08 | Complete |
| Enterprise-to-equity bridge | Per-share result | Each adjustment is sourced and reconciles | `tests/test_tesla_fcff.py::test_three_statement_articulation_and_bridge`, `tests/test_tesla_fcff.py::test_operating_cash_reserve_bridge_sensitivity`, and `docs/freeze-2026-09-30.md` | Base bridge and USD 10bn operating-cash sensitivity reconcile | Complete |
| Peer-policy consistency | Comparable valuation | Policy predates selection; all multiple definitions are consistent |  |  | Open |
| Highest-risk failure test | Terminal-value construction | Model rejects terminal growth at or above WACC | `tests/test_tesla_fcff.py::test_highest_risk_terminal_value_failure_fails_loudly` | Pass on 2026-10-08; injected terminal growth = WACC raises `ValueError` | Complete |
| Cold run | Reproducibility | Clean environment completes from documented instructions | `python tesla_fcff.py` and `python -m unittest discover -s tests -p "test_*.py" -v` | Local reproducibility run passes on 2026-10-08; no third-party packages required | Complete |
| AI-output check | AI reliability | AI output accepted, corrected, qualified, or rejected with evidence |  |  | Open |

## Locked Changed-Input Record — student-authored AI-off prediction required

**Stop here before completing this section. The prediction below must be written by the student without generative-AI assistance and before the corresponding model run.**

| Field | Student entry |
|---|---|
| Precommit timestamp and commit identifier | October 6, 2026, 7:02 PM -pre-run commit: 6b732cd (October 6, 2026, 7:06 PM EDT) |
| Exact input changed, old value, new value, and units | Automotive revenue growth for FY2027 increasing from 4% to 6%, a 2 percentage point increase. All other independent assumptions remain unchanged.  |
| Human-authored AI-off prediction of output direction | With this change, I predict the FY2027 FCFF will increase. |
| Expected decision effect | The result would likely not directly change the watch/defer decision because one small assumption change may not close the large gap between valuation and market price. |
| Why this is a finance-grounded expectation | With automotive revenue growth increased, we should see higher total revenue, gross profit but also higher operating expenses. EBIT and NOPAT will increase if added gross profit exceeds the added expenses. FCFF will should increase but be partly offset by higher working-capital needs. We should also see a higher DCF value if the added FCFF is positive overall |
| Actual output direction and magnitude after run | FY2027 FCFF increased from negative USD 1,770.89m to negative USD 1,763.49m: an increase of USD 7.40m. In the frozen model, base DCF value increased from USD 21.21/share to USD 21.47/share: an increase of USD 0.25/share. |
| Actual decision effect | No change. The result remains far below the September 30 market reference of USD 354.81/share, so the provisional watch/defer / do-not-initiate conclusion remains unchanged. |
| Prediction reconciliation; failure diagnosis or no-change reason | Direction matched the pre-run prediction. The small magnitude reflects only a two-percentage-point FY2027 automotive-growth change; higher FCFF is partly offset by higher operating working-capital needs and does not materially alter the terminal-value-driven conclusion. |
