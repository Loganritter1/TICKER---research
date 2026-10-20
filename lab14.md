# Lab 14 — Portfolio Baselines

## Decision and inputs

- **Decision user:** Meridian Foundation Reserve CIO
- **Horizon:** seven years, with annual rebalancing
- **Benchmark:** 60% global equity index fund / 40% investment-grade bond fund
- **Universe:** Treasury bills, Treasury 10-year note, investment-grade bond fund, and global equity index fund
- **Objective:** CPI + 4%; using the labelled 2.5% CPI estimate, the provisional classroom objective is 6.5% annually
- **Hard constraints relevant to the baseline:** 3.0% reserve minimum in cash or daily-liquid government securities, long-only, at least 90% redeemable within five business days, and no non-exempt issuer above 8%
- **Input units and boundary:** course-authored annual expected returns, annual volatilities, and correlations; these are training values rather than market estimates, so no market as-of date or missing-data rule applies

## Baseline results

| Portfolio | Bills / 10-year / IG / equity weights | Expected return | Volatility | Reserve-eligible | Meets 6.5% objective? |
|---|---:|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | Yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | No |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | No |

The weights sum to 100% in every case. `portfolio.py` validates that all correlations are between -1 and 1 and that the correlation table is symmetric before constructing the covariance matrix.

## Known-answer reconciliation

For the benchmark, only the investment-grade bond and equity sleeves have nonzero weights. Using decimal inputs:

```text
variance = (0.40^2 × 0.06^2) + (0.60^2 × 0.16^2)
           + (2 × 0.40 × 0.60 × 0.25 × 0.06 × 0.16)
         = 0.000576 + 0.009216 + 0.001152
         = 0.010944

volatility = sqrt(0.010944) = 0.1046 = 10.46%
```

The correlation term is essential. When the IG/equity correlation is changed from 0.25 to 0.50 in both cells, the program calculates 11.00% benchmark volatility. A 1.3 correlation produces a clear input error instead of an output.

## Mandate check

Candidate E in `mandate.py` is Meridian's 40% investment-grade bond / 60% equity benchmark. It fails one checkable rule: reserve-eligible weight is 0.0%, below the 3.0% minimum. This confirms that the client benchmark is not itself mandate-compliant.

## Partner swap

My partner shared their Lab 14 `portfolio.py` implementation and Lab 14 record. I reviewed the implementation: it uses the same course inputs, creates the covariance matrix as correlation × volatility × volatility, defines the three required baselines, validates correlation bounds and symmetry, and contains a clear rejection path for a 1.3 IG/equity correlation.

The partner code was shared as email/chat text, which does not preserve runnable Python indentation. The final execution step remains: obtain the actual `portfolio.py` file, run it, verify the three known-answer outputs, then change both IG/equity correlation cells to 1.3 and confirm the rejection. The partner's original file must be restored unchanged after the temporary test.

## Code explanation

`covariance_matrix` multiplies each pair's correlation by the two sleeve volatilities. `portfolio_variance` loops through every ordered sleeve pair and adds `weight_i × covariance_i,j × weight_j`; this includes both cross terms, which is why the formula captures diversification. `portfolio_volatility` takes the square root of that variance so the final result is reported in the same percent units as volatility.

## AI use

AI drafted the standard-library implementation and helped run the validation checks. I accepted the suggestion to validate both correlation bounds and table symmetry because those checks prevent invalid covariance inputs. I verified the benchmark calculation independently with the formula above.
