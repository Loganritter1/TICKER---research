"""Comparable-company P/E calculator using the Lab 07 frozen Asbury inputs."""

**Disclaimer**  I am not a licensed financial professional. This document is for educational purposes only and is not investment advice.

from statistics import median


# Editable inputs.  Prices are USD per share; EPS is total GAAP diluted EPS.
TARGET = {"ticker": "ABG", "name": "Asbury Automotive", "price": 243.03, "eps": 21.50}
PEERS = [
    {"ticker": "AN", "name": "AutoNation", "price": 169.84, "eps": 16.92},
    {"ticker": "GPI", "name": "Group 1 Automotive", "price": 421.48, "eps": 36.81},
]


def meaningful_price_and_eps(company):
    """Return whether a company has inputs suitable for a P/E calculation."""
    return company.get("price") is not None and company.get("eps") is not None and company["price"] > 0 and company["eps"] > 0


def usable_peers(target, peers):
    """Remove the target, duplicate tickers, and peers without meaningful P/E inputs."""
    unique_peers = []
    seen_tickers = {target["ticker"]}
    for peer in peers:
        ticker = peer.get("ticker")
        if ticker in seen_tickers:
            print(f"{ticker}: excluded (target or duplicate ticker).")
            continue
        seen_tickers.add(ticker)
        if not meaningful_price_and_eps(peer):
            print(f"{ticker}: P/E not meaningful (missing or nonpositive price or EPS).")
            continue
        peer = peer.copy()
        peer["pe"] = peer["price"] / peer["eps"]
        unique_peers.append(peer)
    return unique_peers


def implied_price(pe_multiple, target):
    if not meaningful_price_and_eps(target):
        return None
    return pe_multiple * target["eps"]


def print_estimate(label, pe_multiple, target):
    value = implied_price(pe_multiple, target)
    if value is None:
        print(f"{label}: not meaningful (target price or EPS is missing or nonpositive).")
    else:
        print(f"{label}: {pe_multiple:.6f}x -> ${value:,.2f}")


def format_dollar_change(value):
    """Format a signed dollar amount with the sign before the currency symbol."""
    return f"{'-' if value < 0 else '+'}${abs(value):,.2f}"


def main():
    print(f"Target: {TARGET['name']} ({TARGET['ticker']})")
    if not meaningful_price_and_eps(TARGET):
        print("Target implied prices are not meaningful (missing or nonpositive price or EPS).")

    peers = usable_peers(TARGET, PEERS)
    for peer in peers:
        print(f"{peer['name']} ({peer['ticker']}) P/E: {peer['pe']:.6f}x")

    if not peers:
        print("No usable peers; no implied estimate.")
        return

    full_median_pe = median(peer["pe"] for peer in peers)
    if len(peers) == 1:
        print_estimate("Reference estimate (one valid peer)", full_median_pe, TARGET)
    else:
        print_estimate("Minimum peer P/E implied price", min(peer["pe"] for peer in peers), TARGET)
        print_estimate("Median peer P/E implied price", full_median_pe, TARGET)
        print_estimate("Maximum peer P/E implied price", max(peer["pe"] for peer in peers), TARGET)

    print("Leave-one-peer-out analysis:")
    full_estimate = implied_price(full_median_pe, TARGET)
    for removed_peer in peers:
        remaining = [peer for peer in peers if peer["ticker"] != removed_peer["ticker"]]
        if not remaining:
            print(f"Remove {removed_peer['ticker']}: no estimate (no peers remain).")
            continue
        remaining_median = median(peer["pe"] for peer in remaining)
        remaining_estimate = implied_price(remaining_median, TARGET)
        if remaining_estimate is None or full_estimate is None:
            print(f"Remove {removed_peer['ticker']}: not meaningful.")
        else:
            change = remaining_estimate - full_estimate
            print(
                f"Remove {removed_peer['ticker']}: remaining median-implied price "
                f"${remaining_estimate:,.2f}; change from full-peer estimate "
                f"{format_dollar_change(change)}."
            )


if __name__ == "__main__":
    main()
