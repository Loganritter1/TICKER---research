"""Tesla peer P/E reference using September 10, 2026 closing prices.

Educational use only; not investment advice.
"""

from asbury_pe_comps import implied_price, meaningful_price_and_eps, print_estimate, usable_peers


# Prices are USD closing prices on September 10, 2026. EPS is FY2025 GAAP diluted EPS.
TARGET = {"ticker": "TSLA", "name": "Tesla", "price": 363.56, "eps": 1.08}
PEERS = [
    {"ticker": "GM", "name": "General Motors", "price": 86.12, "eps": 3.27},
]


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

    # One qualified peer is a reference estimate, not a peer range.
    full_pe = peers[0]["pe"]
    print_estimate("Reference estimate (one qualified peer)", full_pe, TARGET)

    print("Leave-one-peer-out analysis:")
    full_estimate = implied_price(full_pe, TARGET)
    print("Prediction: removing GM leaves no usable peer and therefore no estimate.")
    print("Remove GM: no estimate (no peers remain).")
    print(f"Full-peer reference used for the check: ${full_estimate:,.2f}.")


if __name__ == "__main__":
    main()
