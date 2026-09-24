"""Lab 10: Tesla five-year pro-forma and FCFE valuation (USD millions).

This is an educational base case, not investment advice.  All opening balances
and historical ratios are tied to Tesla's FY2025 Form 10-K.  The code calculates
cash last and refuses a balance sheet that does not balance.
"""


YEARS = [2026, 2027, 2028, 2029, 2030]

# The key Tesla-specific line is energy generation and storage.  It is modeled
# separately because its reported growth and gross margin differ from automotive.
ASSUMPTIONS = {
    "automotive_growth": [0.00, 0.04, 0.05, 0.05, 0.04],
    "energy_growth": [0.20, 0.18, 0.15, 0.12, 0.10],
    "services_growth": [0.08, 0.07, 0.06, 0.05, 0.04],
    "gross_margin": [0.180, 0.185, 0.190, 0.195, 0.200],
    "sga_to_gross_profit": [0.340, 0.325, 0.315, 0.305, 0.300],
    "rnd_to_revenue": [0.070, 0.065, 0.060, 0.058, 0.055],
    "stock_comp_to_revenue": 2_825.0 / 94_827.0,
    "depreciation_to_opening_ppe": 5_030.0 / 40_643.0,
    "capex": [20_000.0, 16_000.0, 14_000.0, 13_000.0, 12_000.0],
    "inventory_days": 12_392.0 / 77_733.0 * 365.0,
    "other_assets_to_revenue": 40_712.0 / 94_827.0,
    "other_liabilities_to_revenue": 46_565.0 / 94_827.0,
    "tax_rate": 1_423.0 / 5_278.0,
    "debt_rate": 0.040,
    "debt_repayment": 500.0,
    "minimum_cash": 4_000.0,
    "revolver_limit": 0.0,
    "revolver_rate": 0.060,
    "cost_of_equity": 0.100,
    "terminal_growth": 0.025,
    "shares_outstanding": 3_528.0,
}

# FY2025 opening balance sheet.  "Other" lines aggregate reported accounts so
# the model can focus on the operating drivers without typing a cash plug.
OPENING = {
    "automotive_revenue": 69_526.0,
    "energy_revenue": 12_771.0,
    "services_revenue": 12_530.0,
    "inventory": 12_392.0,
    "ppe": 40_643.0,
    "short_term_investments": 27_546.0,
    "other_assets": 40_712.0,
    "cash": 16_513.0,
    "debt": 8_376.0,
    "revolver": 0.0,
    "other_liabilities": 46_565.0,
    "equity": 82_865.0,
}


def print_table(title, rows):
    print(f"\n{title}")
    print(f"{'USD millions':<34}" + "".join(f"FY{year}E".rjust(13) for year in YEARS))
    for label, values in rows:
        print(f"{label:<34}" + "".join(f"{value:>13,.1f}" for value in values))


def assert_balanced(year, gap, cash):
    """Refuse a broken balance sheet or a model below the cash floor."""
    if abs(gap) > 0.05:
        raise AssertionError(f"FY{year}E balance-sheet gap: {gap:.1f}")
    if cash < ASSUMPTIONS["minimum_cash"] - 0.05:
        raise AssertionError(f"FY{year}E cash below minimum: {cash:.1f}")


def build_projection():
    balances = OPENING.copy()
    projection = []

    for index, year in enumerate(YEARS):
        automotive = balances["automotive_revenue"] * (1 + ASSUMPTIONS["automotive_growth"][index])
        energy = balances["energy_revenue"] * (1 + ASSUMPTIONS["energy_growth"][index])
        services = balances["services_revenue"] * (1 + ASSUMPTIONS["services_growth"][index])
        revenue = automotive + energy + services
        gross_profit = revenue * ASSUMPTIONS["gross_margin"][index]
        sga = gross_profit * ASSUMPTIONS["sga_to_gross_profit"][index]
        rnd = revenue * ASSUMPTIONS["rnd_to_revenue"][index]
        depreciation = balances["ppe"] * ASSUMPTIONS["depreciation_to_opening_ppe"]
        operating_income = gross_profit - sga - rnd - depreciation
        interest = balances["debt"] * ASSUMPTIONS["debt_rate"] + balances["revolver"] * ASSUMPTIONS["revolver_rate"]
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * ASSUMPTIONS["tax_rate"]
        net_income = pretax_income - tax
        stock_comp = revenue * ASSUMPTIONS["stock_comp_to_revenue"]

        cost_of_revenue = revenue - gross_profit
        inventory = cost_of_revenue * ASSUMPTIONS["inventory_days"] / 365.0
        ppe = balances["ppe"] + ASSUMPTIONS["capex"][index] - depreciation
        other_assets = revenue * ASSUMPTIONS["other_assets_to_revenue"]
        other_liabilities = revenue * ASSUMPTIONS["other_liabilities_to_revenue"]
        debt = max(0.0, balances["debt"] - ASSUMPTIONS["debt_repayment"])
        equity = balances["equity"] + net_income + stock_comp

        fcfe = (
            net_income + depreciation + stock_comp - ASSUMPTIONS["capex"][index]
            - (inventory - balances["inventory"])
            - (other_assets - balances["other_assets"])
            + (other_liabilities - balances["other_liabilities"])
            - (balances["debt"] - debt)
        )
        cash = balances["cash"] + fcfe
        short_term_investments = balances["short_term_investments"]
        # Treasury investments are reported cash-like liquidity.  Selling them
        # reclassifies an asset to cash; it does not create operating cash flow.
        if cash < ASSUMPTIONS["minimum_cash"]:
            investment_sale = min(short_term_investments, ASSUMPTIONS["minimum_cash"] - cash)
            short_term_investments -= investment_sale
            cash += investment_sale
        revolver = balances["revolver"]
        if cash < ASSUMPTIONS["minimum_cash"]:
            draw = min(ASSUMPTIONS["revolver_limit"] - revolver, ASSUMPTIONS["minimum_cash"] - cash)
            revolver += draw
            cash += draw
        elif revolver > 0.0:
            repayment = min(revolver, cash - ASSUMPTIONS["minimum_cash"])
            revolver -= repayment
            cash -= repayment

        assets = cash + short_term_investments + inventory + ppe + other_assets
        liabilities = debt + revolver + other_liabilities
        gap = assets - liabilities - equity
        assert_balanced(year, gap, cash)
        projection.append(locals().copy())
        balances = {
            "automotive_revenue": automotive, "energy_revenue": energy, "services_revenue": services,
            "inventory": inventory, "ppe": ppe, "short_term_investments": short_term_investments,
            "other_assets": other_assets, "cash": cash,
            "debt": debt, "revolver": revolver, "other_liabilities": other_liabilities, "equity": equity,
        }
    return projection


def values(projection):
    ke, g = ASSUMPTIONS["cost_of_equity"], ASSUMPTIONS["terminal_growth"]
    # This loss-making FCFE period is not assigned a negative perpetuity value.
    # Only positive annual FCFE is valued; the terminal value begins with 2030.
    pv_fcfe = sum(max(0.0, row["fcfe"]) / (1 + ke) ** (i + 1) for i, row in enumerate(projection))
    terminal_value = projection[-1]["fcfe"] * (1 + g) / (ke - g)
    pv_terminal = terminal_value / (1 + ke) ** len(projection)
    equity_value = pv_fcfe + pv_terminal
    return equity_value, pv_terminal / equity_value, equity_value / ASSUMPTIONS["shares_outstanding"]


def main():
    projection = build_projection()
    series = lambda key: [row[key] for row in projection]
    print_table("Income Statement", [("Automotive revenue", series("automotive")), ("Energy revenue", series("energy")),
        ("Services revenue", series("services")), ("Total revenue", series("revenue")),
        ("Gross profit", series("gross_profit")), ("SG&A", series("sga")), ("R&D", series("rnd")),
        ("Depreciation", series("depreciation")), ("Stock compensation", series("stock_comp")),
        ("Operating income", series("operating_income")),
        ("Interest", series("interest")), ("Tax", series("tax")), ("Net income", series("net_income"))])
    print_table("Balance Sheet", [("Inventory", series("inventory")), ("PP&E", series("ppe")),
        ("Short-term investments", series("short_term_investments")), ("Other assets", series("other_assets")),
        ("Cash", series("cash")), ("Debt", series("debt")),
        ("Revolver", series("revolver")), ("Other liabilities", series("other_liabilities")), ("Equity", series("equity"))])
    print_table("Cash Flow", [("Net income", series("net_income")), ("Depreciation", series("depreciation")),
        ("Stock compensation", series("stock_comp")),
        ("Capital spending", [-ASSUMPTIONS["capex"][i] for i in range(len(YEARS))]),
        ("Free cash flow to equity", series("fcfe"))])
    print_table("Checks", [("Assets - liabilities - equity", series("gap")),
        ("Cash at or above minimum", [row["cash"] - ASSUMPTIONS["minimum_cash"] for row in projection])])
    equity_value, terminal_share, value_per_share = values(projection)
    print(f"\nEquity value: ${equity_value:,.1f} million")
    print(f"Share of value after 2030: {terminal_share:.1%}")
    print(f"Value per share: ${value_per_share:,.2f}")


if __name__ == "__main__":
    main()
