"""Lab 13: check the Meridian Foundation Reserve's coded mandate rules."""

# Editable inputs
HOLDINGS = {
    "Cash": {"issuer": "none", "redeem_days": 0, "reserve_eligible": True},
    "Treasury bills": {"issuer": "U.S. Treasury", "redeem_days": 1, "reserve_eligible": True},
    "Treasury 10-year note": {"issuer": "U.S. Treasury", "redeem_days": 1, "reserve_eligible": True},
    "Global equity index fund": {"issuer": "diversified fund", "redeem_days": 2, "reserve_eligible": False},
    "Investment-grade bond fund": {"issuer": "diversified fund", "redeem_days": 3, "reserve_eligible": False},
    "Private real estate fund": {"issuer": "diversified fund", "redeem_days": 90, "reserve_eligible": False},
    "Acme Corp bonds": {"issuer": "Acme Corp", "redeem_days": 4, "reserve_eligible": False},
    "Acme Corp stock": {"issuer": "Acme Corp", "redeem_days": 1, "reserve_eligible": False},
}

CANDIDATES = {
    "A": {
        "Cash": 2, "Treasury bills": 2, "Treasury 10-year note": 10,
        "Global equity index fund": 60, "Investment-grade bond fund": 26,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 55, "Investment-grade bond fund": 20,
        "Private real estate fund": 15, "Acme Corp bonds": 5, "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1, "Treasury bills": 1, "Treasury 10-year note": 0,
        "Global equity index fund": 70, "Investment-grade bond fund": 20,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 8,
    },
    # Candidate D passes all coded checks but intentionally raises an S1/S2 suitability question.
    "D": {
        "Cash": 3, "Treasury bills": 0, "Treasury 10-year note": 0,
        "Global equity index fund": 97, "Investment-grade bond fund": 0,
        "Private real estate fund": 0, "Acme Corp bonds": 0, "Acme Corp stock": 0,
    },
}

RESERVE_SIZE = 100  # USD millions
QUARTERLY_DISTRIBUTION = 0.75  # USD millions
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5  # business days
MINIMUM_LIQUID_SHARE = 90  # percent
ISSUER_LIMIT = 8  # percent
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def verdict(value, passes):
    return f"{value:.1f} {'pass' if passes else 'FAIL'}"


def check_candidate(name, weights, reserve_minimum):
    """Print each checkable rule and return the number of failures."""
    failures = 0

    total_weight = sum(weights.values())
    passes = total_weight == 100
    print(f"Weights sum to 100: {verdict(total_weight, passes)}")
    failures += not passes

    lowest_weight = min(weights.values())
    passes = lowest_weight >= 0
    print(f"Long-only (lowest weight): {verdict(lowest_weight, passes)}")
    failures += not passes

    reserve_weight = sum(
        weights[holding] for holding, details in HOLDINGS.items()
        if details["reserve_eligible"]
    )
    passes = reserve_weight >= reserve_minimum
    print(f"Reserve >= {reserve_minimum:.1f}%: {verdict(reserve_weight, passes)}")
    failures += not passes

    liquid_weight = sum(
        weights[holding] for holding, details in HOLDINGS.items()
        if details["redeem_days"] <= LIQUIDITY_WINDOW
    )
    passes = liquid_weight >= MINIMUM_LIQUID_SHARE
    print(f"Redeemable in {LIQUIDITY_WINDOW} days >= {MINIMUM_LIQUID_SHARE:.1f}%: {verdict(liquid_weight, passes)}")
    failures += not passes

    company_weights = {}
    for holding, details in HOLDINGS.items():
        issuer = details["issuer"]
        if issuer not in EXEMPT_ISSUERS:
            company_weights[issuer] = company_weights.get(issuer, 0) + weights[holding]
    largest_company = max(company_weights.values(), default=0)
    passes = largest_company <= ISSUER_LIMIT
    print(f"Largest single company <= {ISSUER_LIMIT:.1f}%: {verdict(largest_company, passes)}")
    failures += not passes

    print("Calendar-year loss: requires CIO clarification")
    if failures == 0:
        print("passes every checkable rule")
    else:
        print(f"fails {failures} rule(s)")


def main():
    reserve_minimum = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    print(f"Reserve minimum: {reserve_minimum:.1f}% of the portfolio")
    for name, weights in CANDIDATES.items():
        print(f"\nCandidate {name}")
        check_candidate(name, weights, reserve_minimum)


if __name__ == "__main__":
    main()
