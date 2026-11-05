"""Tesla/GM September 30, 2026 comparable-company reference calculations.

The calculation is deliberately a qualified reference, not a peer range.
GM's dealer distribution, ICE-heavy mix, and GM Financial business differ
materially from Tesla's direct-sales, EV, energy-storage, and services mix.
"""


VALUATION_DATE = "2026-09-30"

TESLA = {
    "price": 354.81,
    "diluted_shares": 3_528.0,
    "cash_and_short_term_investments": 44_059.0,
    "debt_and_finance_leases": 8_376.0,
    "revenue": 94_827.0,
    "gaap_diluted_eps": 1.08,
}

GM = {
    "price": 77.00,
    "shares_outstanding": 903.968,
    "automotive_cash_and_securities": 21_700.0,
    "automotive_debt": 16_247.0,
    "automotive_revenue": 167_970.0,
    "gaap_diluted_eps": 3.27,
}


def enterprise_value(market_cap, debt, cash):
    return market_cap + debt - cash


def main():
    tesla_market_cap = TESLA["price"] * TESLA["diluted_shares"]
    tesla_ev = enterprise_value(
        tesla_market_cap,
        TESLA["debt_and_finance_leases"],
        TESLA["cash_and_short_term_investments"],
    )
    gm_market_cap = GM["price"] * GM["shares_outstanding"]
    gm_automotive_ev = enterprise_value(
        gm_market_cap,
        GM["automotive_debt"],
        GM["automotive_cash_and_securities"],
    )
    gm_ev_revenue = gm_automotive_ev / GM["automotive_revenue"]
    tesla_ev_revenue = tesla_ev / TESLA["revenue"]
    tesla_ev_implied = gm_ev_revenue * TESLA["revenue"]
    tesla_equity_implied = (
        tesla_ev_implied
        + TESLA["cash_and_short_term_investments"]
        - TESLA["debt_and_finance_leases"]
    )
    tesla_ev_revenue_price = tesla_equity_implied / TESLA["diluted_shares"]
    gm_pe = GM["price"] / GM["gaap_diluted_eps"]
    tesla_pe_implied_price = gm_pe * TESLA["gaap_diluted_eps"]

    print(f"Qualified Tesla/GM reference | Valuation date: {VALUATION_DATE}")
    print(f"Tesla market capitalization: ${tesla_market_cap:,.1f} million")
    print(f"Tesla enterprise value: ${tesla_ev:,.1f} million")
    print(f"Tesla EV / FY2025 revenue: {tesla_ev_revenue:.2f}x")
    print(f"GM automotive enterprise value: ${gm_automotive_ev:,.1f} million")
    print(f"GM automotive EV / FY2025 automotive revenue: {gm_ev_revenue:.2f}x")
    print(f"GM EV/revenue-implied TSLA reference: ${tesla_ev_revenue_price:.2f} per diluted share")
    print(f"GM P/E: {gm_pe:.2f}x")
    print(f"GM P/E-implied TSLA reference: ${tesla_pe_implied_price:.2f} per diluted share")
    print("Qualification: one-peer references only; do not present as a peer range.")


if __name__ == "__main__":
    main()
