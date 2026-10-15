# Lab 13 — Portfolio Mandate Defense

## S1–S10 statement types

| Statement | Type | Reason |
|---|---|---|
| S1: Horizon seven years; annual rebalancing. | Objective | The seven-year horizon frames the investment plan, while annual rebalancing describes how the policy would be maintained rather than a numerical portfolio limit. |
| S2: CPI + 4% a year, net of costs, over rolling five-year periods. | Objective | This is the desired investment outcome and specifies the return target, measurement period, and that costs must be included. |
| S3: $0.75 million quarterly payout; twelve months of payouts held in cash or daily-liquid government securities. | Hard constraint | The required amount and permitted liquidity sources are stated precisely enough to calculate and test. |
| S4: 60% global equities, 40% U.S. investment-grade bonds benchmark. | Preference | It supplies a comparison benchmark, but does not say that the portfolio must track it or impose a maximum tracking error. |
| S5: Long-only; no borrowing, short sales, or derivatives. | Hard constraint | These are direct investment prohibitions. The checker tests the long-only part from portfolio weights; the other prohibitions would require holdings or trading data. |
| S6: No single issuer above 8%. | Hard constraint | It establishes a measurable concentration cap, with the stated exemptions for cash, Treasury, and diversified funds. |
| S7: Annual turnover at most 25% without committee approval. | Hard constraint | This is a measurable trading limit, but it cannot be tested from one static portfolio without prior holdings and trades. |
| S8: At least 90% redeemable within five business days. | Hard constraint | It gives an explicit percentage, time window, and liquidity requirement. |
| S9: No calendar-year loss greater than 10%. No measure or breach rule. | Unverifiable promise | The loss measure, timing, valuation method, and consequence of breach are unspecified, so it should not be coded as a pass/fail rule. |
| S10: No sector, ESG, tax, or home-bias preference; nobody has said what the pilot should optimize. | Missing | The investment decision criterion for the pilot is absent; the listed non-preferences do not tell an optimizer what to maximize or minimize. |

## Investment policy statement

An investment policy statement (IPS) is a written agreement translating a client's goals, risk tolerance, liquidity needs, time horizon, and governance into an investment mandate. It guides portfolio construction, monitoring, rebalancing, and accountability.

For Meridian, S1 and S2 define the horizon and return objective. S3, S5, S6, S7, and S8 are constraints on liquidity, implementation, concentration, and trading. S4 is the benchmark for evaluation. S9 remains unresolved because it does not define a measurable risk rule, and S10 is an unresolved design choice because the optimization objective is missing.

## Candidate D: attack on the checker

Candidate D is 3% Cash and 97% Global equity index fund. It passes each rule checked by `mandate.py`: its weights total 100%, it is long-only, it holds the 3% reserve minimum, all holdings are redeemable within five days, and no non-exempt company exceeds 8%.

The objection holds because the portfolio takes almost all of its investment risk in equities without a stated rule for trading expected return against downside risk. It exposes S10: the CIO has not said what the pilot should optimize. If the CIO prioritizes minimizing drawdowns or meeting the CPI + 4% target with high reliability, the portfolio could need materially more bonds or cash; if the CIO prioritizes expected return, a high equity weight may be acceptable.

### Skeptical-colleague check (solo role)

Working alone, I played the skeptical colleague required by the instructions. I independently checked candidate D in `mandate.py`: it passes every coded rule, so the objection is not that the checker is wrong. I would still challenge D under S10 because the CIO must choose the pilot's objective and its tradeoff between return, downside risk, and the probability of meeting the target before deciding whether a 97% equity allocation is acceptable.

## Question for the CIO before optimization

What risk criterion should the pilot optimize subject to the CPI + 4% objective—for example, maximum expected return, minimum volatility, minimum expected shortfall, or the highest probability of meeting the five-year target? The answer changes the allocation: a drawdown or expected-shortfall priority would justify more high-quality bonds and cash, while maximizing expected return or target-meeting probability could support a larger equity weight.

## Reflection

A portfolio can pass every checkable rule and still be wrong because the checker only evaluates precise, observable limits. It cannot establish that the portfolio has an appropriate chance of achieving CPI + 4% net of costs, follows the benchmark sensibly, respects the turnover limit, or satisfies the undefined calendar-year-loss statement.

The statement type I was least sure of was S4. I classified it as a preference because it sets a standard for comparison, but it would become a hard constraint if the CIO also specified a required tracking-error band, allocation range, or other rule requiring the portfolio to stay close to it.

## Required checker verification

`mandate.py` calculates a 3.0% reserve minimum. With the supplied A–C inputs, it produces the required A/B/C values and verdicts. Candidate D also passes every checkable rule.

For the required probe, temporarily change candidate A's Cash allocation from 2 to -2 and its Global equity index fund allocation from 60 to 64, then run `python mandate.py`. A's lowest weight should be -2.0 and fail long-only; its reserve-eligible weight remains 10.0 and continues to pass. Restore the original values afterward.

## AI quiz response

I reviewed how issuer aggregation works: the code groups non-exempt holdings by issuer before applying the 8% cap. Therefore, Acme Corp bonds and Acme Corp stock must be added together; in candidate B, 5% + 4% = 9%, which fails.
