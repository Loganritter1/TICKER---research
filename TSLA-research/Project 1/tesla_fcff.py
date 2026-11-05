"""Tesla FCFF valuation engine for FIN 43900 Project 1.

All amounts are USD millions unless stated otherwise.  This is an educational
model, not investment advice.  FY2025 is the filing-based base year and the
valuation date is September 30, 2026.  The WACC and market-price inputs remain
explicit assumptions until the final dated-source reconciliation is complete.
"""

from copy import deepcopy


VALUATION_DATE = "2026-09-30"
MARKET_PRICE = 354.81
YEARS = [2026, 2027, 2028, 2029, 2030]

# Frozen September 30, 2026 market inputs. The share figure is FY2025 diluted
# weighted-average shares, deliberately used as a valuation convention rather
# than represented as a September 30 spot share count.
WACC_INPUTS = {
    "risk_free_rate": 0.0529,
    "beta": 1.85,
    "equity_risk_premium": 0.0500,
    "pre_tax_cost_of_debt": 0.0400,
    "tax_rate": 0.27,
    "market_price": MARKET_PRICE,
    "diluted_shares": 3_528.0,
    "debt_and_finance_leases": 8_376.0,
}
WACC_INPUTS["cost_of_equity"] = (
    WACC_INPUTS["risk_free_rate"]
    + WACC_INPUTS["beta"] * WACC_INPUTS["equity_risk_premium"]
)
WACC_INPUTS["market_capitalization"] = (
    WACC_INPUTS["market_price"] * WACC_INPUTS["diluted_shares"]
)
WACC_INPUTS["equity_weight"] = WACC_INPUTS["market_capitalization"] / (
    WACC_INPUTS["market_capitalization"] + WACC_INPUTS["debt_and_finance_leases"]
)
WACC_INPUTS["debt_weight"] = 1 - WACC_INPUTS["equity_weight"]
WACC_INPUTS["wacc"] = (
    WACC_INPUTS["equity_weight"] * WACC_INPUTS["cost_of_equity"]
    + WACC_INPUTS["debt_weight"]
    * WACC_INPUTS["pre_tax_cost_of_debt"]
    * (1 - WACC_INPUTS["tax_rate"])
)

# FY2025 amounts from Tesla's Form 10-K, filed January 29, 2026.  The balance
# sheet is intentionally simplified but remains fully linked and balanced.
OPENING = {
    "automotive_revenue": 69_526.0,
    "energy_revenue": 12_771.0,
    "services_revenue": 12_530.0,
    "cash": 16_513.0,
    "short_term_investments": 27_546.0,
    "inventory": 12_392.0,
    "ppe": 40_643.0,
    "other_assets": 40_712.0,
    "debt_and_finance_leases": 8_376.0,
    "other_liabilities": 46_565.0,
    "equity": 82_865.0,
}

ASSUMPTIONS = {
    # Company-specific operating drivers.
    "automotive_growth": [0.00, 0.04, 0.05, 0.05, 0.04],
    "energy_growth": [0.20, 0.18, 0.15, 0.12, 0.10],
    "services_growth": [0.08, 0.07, 0.06, 0.05, 0.04],
    "gross_margin": [0.180, 0.185, 0.190, 0.195, 0.200],
    "sga_to_gross_profit": [0.340, 0.325, 0.315, 0.305, 0.300],
    "rnd_to_revenue": [0.070, 0.065, 0.060, 0.058, 0.055],
    "capex": [20_000.0, 16_000.0, 14_000.0, 13_000.0, 12_000.0],
    "depreciation_to_opening_ppe": 5_030.0 / 40_643.0,
    "stock_comp_to_revenue": 2_825.0 / 94_827.0,
    "inventory_days": 12_392.0 / 77_733.0 * 365.0,
    "other_assets_to_revenue": 40_712.0 / 94_827.0,
    "other_liabilities_to_revenue": 46_565.0 / 94_827.0,
    "debt_rate": 0.040,
    "tax_rate": 1_423.0 / 5_278.0,
    # September 30 WACC: 5.29% risk-free rate + 1.85 beta x 5.0% ERP gives a
    # 14.54% cost of equity.  Market-value weighting with 4.0% pre-tax cost of
    # debt and 27.0% tax rate gives a 14.46% WACC.
    "wacc": WACC_INPUTS["wacc"],
    "terminal_growth": 0.030,
    "diluted_shares": 3_528.0,
    # Base bridge policy treats all unrestricted cash and short-term
    # investments as non-operating. A USD 10bn operating-cash reserve is
    # reported as a separate bridge sensitivity, not embedded in base value.
    "operating_cash_reserve": 0.0,
}


def assert_balanced(year, gap):
    """Fail loudly if the forecast balance sheet does not articulate."""
    if abs(gap) > 0.05:
        raise AssertionError(f"FY{year}E balance-sheet gap: {gap:.2f}")


def build_projection(assumptions=ASSUMPTIONS):
    """Build linked income statement, balance sheet, cash flow, and FCFF."""
    balances = OPENING.copy()
    projection = []

    for index, year in enumerate(YEARS):
        automotive = balances["automotive_revenue"] * (1 + assumptions["automotive_growth"][index])
        energy = balances["energy_revenue"] * (1 + assumptions["energy_growth"][index])
        services = balances["services_revenue"] * (1 + assumptions["services_growth"][index])
        revenue = automotive + energy + services
        gross_profit = revenue * assumptions["gross_margin"][index]
        sga = gross_profit * assumptions["sga_to_gross_profit"][index]
        rnd = revenue * assumptions["rnd_to_revenue"][index]
        # Reported gross profit and operating expenses already include D&A.
        # Do not subtract depreciation a second time from EBIT.
        ebit = gross_profit - sga - rnd
        depreciation = balances["ppe"] * assumptions["depreciation_to_opening_ppe"]
        stock_comp = revenue * assumptions["stock_comp_to_revenue"]
        interest = balances["debt_and_finance_leases"] * assumptions["debt_rate"]
        pretax_income = ebit - interest
        tax = max(0.0, pretax_income) * assumptions["tax_rate"]
        net_income = pretax_income - tax
        nopat = ebit * (1 - assumptions["tax_rate"])

        inventory = (revenue - gross_profit) * assumptions["inventory_days"] / 365.0
        ppe = balances["ppe"] + assumptions["capex"][index] - depreciation
        other_assets = revenue * assumptions["other_assets_to_revenue"]
        other_liabilities = revenue * assumptions["other_liabilities_to_revenue"]
        debt_and_finance_leases = balances["debt_and_finance_leases"]

        change_nwc = (
            (inventory - balances["inventory"])
            + (other_assets - balances["other_assets"])
            - (other_liabilities - balances["other_liabilities"])
        )
        fcff = nopat + depreciation + stock_comp - assumptions["capex"][index] - change_nwc
        cash_from_operations = net_income + depreciation + stock_comp - change_nwc
        cash = balances["cash"] + cash_from_operations - assumptions["capex"][index]
        short_term_investments = balances["short_term_investments"]
        equity = balances["equity"] + net_income + stock_comp

        assets = cash + short_term_investments + inventory + ppe + other_assets
        liabilities_and_equity = debt_and_finance_leases + other_liabilities + equity
        gap = assets - liabilities_and_equity
        assert_balanced(year, gap)

        projection.append(
            {
                "year": year,
                "automotive": automotive,
                "energy": energy,
                "services": services,
                "revenue": revenue,
                "gross_profit": gross_profit,
                "sga": sga,
                "rnd": rnd,
                "ebit": ebit,
                "depreciation": depreciation,
                "stock_comp": stock_comp,
                "interest": interest,
                "pretax_income": pretax_income,
                "tax": tax,
                "net_income": net_income,
                "nopat": nopat,
                "inventory": inventory,
                "ppe": ppe,
                "other_assets": other_assets,
                "cash": cash,
                "short_term_investments": short_term_investments,
                "debt_and_finance_leases": debt_and_finance_leases,
                "other_liabilities": other_liabilities,
                "equity": equity,
                "change_nwc": change_nwc,
                "cash_from_operations": cash_from_operations,
                "capex": assumptions["capex"][index],
                "fcff": fcff,
                "gap": gap,
            }
        )
        balances = {
            "automotive_revenue": automotive,
            "energy_revenue": energy,
            "services_revenue": services,
            "cash": cash,
            "short_term_investments": short_term_investments,
            "inventory": inventory,
            "ppe": ppe,
            "other_assets": other_assets,
            "debt_and_finance_leases": debt_and_finance_leases,
            "other_liabilities": other_liabilities,
            "equity": equity,
        }
    return projection


def dcf_value(projection, assumptions=ASSUMPTIONS):
    """Return enterprise value, terminal-value share, equity value, and per share."""
    wacc = assumptions["wacc"]
    terminal_growth = assumptions["terminal_growth"]
    if wacc <= terminal_growth:
        raise ValueError("WACC must exceed terminal growth for a perpetuity-growth terminal value.")
    pv_fcff = sum(row["fcff"] / (1 + wacc) ** (index + 1) for index, row in enumerate(projection))
    terminal_value = projection[-1]["fcff"] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1 + wacc) ** len(projection)
    enterprise_value = pv_fcff + pv_terminal
    gross_liquidity = OPENING["cash"] + OPENING["short_term_investments"]
    operating_cash_reserve = assumptions.get("operating_cash_reserve", 0.0)
    if not 0 <= operating_cash_reserve <= gross_liquidity:
        raise ValueError("Operating-cash reserve must be between zero and gross liquidity.")
    non_operating_cash = gross_liquidity - operating_cash_reserve
    equity_value = enterprise_value + non_operating_cash - OPENING["debt_and_finance_leases"]
    return {
        "enterprise_value": enterprise_value,
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "terminal_value_share": pv_terminal / enterprise_value,
        "non_operating_cash": non_operating_cash,
        "operating_cash_reserve": operating_cash_reserve,
        "debt_and_finance_leases": OPENING["debt_and_finance_leases"],
        "equity_value": equity_value,
        "per_share_value": equity_value / assumptions["diluted_shares"],
    }


def reverse_dcf_terminal_growth(projection):
    """Solve the terminal growth rate that matches the September 30 share price.

    Explicit FCFF, WACC, cash, debt, and diluted shares stay fixed.  A result
    close to WACC is a warning, not a plausible long-run forecast.
    """
    target_equity = MARKET_PRICE * ASSUMPTIONS["diluted_shares"]
    target_enterprise = (
        target_equity
        - (OPENING["cash"] + OPENING["short_term_investments"] - ASSUMPTIONS["operating_cash_reserve"])
        + OPENING["debt_and_finance_leases"]
    )
    low, high = -0.05, ASSUMPTIONS["wacc"] - 0.0001
    for _ in range(200):
        midpoint = (low + high) / 2
        run_assumptions = deepcopy(ASSUMPTIONS)
        run_assumptions["terminal_growth"] = midpoint
        enterprise_value = dcf_value(projection, run_assumptions)["enterprise_value"]
        if enterprise_value < target_enterprise:
            low = midpoint
        else:
            high = midpoint
    return (low + high) / 2


def sensitivity(projection, assumptions=ASSUMPTIONS):
    """Return a WACC-terminal growth sensitivity and verify monotonicity."""
    center_wacc = assumptions["wacc"]
    waccs = [center_wacc - 0.010, center_wacc, center_wacc + 0.010]
    growths = [0.020, 0.030, 0.040]
    grid = {}
    for wacc in waccs:
        for growth in growths:
            run_assumptions = deepcopy(assumptions)
            run_assumptions["wacc"] = wacc
            run_assumptions["terminal_growth"] = growth
            grid[(wacc, growth)] = dcf_value(projection, run_assumptions)["per_share_value"]
    for growth in growths:
        assert grid[(waccs[0], growth)] > grid[(waccs[1], growth)] > grid[(waccs[2], growth)]
    for wacc in waccs:
        assert grid[(wacc, growths[0])] < grid[(wacc, growths[1])] < grid[(wacc, growths[2])]
    return grid


def print_table(title, rows):
    print(f"\n{title}")
    print(f"{'USD millions':<34}" + "".join(f"FY{year}E".rjust(13) for year in YEARS))
    for label, values in rows:
        print(f"{label:<34}" + "".join(f"{value:>13,.1f}" for value in values))


def main():
    projection = build_projection()
    series = lambda key: [row[key] for row in projection]
    print(f"Tesla FCFF DCF | Valuation date: {VALUATION_DATE}")
    print_table("Income Statement", [
        ("Automotive revenue", series("automotive")),
        ("Energy revenue", series("energy")),
        ("Services revenue", series("services")),
        ("Total revenue", series("revenue")),
        ("Gross profit", series("gross_profit")),
        ("SG&A", series("sga")),
        ("R&D", series("rnd")),
        ("EBIT", series("ebit")),
        ("Net income", series("net_income")),
    ])
    print_table("Balance Sheet", [
        ("Cash", series("cash")),
        ("Short-term investments", series("short_term_investments")),
        ("Inventory", series("inventory")),
        ("PP&E", series("ppe")),
        ("Other assets", series("other_assets")),
        ("Debt and finance leases", series("debt_and_finance_leases")),
        ("Other liabilities", series("other_liabilities")),
        ("Equity", series("equity")),
    ])
    print_table("Cash Flow and FCFF", [
        ("NOPAT", series("nopat")),
        ("Depreciation and amortization", series("depreciation")),
        ("Stock-based compensation", series("stock_comp")),
        ("Change in operating NWC", series("change_nwc")),
        ("Capital expenditures", [-value for value in series("capex")]),
        ("FCFF", series("fcff")),
    ])
    print_table("Articulation Checks", [("Assets - liabilities - equity", series("gap"))])
    value = dcf_value(projection)
    print("\nEnterprise-to-equity bridge")
    for label in ("enterprise_value", "non_operating_cash", "debt_and_finance_leases", "equity_value", "per_share_value"):
        print(f"{label}: {value[label]:,.2f}")
    print(f"Terminal-value share: {value['terminal_value_share']:.1%}")
    grid = sensitivity(projection)
    print("\nPer-share sensitivity (WACC x terminal growth)")
    for wacc in [ASSUMPTIONS["wacc"] - 0.010, ASSUMPTIONS["wacc"], ASSUMPTIONS["wacc"] + 0.010]:
        print(f"{wacc:.1%}: " + ", ".join(f"{grid[(wacc, growth)]:.2f}" for growth in [0.020, 0.030, 0.040]))
    print("Monotonicity checks: PASS")
    implied_growth = reverse_dcf_terminal_growth(projection)
    print(f"Market price on {VALUATION_DATE}: ${MARKET_PRICE:,.2f}")
    print(f"Reverse DCF implied terminal growth: {implied_growth:.2%}")
    reserve_case = deepcopy(ASSUMPTIONS)
    reserve_case["operating_cash_reserve"] = 10_000.0
    reserve_value = dcf_value(projection, reserve_case)
    print(
        "Operating-cash reserve sensitivity: "
        f"USD {reserve_case['operating_cash_reserve']:,.0f}m reserve -> "
        f"${reserve_value['per_share_value']:,.2f} per share"
    )


if __name__ == "__main__":
    main()
