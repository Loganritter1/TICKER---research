"""Lab 14: price Meridian's three portfolio baselines using course inputs."""

import csv
from math import sqrt


# Editable inputs. Returns and volatilities are annual decimals.
SLEEVES = {
    "Treasury bills": {"return": 0.035, "volatility": 0.005, "reserve_eligible": True},
    "Treasury 10-year note": {"return": 0.043, "volatility": 0.070, "reserve_eligible": True},
    "Investment-grade bond fund": {"return": 0.050, "volatility": 0.060, "reserve_eligible": False},
    "Global equity index fund": {"return": 0.080, "volatility": 0.160, "reserve_eligible": False},
}

CORRELATIONS = {
    "Treasury bills": {
        "Treasury bills": 1.00, "Treasury 10-year note": 0.10,
        "Investment-grade bond fund": 0.05, "Global equity index fund": 0.00,
    },
    "Treasury 10-year note": {
        "Treasury bills": 0.10, "Treasury 10-year note": 1.00,
        "Investment-grade bond fund": 0.80, "Global equity index fund": -0.10,
    },
    "Investment-grade bond fund": {
        "Treasury bills": 0.05, "Treasury 10-year note": 0.80,
        "Investment-grade bond fund": 1.00, "Global equity index fund": 0.25,
    },
    "Global equity index fund": {
        "Treasury bills": 0.00, "Treasury 10-year note": -0.10,
        "Investment-grade bond fund": 0.25, "Global equity index fund": 1.00,
    },
}

OBJECTIVE_RETURN = 0.065  # CPI estimate of 2.5% + 4.0%


def validate_correlations(correlations, sleeves):
    """Reject correlations outside [-1, 1] and tables that are not symmetric."""
    names = list(sleeves)
    for first in names:
        if first not in correlations:
            raise ValueError(f"Correlation table is missing row: {first}")
        for second in names:
            if second not in correlations[first]:
                raise ValueError(f"Correlation table is missing {first} / {second}")
            value = correlations[first][second]
            if not -1 <= value <= 1:
                raise ValueError(
                    f"Correlation for {first} / {second} is {value}; it must be between -1 and 1."
                )
            if value != correlations.get(second, {}).get(first):
                raise ValueError(f"Correlation table is not symmetric at {first} / {second}.")


def covariance_matrix(sleeves, correlations):
    """Return covariance[i][j] = correlation[i][j] * volatility[i] * volatility[j]."""
    return {
        first: {
            second: correlations[first][second]
            * sleeves[first]["volatility"]
            * sleeves[second]["volatility"]
            for second in sleeves
        }
        for first in sleeves
    }


def equal_weight_portfolio(sleeves):
    """Give every sleeve the same portfolio weight."""
    return {name: 1 / len(sleeves) for name in sleeves}


def inverse_volatility_portfolio(sleeves):
    """Weight each sleeve by 1 / volatility, then scale the weights to sum to one."""
    raw_weights = {name: 1 / details["volatility"] for name, details in sleeves.items()}
    total = sum(raw_weights.values())
    return {name: weight / total for name, weight in raw_weights.items()}


def expected_return(weights, sleeves):
    """Calculate the weighted-average expected return."""
    return sum(weights[name] * sleeves[name]["return"] for name in sleeves)


def portfolio_variance(weights, covariance):
    """Calculate sum_i sum_j weight_i * covariance_i,j * weight_j."""
    return sum(
        weights[first] * covariance[first][second] * weights[second]
        for first in weights
        for second in weights
    )


def portfolio_volatility(weights, covariance):
    """Calculate the square root of portfolio variance."""
    return sqrt(portfolio_variance(weights, covariance))


def reserve_eligible_weight(weights, sleeves):
    """Add the weights of bills and the 10-year note, the reserve-eligible sleeves."""
    return sum(weights[name] for name in sleeves if sleeves[name]["reserve_eligible"])


def lowest_risk_mix(sleeves, correlations, objective_return, minimum_reserve_weight, step=0.05):
    """Return the lowest-volatility long-only mix meeting the mandate, or None.

    The search uses whole ``step`` increments (5% by default), so every returned
    weight is non-negative and the weights add to 100%.
    """
    if not 0 < step <= 1:
        raise ValueError("Step must be greater than 0 and no more than 1.")
    increments = round(1 / step)
    if abs(increments * step - 1) > 1e-9:
        raise ValueError("Step must divide 100% evenly.")
    if not 0 <= minimum_reserve_weight <= 1:
        raise ValueError("Minimum reserve weight must be between 0% and 100%.")

    validate_correlations(correlations, sleeves)
    names = list(sleeves)
    covariance = covariance_matrix(sleeves, correlations)
    best_weights = None
    best_volatility = None

    def try_weights(position, remaining, counts):
        nonlocal best_weights, best_volatility
        if position == len(names) - 1:
            weights = {
                name: count * step
                for name, count in zip(names, [*counts, remaining])
            }
            if expected_return(weights, sleeves) < objective_return:
                return
            if reserve_eligible_weight(weights, sleeves) < minimum_reserve_weight:
                return
            volatility = portfolio_volatility(weights, covariance)
            if best_volatility is None or volatility < best_volatility:
                best_weights = weights
                best_volatility = volatility
            return

        for count in range(remaining + 1):
            try_weights(position + 1, remaining - count, [*counts, count])

    try_weights(0, increments, [])
    return best_weights


def estimate_from_prices(csv_source, last_36_months=False):
    """Estimate annual returns, volatility, and correlations from monthly prices.

    ``csv_source`` may be a CSV path, text, or bytes. Its first column must be a
    date and each remaining column must contain chronological monthly prices.
    Returns are historical estimates: mean monthly return * 12 and sample
    standard deviation of monthly returns * sqrt(12).
    """
    if isinstance(csv_source, bytes):
        rows = list(csv.DictReader(csv_source.decode("utf-8-sig").splitlines()))
    elif isinstance(csv_source, str) and "\n" not in csv_source:
        with open(csv_source, newline="", encoding="utf-8-sig") as price_file:
            rows = list(csv.DictReader(price_file))
    else:
        rows = list(csv.DictReader(csv_source.splitlines()))

    if not rows or not rows[0]:
        raise ValueError("Prices CSV must contain a header and at least two rows.")
    columns = list(rows[0])
    if len(columns) < 3:
        raise ValueError("Prices CSV needs a date column and at least two ticker columns.")
    tickers = columns[1:]
    prices = {ticker: [] for ticker in tickers}
    for row_number, row in enumerate(rows, start=2):
        for ticker in tickers:
            try:
                price = float(row[ticker])
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError(f"Invalid price for {ticker} on CSV row {row_number}.") from error
            if price <= 0:
                raise ValueError(f"Price for {ticker} on CSV row {row_number} must be positive.")
            prices[ticker].append(price)

    monthly_returns = {
        ticker: [later / earlier - 1 for earlier, later in zip(values, values[1:])]
        for ticker, values in prices.items()
    }
    if last_36_months:
        monthly_returns = {ticker: values[-36:] for ticker, values in monthly_returns.items()}
    observations = len(next(iter(monthly_returns.values())))
    if observations < 2:
        raise ValueError("Prices CSV needs at least three monthly prices.")

    means = {ticker: sum(values) / observations for ticker, values in monthly_returns.items()}
    monthly_volatilities = {
        ticker: sqrt(sum((value - means[ticker]) ** 2 for value in values) / (observations - 1))
        for ticker, values in monthly_returns.items()
    }
    if any(volatility == 0 for volatility in monthly_volatilities.values()):
        raise ValueError("Each ticker needs variation in monthly returns to estimate correlations.")

    sleeves = {
        ticker: {
            "return": means[ticker] * 12,
            "volatility": monthly_volatilities[ticker] * sqrt(12),
            "reserve_eligible": False,
        }
        for ticker in tickers
    }
    correlations = {ticker: {} for ticker in tickers}
    for first_index, first in enumerate(tickers):
        for second_index, second in enumerate(tickers):
            if first == second:
                correlations[first][second] = 1.0
            elif second_index < first_index:
                correlations[first][second] = correlations[second][first]
            else:
                correlations[first][second] = sum(
                    (left - means[first]) * (right - means[second])
                    for left, right in zip(monthly_returns[first], monthly_returns[second])
                ) / ((observations - 1) * monthly_volatilities[first] * monthly_volatilities[second])
    return sleeves, correlations


def print_portfolio(name, weights, sleeves, covariance, objective_return):
    """Print a portfolio's inputs-derived weights and metrics."""
    print(f"\n{name}")
    print("Weights:")
    for sleeve, weight in weights.items():
        print(f"  {sleeve}: {weight:.1%}")
    result_return = expected_return(weights, sleeves)
    result_volatility = portfolio_volatility(weights, covariance)
    reserve_weight = reserve_eligible_weight(weights, sleeves)
    print(f"Expected return: {result_return:.2%}")
    print(f"Volatility: {result_volatility:.2%}")
    print(f"Reserve-eligible: {reserve_weight:.1%}")
    print(f"Meets {objective_return:.1%} objective: {'yes' if result_return >= objective_return else 'no'}")


def main():
    validate_correlations(CORRELATIONS, SLEEVES)
    covariance = covariance_matrix(SLEEVES, CORRELATIONS)
    portfolios = {
        "Benchmark": {
            "Treasury bills": 0.0,
            "Treasury 10-year note": 0.0,
            "Investment-grade bond fund": 0.4,
            "Global equity index fund": 0.6,
        },
        "Equal weight": equal_weight_portfolio(SLEEVES),
        "Inverse volatility": inverse_volatility_portfolio(SLEEVES),
    }
    for name, weights in portfolios.items():
        print_portfolio(name, weights, SLEEVES, covariance, OBJECTIVE_RETURN)


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"Input error: {error}")
