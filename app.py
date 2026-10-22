"""Lab 15: Streamlit interface for the portfolio stability decision."""

from copy import deepcopy

import streamlit as st

from portfolio import (
    CORRELATIONS,
    OBJECTIVE_RETURN,
    SLEEVES,
    estimate_from_prices,
    expected_return,
    lowest_risk_mix,
    portfolio_volatility,
    covariance_matrix,
    reserve_eligible_weight,
)


def metrics(weights, sleeves, correlations):
    """Return the displayed portfolio metrics using portfolio.py calculations."""
    covariance = covariance_matrix(sleeves, correlations)
    return {
        "return": expected_return(weights, sleeves),
        "volatility": portfolio_volatility(weights, covariance),
        "reserve": reserve_eligible_weight(weights, sleeves),
    }


def show_answer(title, weights, sleeves, correlations):
    """Show an allocation and its calculated metrics, or the infeasible message."""
    st.subheader(title)
    if weights is None:
        st.warning("No mix meets the objective.")
        return

    result = metrics(weights, sleeves, correlations)
    st.dataframe(
        {
            "Asset": list(weights),
            "Weight": [f"{weight:.0%}" for weight in weights.values()],
        },
        hide_index=True,
        use_container_width=True,
    )
    first, second, third = st.columns(3)
    first.metric("Expected return", f"{result['return']:.2%}")
    second.metric("Volatility", f"{result['volatility']:.2%}")
    third.metric("Reserve-eligible", f"{result['reserve']:.0%}")


st.set_page_config(page_title="Portfolio Stability Decision", layout="wide")
st.title("Portfolio Stability Decision")
st.caption("Built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    st.header("Mandate controls")
    objective = st.number_input(
        "Objective return estimate (%)", value=OBJECTIVE_RETURN * 100, step=0.1
    ) / 100
    reserve_minimum = st.number_input(
        "Minimum reserve-eligible weight (%)", value=3.0, min_value=0.0, max_value=100.0, step=1.0
    ) / 100
    uploaded_file = st.file_uploader("Upload monthly prices.csv", type="csv")
    last_36_months = st.toggle("Use last 36 monthly returns", value=False)

if uploaded_file is None:
    source_name = "Meridian training inputs"
    loaded_sleeves = deepcopy(SLEEVES)
    loaded_correlations = deepcopy(CORRELATIONS)
    active_sleeves = deepcopy(loaded_sleeves)
    active_correlations = loaded_correlations
else:
    try:
        source_name = "Uploaded prices.csv"
        uploaded_bytes = uploaded_file.getvalue()
        loaded_sleeves, loaded_correlations = estimate_from_prices(uploaded_bytes)
        if last_36_months:
            active_sleeves, active_correlations = estimate_from_prices(
                uploaded_bytes, last_36_months=True
            )
        else:
            active_sleeves = deepcopy(loaded_sleeves)
            active_correlations = loaded_correlations
    except ValueError as error:
        st.error(f"Could not estimate from this CSV: {error}")
        st.stop()

st.write(f"**Data source:** {source_name}. Returns shown are historical estimates, not forecasts.")
st.subheader("Editable inputs")
st.caption("Edit an expected return estimate or reserve eligibility to test stability.")

input_columns = st.columns(2)
for index, asset in enumerate(active_sleeves):
    with input_columns[index % 2]:
        active_sleeves[asset]["return"] = st.number_input(
            f"{asset} expected return estimate (%)",
            value=active_sleeves[asset]["return"] * 100,
            step=0.1,
            key=f"return_{source_name}_{last_36_months}_{asset}",
        ) / 100
        active_sleeves[asset]["reserve_eligible"] = st.checkbox(
            f"{asset} is reserve-eligible",
            value=active_sleeves[asset]["reserve_eligible"],
            key=f"reserve_{source_name}_{last_36_months}_{asset}",
        )

baseline_sleeves = deepcopy(loaded_sleeves)
for asset in baseline_sleeves:
    baseline_sleeves[asset]["reserve_eligible"] = active_sleeves[asset]["reserve_eligible"]

loaded_answer = lowest_risk_mix(
    baseline_sleeves, loaded_correlations, objective, reserve_minimum
)
active_answer = lowest_risk_mix(
    active_sleeves, active_correlations, objective, reserve_minimum
)

current, baseline = st.columns(2)
with current:
    show_answer("Lowest-risk mix with your current edits", active_answer, active_sleeves, active_correlations)
with baseline:
    show_answer("Answer for inputs as loaded", loaded_answer, baseline_sleeves, loaded_correlations)

if active_answer is not None and loaded_answer is not None:
    largest_change = max(
        abs(active_answer[asset] - loaded_answer[asset]) for asset in active_answer
    )
    st.info(f"Largest weight change from the loaded answer: {largest_change:.0%} points.")
