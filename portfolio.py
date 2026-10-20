"""Lab 14: price Meridian's three portfolio baselines using course inputs."""

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
