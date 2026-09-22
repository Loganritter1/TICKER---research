"""Lab 09: ABG five-year pro-forma and FCFE valuation (USD millions)."""


YEARS = [2026, 2027, 2028, 2029, 2030]

ASSUMPTIONS = {
    "growth": 0.018,
    "gross_margin": 0.1705,
    "sga_to_gross_profit": [0.665, 0.655, 0.645, 0.645, 0.645],
    "depreciation_to_opening_ppe": 82.4 / 3070.4,
    "impairment": 120.0,
    "capex": 250.0,
    "tax_rate": 0.255,
    "inventory_days": 2135.8 / (17999.0 - 3071.7) * 365,
    "floor_plan_to_inventory": 2027.0 / 2135.8,
    "other_working_capital_rate": 0.008,
    "minimum_cash": 25.0,
    "revolver_limit": 850.0,
    "revolver_rate": 0.06,
    "debt_repayment": 150.0,
    "buyback": 150.0,
    "floor_plan_rate": 0.0467,
    "term_debt_rate": 0.0544,
    "cost_of_equity": 0.10,
    "terminal_growth": 0.025,
    "shares_outstanding": 17.951349,
}

OPENING = {
    "revenue": 17999.0,
    "inventory": 2135.8,
    "ppe": 3070.4,
    "other_assets": 6371.6,
    "cash": 40.4,
    "floor_plan": 2027.0,
    "debt": 3572.0,
    "revolver": 0.0,
    "other_liabilities": 2127.5,
    "equity": 3891.7,
}


def print_table(title, rows):
    """Print a statement with fiscal years across and one-decimal values."""
    print(f"\n{title}")
    print(f"{'USD millions':<32}" + "".join(f"FY{year}E".rjust(12) for year in YEARS))
    for label, values in rows:
        print(f"{label:<32}" + "".join(f"{value:>12.1f}" for value in values))


def assert_balanced(year, gap, cash):
    """Refuse a year whose balance sheet or minimum-cash check fails."""
    if abs(gap) > 0.05:
        raise AssertionError(f"FY{year}E balance-sheet gap: {gap:.1f}")
    if cash < ASSUMPTIONS["minimum_cash"] - 0.05:
        raise AssertionError(
            f"FY{year}E cash below minimum: {cash:.1f} "
            f"(minimum {ASSUMPTIONS['minimum_cash']:.1f})"
        )


def build_projection():
    """Build the income statement, balance sheet, and cash flow in model order."""
    balances = OPENING.copy()
    projection = []

    for index, year in enumerate(YEARS):
        revenue = balances["revenue"] * (1 + ASSUMPTIONS["growth"])
        gross_profit = revenue * ASSUMPTIONS["gross_margin"]
        sga = gross_profit * ASSUMPTIONS["sga_to_gross_profit"][index]
        depreciation = balances["ppe"] * ASSUMPTIONS["depreciation_to_opening_ppe"]
        impairment = ASSUMPTIONS["impairment"]
        operating_income = gross_profit - sga - depreciation - impairment
        interest = (
            balances["floor_plan"] * ASSUMPTIONS["floor_plan_rate"]
            + balances["debt"] * ASSUMPTIONS["term_debt_rate"]
            + balances["revolver"] * ASSUMPTIONS["revolver_rate"]
        )
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * ASSUMPTIONS["tax_rate"]
        net_income = pretax_income - tax

        inventory = (revenue - gross_profit) * ASSUMPTIONS["inventory_days"] / 365
        floor_plan = inventory * ASSUMPTIONS["floor_plan_to_inventory"]
        ppe = balances["ppe"] + ASSUMPTIONS["capex"] - depreciation
        other_working_capital = ASSUMPTIONS["other_working_capital_rate"] * (
            revenue - balances["revenue"]
        )
        other_assets = balances["other_assets"] + other_working_capital - impairment
        debt = balances["debt"] - ASSUMPTIONS["debt_repayment"]
        other_liabilities = balances["other_liabilities"]
        equity = balances["equity"] + net_income - ASSUMPTIONS["buyback"]

        fcfe = (
            net_income
            + depreciation
            + impairment
            - ASSUMPTIONS["capex"]
            - (inventory - balances["inventory"])
            - other_working_capital
            + (floor_plan - balances["floor_plan"])
            - ASSUMPTIONS["debt_repayment"]
        )
        cash = balances["cash"] + fcfe - ASSUMPTIONS["buyback"]

        revolver = balances["revolver"]
        if cash < ASSUMPTIONS["minimum_cash"]:
            draw = min(ASSUMPTIONS["revolver_limit"] - revolver, ASSUMPTIONS["minimum_cash"] - cash)
            revolver += draw
            cash += draw
        elif revolver > 0.0:
            repayment = min(revolver, cash - ASSUMPTIONS["minimum_cash"])
            revolver -= repayment
            cash -= repayment

        assets = cash + inventory + ppe + other_assets
        liabilities = floor_plan + debt + revolver + other_liabilities
        gap = assets - liabilities - equity
        assert_balanced(year, gap, cash)

        projection.append(
            {
                "year": year,
                "revenue": revenue,
                "gross_profit": gross_profit,
                "sga": sga,
                "depreciation": depreciation,
                "impairment": impairment,
                "operating_income": operating_income,
                "interest": interest,
                "pretax_income": pretax_income,
                "tax": tax,
                "net_income": net_income,
                "inventory": inventory,
                "ppe": ppe,
                "other_assets": other_assets,
                "cash": cash,
                "floor_plan": floor_plan,
                "debt": debt,
                "revolver": revolver,
                "other_liabilities": other_liabilities,
                "equity": equity,
                "fcfe": fcfe,
                "other_working_capital": other_working_capital,
                "gap": gap,
            }
        )
        balances = {
            "revenue": revenue,
            "inventory": inventory,
            "ppe": ppe,
            "other_assets": other_assets,
            "cash": cash,
            "floor_plan": floor_plan,
            "debt": debt,
            "revolver": revolver,
            "other_liabilities": other_liabilities,
            "equity": equity,
        }
    return projection


def values(projection):
    """Value equity from FCFE and a terminal value at the cost of equity."""
    cost_of_equity = ASSUMPTIONS["cost_of_equity"]
    terminal_growth = ASSUMPTIONS["terminal_growth"]
    pv_fcfe = sum(row["fcfe"] / (1 + cost_of_equity) ** (index + 1) for index, row in enumerate(projection))
    terminal_value = (
        (projection[-1]["fcfe"] + ASSUMPTIONS["debt_repayment"])
        * (1 + terminal_growth)
        / (cost_of_equity - terminal_growth)
    )
    pv_terminal_value = terminal_value / (1 + cost_of_equity) ** len(projection)
    equity_value = pv_fcfe + pv_terminal_value
    return equity_value, pv_terminal_value / equity_value, equity_value / ASSUMPTIONS["shares_outstanding"]


def main():
    projection = build_projection()
    series = lambda key: [row[key] for row in projection]
    print_table("Income Statement", [
        ("Revenue", series("revenue")),
        ("Gross profit", series("gross_profit")),
        ("SG&A", series("sga")),
        ("Depreciation", series("depreciation")),
        ("Impairment", series("impairment")),
        ("Operating income", series("operating_income")),
        ("Interest", series("interest")),
        ("Pretax income", series("pretax_income")),
        ("Tax", series("tax")),
        ("Net income", series("net_income")),
    ])
    print_table("Balance Sheet", [
        ("Inventory", series("inventory")),
        ("PP&E", series("ppe")),
        ("Other assets", series("other_assets")),
        ("Cash", series("cash")),
        ("Floor plan", series("floor_plan")),
        ("Term debt", series("debt")),
        ("Revolver", series("revolver")),
        ("Other liabilities", series("other_liabilities")),
        ("Equity", series("equity")),
    ])
    print_table("Cash Flow", [
        ("Net income", series("net_income")),
        ("Depreciation", series("depreciation")),
        ("Impairment", series("impairment")),
        ("Capital spending", [-ASSUMPTIONS["capex"]] * len(YEARS)),
        ("Change in inventory", [row["inventory"] - (OPENING["inventory"] if index == 0 else projection[index - 1]["inventory"]) for index, row in enumerate(projection)]),
        ("Change in other working capital", series("other_working_capital")),
        ("Change in floor plan", [row["floor_plan"] - (OPENING["floor_plan"] if index == 0 else projection[index - 1]["floor_plan"]) for index, row in enumerate(projection)]),
        ("Debt repayment", [-ASSUMPTIONS["debt_repayment"]] * len(YEARS)),
        ("Free cash flow to equity", series("fcfe")),
    ])
    print_table("Checks", [
        ("Assets - liabilities - equity", series("gap")),
        ("Cash at or above minimum", [row["cash"] - ASSUMPTIONS["minimum_cash"] for row in projection]),
    ])
    equity_value, terminal_share, value_per_share = values(projection)
    print(f"\nEquity value: ${equity_value:,.1f} million")
    print(f"Share of value after 2030: {terminal_share:.1%}")
    print(f"Value per share: ${value_per_share:,.2f}")


if __name__ == "__main__":
    main()
