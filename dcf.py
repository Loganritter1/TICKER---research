"""Five-year FCFF DCF, sensitivity grid, and reverse DCF (USD millions)."""

import sys


# Editable inputs: Tesla case
STARTING_FCFF = 6433.16
GROWTH_RATES = [0.11, 0.08, 0.06, 0.05, 0.04]
WACC = 0.161
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 44059.0
DEBT = 8177.0
DILUTED_SHARES = 3528.0

# Editable sensitivity and reverse-DCF inputs
SENSITIVITY_WACCS = [0.151, 0.161, 0.171]
SENSITIVITY_TERMINAL_GROWTHS = [0.02, 0.03, 0.04]
TARGET_SHARE_PRICE = 367.81
REVERSE_SHIFT_LOWER_BOUND = -0.05
REVERSE_SHIFT_UPPER_BOUND = 0.10
BISECTION_TOLERANCE = 0.00000001
BISECTION_MAX_ITERATIONS = 200


def validate_base_inputs():
    if TERMINAL_GROWTH >= WACC:
        sys.exit("Error: terminal growth must be less than WACC.")
    if len(GROWTH_RATES) != 5:
        sys.exit("Error: provide exactly five yearly growth rates.")
    if DILUTED_SHARES <= 0:
        sys.exit("Error: diluted shares must be greater than zero.")


def value_dcf(growth_rates, wacc, terminal_growth):
    """Return FCFF path and valuation values for a five-year FCFF DCF."""
    fcff_by_year = []
    fcff = STARTING_FCFF
    for growth_rate in growth_rates:
        fcff *= 1 + growth_rate
        fcff_by_year.append(fcff)

    explicit_present_value = sum(
        year_fcff / (1 + wacc) ** year
        for year, year_fcff in enumerate(fcff_by_year, start=1)
    )
    terminal_value_year_5 = (
        fcff_by_year[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    )
    terminal_present_value = terminal_value_year_5 / (1 + wacc) ** 5
    enterprise_value = explicit_present_value + terminal_present_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    value_per_share = equity_value / DILUTED_SHARES
    return (
        fcff_by_year,
        explicit_present_value,
        terminal_value_year_5,
        terminal_present_value,
        enterprise_value,
        equity_value,
        value_per_share,
        terminal_present_value / enterprise_value,
    )


def print_base_case(results):
    (
        fcff_by_year,
        explicit_present_value,
        terminal_value_year_5,
        terminal_present_value,
        enterprise_value,
        equity_value,
        value_per_share,
        terminal_share,
    ) = results
    for year, year_fcff in enumerate(fcff_by_year, start=1):
        print(f"FCFF Year {year}: {year_fcff:.4f}")
    print(f"PV of Explicit FCFF: {explicit_present_value:.4f}")
    print(f"Terminal Value at Year 5: {terminal_value_year_5:.4f}")
    print(f"PV of Terminal Value: {terminal_present_value:.4f}")
    print(f"Enterprise Value: {enterprise_value:.4f}")
    print(f"Equity Value: {equity_value:.4f}")
    print(f"Value per Diluted Share: {value_per_share:.4f}")
    print(f"PV of Terminal Value / Enterprise Value: {terminal_share:.4f}")


def print_sensitivity_grid():
    print("\nSensitivity Grid: Value per Diluted Share")
    header = "WACC \\ Terminal Growth".ljust(24)
    header += "".join(f"{growth:>12.1%}" for growth in SENSITIVITY_TERMINAL_GROWTHS)
    print(header)
    for sensitivity_wacc in SENSITIVITY_WACCS:
        row = f"{sensitivity_wacc:.1%}".ljust(24)
        for sensitivity_terminal_growth in SENSITIVITY_TERMINAL_GROWTHS:
            if sensitivity_terminal_growth >= sensitivity_wacc:
                cell = "invalid"
            else:
                cell = f"{value_dcf(GROWTH_RATES, sensitivity_wacc, sensitivity_terminal_growth)[6]:.4f}"
            row += f"{cell:>12}"
        print(row)


def reverse_value_per_share(shift):
    shifted_growth_rates = [growth_rate + shift for growth_rate in GROWTH_RATES]
    return value_dcf(shifted_growth_rates, WACC, TERMINAL_GROWTH)[6]


def print_reverse_dcf():
    print("\nReverse DCF: Uniform Shift to All Five Explicit Growth Rates")
    held_fixed = (
        f"starting FCFF={STARTING_FCFF:.4f}; WACC={WACC:.2%}; "
        f"terminal growth={TERMINAL_GROWTH:.2%}; cash={NON_OPERATING_CASH:.4f}; "
        f"debt={DEBT:.4f}; diluted shares={DILUTED_SHARES:.4f}; "
        f"base growth rates={GROWTH_RATES}"
    )
    print(f"Target Share Price: {TARGET_SHARE_PRICE:.4f}")
    print(f"Inputs Held Fixed: {held_fixed}")

    if any(growth + REVERSE_SHIFT_LOWER_BOUND <= -1 for growth in GROWTH_RATES):
        print("Result: no solution; lower bound pushes an annual growth rate to -100% or below.")
        return
    if any(growth + REVERSE_SHIFT_UPPER_BOUND <= -1 for growth in GROWTH_RATES):
        print("Result: no solution; upper bound pushes an annual growth rate to -100% or below.")
        return

    lower_value = reverse_value_per_share(REVERSE_SHIFT_LOWER_BOUND)
    upper_value = reverse_value_per_share(REVERSE_SHIFT_UPPER_BOUND)
    if not min(lower_value, upper_value) <= TARGET_SHARE_PRICE <= max(lower_value, upper_value):
        print(
            "Result: no solution in bracket "
            f"[{REVERSE_SHIFT_LOWER_BOUND:.2%}, {REVERSE_SHIFT_UPPER_BOUND:.2%}]."
        )
        return

    lower_bound = REVERSE_SHIFT_LOWER_BOUND
    upper_bound = REVERSE_SHIFT_UPPER_BOUND
    for _ in range(BISECTION_MAX_ITERATIONS):
        midpoint = (lower_bound + upper_bound) / 2
        midpoint_value = reverse_value_per_share(midpoint)
        if abs(midpoint_value - TARGET_SHARE_PRICE) < BISECTION_TOLERANCE:
            break
        if midpoint_value < TARGET_SHARE_PRICE:
            lower_bound = midpoint
        else:
            upper_bound = midpoint

    print(f"Solved Uniform Growth Shift: {midpoint:.4%}")
    print(f"Value per Diluted Share at Solved Shift: {midpoint_value:.4f}")


validate_base_inputs()
base_case_results = value_dcf(GROWTH_RATES, WACC, TERMINAL_GROWTH)
print_base_case(base_case_results)
print_sensitivity_grid()
print_reverse_dcf()
