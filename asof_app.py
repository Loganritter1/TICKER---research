"""Lab 17: compare FRED's current values with an ALFRED vintage."""

from datetime import date
from io import StringIO

import pandas as pd
import streamlit as st
import altair as alt


SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Effective federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
ALFRED_CSV = (
    "https://alfred.stlouisfed.org/graph/alfredgraph.csv?"
    "id={series_id}&vintage_date={vintage_date}"
)


def tidy_csv(csv_text: str, series_id: str) -> pd.DataFrame:
    """Return date/value columns and turn FRED's '.' marker into a missing value."""
    frame = pd.read_csv(StringIO(csv_text))
    if frame.shape[1] < 2:
        raise ValueError("The download did not contain a value column.")
    frame = frame.iloc[:, :2].copy()
    frame.columns = ["date", "value"]
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["value"] = pd.to_numeric(frame["value"].replace(".", pd.NA), errors="coerce")
    frame = frame.dropna(subset=["date"]).sort_values("date")
    if frame.empty:
        raise ValueError(f"FRED returned no dated observations for {series_id}.")
    return frame


@st.cache_data(show_spinner=False)
def download_current(series_id: str) -> pd.DataFrame:
    """Download the current FRED representation once per selected series."""
    url = FRED_CSV.format(series_id=series_id)
    response = pd.read_csv(url)
    return tidy_csv(response.to_csv(index=False), series_id)


@st.cache_data(show_spinner=False)
def download_vintage(series_id: str, vintage_date: str) -> pd.DataFrame:
    """Download the ALFRED representation available on the requested date."""
    url = ALFRED_CSV.format(series_id=series_id, vintage_date=vintage_date)
    response = pd.read_csv(url)
    return tidy_csv(response.to_csv(index=False), series_id)


def value_on(frame: pd.DataFrame, measured_date: pd.Timestamp) -> float | None:
    """Return a current value for a measurement date, if it exists and is not missing."""
    matches = frame.loc[frame["date"] == measured_date, "value"].dropna()
    return None if matches.empty else float(matches.iloc[-1])


def fmt_value(value: float | None) -> str:
    return "—" if value is None or pd.isna(value) else f"{value:,.3f}".rstrip("0").rstrip(".")


def audit_series(
    series_id: str, start_date: date, as_of_date: date
) -> tuple[pd.DataFrame, dict, pd.DataFrame]:
    """Build the chart data and point-in-time audit row for one FRED series."""
    current = download_current(series_id)
    vintage = download_vintage(series_id, as_of_date.isoformat())
    cutoff = pd.Timestamp(as_of_date)
    start = pd.Timestamp(start_date)
    known = vintage.loc[(vintage["date"] >= start) & (vintage["date"] <= cutoff)].dropna(subset=["value"])
    chart_data = current.loc[current["date"] >= start].dropna(subset=["value"])
    if known.empty:
        raise ValueError(f"No non-missing {series_id} observations were known by {as_of_date:%Y-%m-%d}.")

    last = known.iloc[-1]
    last_date = last["date"]
    current_same_date = value_on(current, last_date)
    current_to_cutoff = current.loc[(current["date"] >= start) & (current["date"] <= cutoff)].dropna(subset=["value"])
    later_count = int((current_to_cutoff["date"] > last_date).sum())
    aligned = known.merge(current[["date", "value"]], on="date", how="left", suffixes=("_known", "_today"))
    revised_count = int(
        (aligned["value_today"].notna() & (aligned["value_known"] != aligned["value_today"])).sum()
    )
    revisions = aligned.loc[
        aligned["value_today"].notna() & (aligned["value_known"] != aligned["value_today"]),
        ["date", "value_known", "value_today"],
    ].copy()
    revisions["difference"] = revisions["value_today"] - revisions["value_known"]
    row = {
        "Series": series_id,
        "Last measurement known then": last_date.date().isoformat(),
        "Value known then": fmt_value(float(last["value"])),
        "Value today (same date)": fmt_value(current_same_date),
        "Current values after that date": later_count,
        "Revised same-date values": revised_count,
    }
    return chart_data, row, revisions


st.set_page_config(page_title="Point-in-Time Rates Audit", layout="wide")
st.title("Point-in-Time Rates Audit")
st.caption(
    "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today; "
    "built with AI help, a learning demonstration, not investment advice."
)

with st.sidebar:
    st.header("Audit controls")
    selected = st.multiselect(
        "Series IDs",
        options=list(SERIES),
        default=list(SERIES),
        format_func=lambda series_id: f"{series_id} — {SERIES[series_id]}",
    )
    extra_id = st.text_input("Add another FRED series ID", placeholder="e.g., PAYEMS").strip().upper()
    start_date = st.date_input("Start date", value=date(2020, 1, 1))
    as_of_date = st.date_input("As known on", value=date.today(), max_value=date.today())
    combine_charts = st.checkbox("Also show selected series on one chart", value=False)
    combined_view = st.radio(
        "Combined-chart scale",
        options=["Raw values", "Normalize to 100 at start"],
        disabled=not combine_charts,
        help="Normalization makes every series start at 100, so their percentage moves can be compared.",
    )

if extra_id and extra_id not in selected:
    selected.append(extra_id)

if not selected:
    st.info("Select at least one series to start the audit.")
    st.stop()

if start_date > as_of_date:
    st.error("The start date must be on or before the as-known-on date.")
    st.stop()

rows = []
combined = []
for series_id in selected:
    label = SERIES.get(series_id, "Custom FRED series")
    try:
        with st.spinner(f"Downloading {series_id}..."):
            chart, audit_row, revisions = audit_series(series_id, start_date, as_of_date)
        st.subheader(f"{series_id} — {label}")
        st.line_chart(chart.set_index("date")["value"], width="stretch")
        st.caption(
            f"Last non-missing measurement known on {as_of_date.strftime('%B')} {as_of_date.day}, {as_of_date.year}: "
            f"{audit_row['Last measurement known then']} ({audit_row['Value known then']})."
        )
        metrics = st.columns(4)
        metrics[0].metric("Latest value", fmt_value(float(chart["value"].iloc[-1])))
        metrics[1].metric(
            "Change since start",
            f"{(chart['value'].iloc[-1] / chart['value'].iloc[0] - 1):.2%}",
        )
        metrics[2].metric("Late observations", audit_row["Current values after that date"])
        metrics[3].metric("Revised observations", audit_row["Revised same-date values"])
        if not revisions.empty:
            with st.expander(f"Review {len(revisions)} revised {series_id} observations"):
                st.dataframe(
                    revisions.assign(date=revisions["date"].dt.date),
                    hide_index=True,
                    width="stretch",
                )
        else:
            st.caption("No same-date revisions were found in this selected history and vintage.")
        combined.append(chart.rename(columns={"value": series_id}).set_index("date"))
        rows.append(audit_row)
    except Exception as error:  # Each series is independent so one bad ID does not stop the audit.
        st.error(f"{series_id}: {error}")

if combine_charts and combined:
    st.subheader("Selected series together")
    combined_chart = pd.concat(combined, axis=1, sort=True)
    if combined_view == "Normalize to 100 at start":
        combined_chart = combined_chart.apply(lambda column: column / column.dropna().iloc[0] * 100)
        st.caption("Each series equals 100 at its first displayed non-missing observation.")
    else:
        st.caption("Values retain their original units; compare direction, not level, when units or scales differ.")
    chart_long = (
        combined_chart.reset_index()
        .melt(id_vars="date", var_name="Series", value_name="Value")
        .dropna(subset=["Value"])
    )
    st.altair_chart(
        alt.Chart(chart_long)
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Measurement date"),
            y=alt.Y("Value:Q", title="Index (start = 100)" if combined_view != "Raw values" else "Rate value"),
            color=alt.Color("Series:N", title="Series"),
            tooltip=[alt.Tooltip("date:T", title="Date"), "Series:N", alt.Tooltip("Value:Q", format=".3f")],
        )
        .interactive(),
        width="stretch",
    )

if rows:
    table = pd.DataFrame(rows)
    table["Series"] = table["Series"].map(
        lambda series_id: f"https://fred.stlouisfed.org/series/{series_id}"
    )
    st.subheader("As-known-on audit table")
    st.dataframe(
        table,
        column_config={"Series": st.column_config.LinkColumn("Series ID", display_text=r".*/([^/]+)$")},
        hide_index=True,
        width="stretch",
    )
    st.download_button(
        "Download audit table as CSV",
        data=pd.DataFrame(rows).to_csv(index=False),
        file_name=f"fred_alfred_audit_{as_of_date.isoformat()}.csv",
        mime="text/csv",
    )

st.subheader("Project 2 decision note")
st.text_area(
    "Record an admit, quarantine, or reject decision; state the as-of rule and what would change it.",
    placeholder="Example: Admit DGS10 only from ALFRED data available by the prior completed business day...",
)
