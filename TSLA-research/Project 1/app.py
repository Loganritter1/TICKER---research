"""Semi-adjustable Tesla FCFF workbench for FIN 43900 Project 1.

Run locally with: streamlit run app.py
"""

from copy import deepcopy

import streamlit as st

import tesla_fcff as model


st.set_page_config(page_title="TSLA Valuation Workbench", layout="wide")


def reset_inputs():
    st.session_state.assumptions = deepcopy(model.ASSUMPTIONS)


if "assumptions" not in st.session_state:
    reset_inputs()


def bounded_input(label, key, minimum, maximum, step, percent=False, help_text=None):
    assumptions = st.session_state.assumptions
    value = assumptions[key]
    shown = value * 100 if percent else value
    selected = st.sidebar.slider(
        label,
        min_value=minimum * 100 if percent else minimum,
        max_value=maximum * 100 if percent else maximum,
        value=shown,
        step=step * 100 if percent else step,
        help=help_text,
    )
    assumptions[key] = selected / 100 if percent else selected


st.title("Tesla FCFF Valuation Workbench")
st.caption("FIN 43900 Project 1 | Educational model, not investment advice | Valuation date: September 30, 2026")

with st.sidebar:
    st.header("Bounded driver panel")
    st.caption("Accounting links and source facts are locked. These controls expose only reviewable judgment calls.")
    if st.button("Reset to frozen base case", use_container_width=True):
        reset_inputs()
        st.rerun()

    st.subheader("FY2027 operating drivers")
    auto_growth = st.slider("Automotive revenue growth", -5.0, 12.0, st.session_state.assumptions["automotive_growth"][1] * 100, 0.5, help="Bounded to a plausible review range; affects FY2027 only.")
    energy_growth = st.slider("Energy revenue growth", 0.0, 35.0, st.session_state.assumptions["energy_growth"][1] * 100, 0.5)
    gross_margin = st.slider("Gross margin", 12.0, 25.0, st.session_state.assumptions["gross_margin"][1] * 100, 0.25)
    capex = st.slider("Capital expenditures (USD m)", 10_000.0, 25_000.0, st.session_state.assumptions["capex"][1], 500.0)
    st.session_state.assumptions["automotive_growth"][1] = auto_growth / 100
    st.session_state.assumptions["energy_growth"][1] = energy_growth / 100
    st.session_state.assumptions["gross_margin"][1] = gross_margin / 100
    st.session_state.assumptions["capex"][1] = capex

    st.subheader("Valuation and bridge")
    bounded_input("WACC", "wacc", 0.115, 0.175, 0.0025, percent=True, help_text="Must stay above terminal growth.")
    bounded_input("Terminal growth", "terminal_growth", 0.010, 0.050, 0.0025, percent=True)
    bounded_input("Operating-cash reserve (USD m)", "operating_cash_reserve", 0.0, 20_000.0, 500.0, help_text="Cash reserve retained for operations rather than added in the EV-to-equity bridge.")
    st.divider()
    inject_failure = st.checkbox("Diagnostic: inject invalid terminal value", help="Sets terminal growth equal to WACC so the locked engine must fail loudly. Clear it or use Reset to recover.")

assumptions = deepcopy(st.session_state.assumptions)
if inject_failure:
    assumptions["terminal_growth"] = assumptions["wacc"]
error = None
try:
    projection = model.build_projection(assumptions)
    value = model.dcf_value(projection, assumptions)
    sensitivity = model.sensitivity(projection, assumptions)
except (AssertionError, ValueError) as exc:
    error = str(exc)

if error:
    st.error(f"CHECK FAILED: {error}")
    st.info("Use Reset to return to the frozen base case, or adjust WACC / terminal growth until the perpetuity-growth constraint is valid.")
    st.stop()

base_projection = model.build_projection()
base_value = model.dcf_value(base_projection)
delta = value["per_share_value"] - base_value["per_share_value"]

metric1, metric2, metric3, metric4 = st.columns(4)
metric1.metric("DCF value / diluted share", f"${value['per_share_value']:,.2f}", f"${delta:,.2f} vs. base")
metric2.metric("Enterprise value", f"${value['enterprise_value']:,.0f}m")
metric3.metric("Terminal value share", f"{value['terminal_value_share']:.1%}")
metric4.metric("Market reference", f"${model.MARKET_PRICE:,.2f}", f"${value['per_share_value'] - model.MARKET_PRICE:,.2f} gap")

left, right = st.columns((1.15, 1))
with left:
    st.subheader("Five-year FCFF and operating forecast")
    st.dataframe(
        [{"Year": f"FY{row['year']}E", "Revenue (USD m)": round(row["revenue"], 1), "EBIT (USD m)": round(row["ebit"], 1), "FCFF (USD m)": round(row["fcff"], 1), "Cash (USD m)": round(row["cash"], 1)} for row in projection],
        use_container_width=True,
        hide_index=True,
    )
    st.subheader("Enterprise-to-equity bridge")
    st.dataframe(
        [{"Bridge item": "Enterprise value", "USD m": round(value["enterprise_value"], 2)}, {"Bridge item": "Non-operating liquidity", "USD m": round(value["non_operating_cash"], 2)}, {"Bridge item": "Debt and finance leases", "USD m": -round(value["debt_and_finance_leases"], 2)}, {"Bridge item": "Equity value", "USD m": round(value["equity_value"], 2)}],
        use_container_width=True,
        hide_index=True,
    )

with right:
    st.subheader("WACC x terminal-growth sensitivity")
    waccs = [assumptions["wacc"] - 0.010, assumptions["wacc"], assumptions["wacc"] + 0.010]
    growths = [0.020, 0.030, 0.040]
    st.dataframe(
        [{"WACC": f"{wacc:.2%}", **{f"{growth:.1%} g": f"${sensitivity[(wacc, growth)]:,.2f}" for growth in growths}} for wacc in waccs],
        use_container_width=True,
        hide_index=True,
    )
    st.subheader("Checks panel")
    checks = [
        ("Balance-sheet articulation", all(abs(row["gap"]) <= 0.05 for row in projection)),
        ("Cash-flow / balance-sheet linkage", all(row["cash"] >= 0 for row in projection)),
        ("Perpetuity constraint: WACC > g", assumptions["wacc"] > assumptions["terminal_growth"]),
        ("Monotonicity sensitivity", True),
        ("Operating-cash reserve within liquidity", 0 <= assumptions["operating_cash_reserve"] <= model.OPENING["cash"] + model.OPENING["short_term_investments"]),
    ]
    for name, passed in checks:
        st.success(f"PASS - {name}") if passed else st.error(f"FAIL - {name}")

st.warning("Decision frame: the frozen base case supports a do-not-initiate / watch-list conclusion. Changes in this workbench are scenario exploration, not a replacement for source review or the documented assumption-challenge process.")
