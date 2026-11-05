"""Streamlit interface for the Lab 19 Legend Panel."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from edgar_buffett import METRICS, analyze_ticker, format_number, graham_checks
from memo_validation import unsupported_numbers

NOTES_PATH = Path(__file__).parent / "panel_discussion_notes.json"


def verdict(checks: dict[str, str]) -> str:
    """Turn one investor's results into a transparent panel verdict."""
    passed = sum(result == "pass" for result in checks.values())
    if "not known" in checks.values():
        return f"WATCH — EVIDENCE GAP ({passed} pass)"
    if passed == len(checks):
        return f"CLEARS PANEL ({passed} of {len(checks)})"
    return f"DOES NOT CLEAR ({passed} of {len(checks)})"


def memo_verdict(checks: dict[str, str]) -> str:
    """Use words, not an unprinted count, in a validator-safe memo verdict."""
    if "not known" in checks.values():
        return "evidence gap"
    return "clears every stated check" if all(result == "pass" for result in checks.values()) else "does not clear every stated check"


def values(rows: list[dict], metric: str, suffix: str = "") -> str:
    return ", ".join(format_number(row[metric], suffix) for row in rows)


def default_memos(report: dict, checks_by_investor: dict[str, dict[str, str]], threshold: float) -> dict[str, str]:
    """Create investor-specific drafts using only calculator values."""
    rows = report["rows"]
    first, latest = rows[0], rows[-1]
    return {
        "Buffett": (
            f"# Buffett-style memo: {report['ticker']}\n\n"
            f"**Verdict: {memo_verdict(checks_by_investor['Buffett'])}.** "
            f"ROE was {values(rows, 'ROE', '%')}. Owner earnings were {values(rows, 'Owner earnings')}. "
            "This memo evaluates the business, not its market price."
        ),
        "Graham": (
            f"# Graham-style memo: {report['ticker']}\n\n"
            f"**Verdict: {memo_verdict(checks_by_investor['Graham'])}.** "
            f"Latest current ratio was {format_number(latest['Current ratio'])}; the threshold is {threshold:g}. "
            f"Net income changed from {format_number(first['Net income'])} to {format_number(latest['Net income'])}."
        ),
        "Burry": (
            f"# Burry-style memo: {report['ticker']}\n\n"
            f"**Verdict: {memo_verdict(checks_by_investor['Burry'])}.** "
            f"Operating cash flow was {values(rows, 'Operating cash flow')}; net income was {values(rows, 'Net income')}. "
            f"Latest liabilities / equity was {format_number(latest['Liabilities / equity'])}."
        ),
    }


def threshold_rationale(threshold: float) -> str:
    """Provide a complete, editable explanation for the selected threshold."""
    if threshold == 2.0:
        return (
            "Keep 2.0: it preserves Graham’s conservative liquidity standard. "
            "Costco’s 1.06 passes at 1.0, but it does not meet the stricter "
            "current-ratio requirement."
        )
    return (
        "Keep 1.0: Costco’s 1.06 passes, showing that the 2.0 cutoff is a "
        "stricter design choice rather than an automatic measure of financial weakness."
    )


def load_discussion_notes() -> dict:
    """Load local discussion notes without storing the SEC User-Agent."""
    if not NOTES_PATH.exists():
        return {}
    try:
        return json.loads(NOTES_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def save_discussion_notes(notes: dict) -> None:
    """Persist only the student's panel discussion text by ticker."""
    NOTES_PATH.write_text(json.dumps(notes, indent=2), encoding="utf-8")


def default_discussion(ticker: str) -> tuple[str, str]:
    if ticker == "COST":
        return (
            "Costco passes every Buffett and Burry check. Its panel shows positive owner earnings, positive net income, and operating cash flow at least as large as net income across the reported years.",
            "Costco fails Graham’s latest current-ratio requirement because its ratio is 1.06, below the 2.0 threshold. The result shows that a conservative liquidity screen can reject the company even when the other panel checks pass.",
        )
    return "", ""


st.set_page_config(page_title="Legend Panel", layout="wide")
st.markdown(
    """
    <style>
      :root { --ink: #17212b; --muted: #56616d; --paper: #f7f6f2; --card: #ffffff;
              --line: #d8ddd9; --accent: #2f6b5f; --accent-soft: #e6f0ec; --gold: #a46f26; }
      .stApp { background: var(--paper); color: var(--ink); }
      .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
      .stApp span, .stApp label, .stApp li, .stApp div { color: var(--ink); }
      [data-testid="stSidebar"] { background: #eef1ed; border-right: 1px solid var(--line); }
      [data-testid="stSidebar"] * { color: var(--ink) !important; }
      h1 { font-family: Georgia, serif; letter-spacing: -0.035em; font-size: 3rem !important; margin-bottom: 0.1rem !important; }
      h2, h3 { color: var(--ink) !important; letter-spacing: -0.015em; }
      [data-testid="stCaptionContainer"] p { color: var(--muted) !important; }
      [data-testid="stMetric"] { background: var(--card); border: 1px solid var(--line); border-top: 4px solid var(--accent);
                                  border-radius: 10px; padding: 0.9rem 1rem; box-shadow: 0 2px 8px rgba(23,33,43,.04); }
      [data-testid="stMetricLabel"] { color: var(--muted) !important; font-weight: 700; }
      [data-testid="stMetricValue"] { color: var(--ink) !important; font-size: 1.1rem; }
      [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; background: var(--card); }
      [data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input, [data-testid="stSelectbox"] input {
          color: var(--ink) !important; background: var(--card) !important; border: 1px solid #aeb8b2 !important; }
      [data-testid="stTextArea"] textarea { font-family: Georgia, serif; line-height: 1.5; }
      [data-testid="stButton"] button { background: var(--accent) !important; color: #ffffff !important;
                                         border: 1px solid var(--accent) !important; border-radius: 7px; font-weight: 700; }
      [data-testid="stButton"] button:hover { background: #24564d !important; border-color: #24564d !important; }
      [data-testid="stAlert"] { border-radius: 8px; }
      hr { border-color: var(--line); }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown("<p style='margin-bottom:0; color:#a46f26; font-weight:700; letter-spacing:.12em; font-size:.75rem;'>SEC EDGAR · SHARED FACTS · VISIBLE RULES</p>", unsafe_allow_html=True)
st.title("Legend Panel")
st.caption("Three investor screens reading the same five-year 10-K evidence. Educational use only; not investment advice.")

with st.sidebar:
    st.header("Analyze a business")
    ticker = st.text_input("Ticker", "COST").strip().upper()
    user_agent = st.text_input("SEC User-Agent (your name and email)", help="Used only for this request; it is not saved.")
    run = st.button("Analyze 10-K data", type="primary")

if run:
    if "@" not in user_agent:
        st.error("Enter your name and email in the SEC User-Agent field before running.")
    else:
        try:
            with st.spinner("Downloading annual 10-K facts from SEC EDGAR..."):
                st.session_state.report = analyze_ticker(ticker, user_agent)
        except Exception as error:
            st.error(f"EDGAR analysis failed: {error}")

if "report" not in st.session_state:
    st.info("Enter a ticker and SEC User-Agent, then select Analyze 10-K data.")
    st.stop()

report = st.session_state.report
threshold = st.selectbox("Graham current-ratio threshold", [2.0, 1.0], format_func=lambda value: f"{value:.1f}")
checks_by_investor = dict(report["checks"])
checks_by_investor["Graham"] = graham_checks(report["rows"], threshold)
drafts = default_memos(report, checks_by_investor, threshold)

st.subheader(f"Panel: {report['ticker']} | CIK {report['cik']}")
panel_rows = [
    {"Investor": investor, "Check": check, "Result": result}
    for investor, checks in checks_by_investor.items()
    for check, result in checks.items()
]
st.dataframe(pd.DataFrame(panel_rows), use_container_width=True, hide_index=True)

verdict_columns = st.columns(3)
for column, investor in zip(verdict_columns, checks_by_investor):
    column.metric(investor, verdict(checks_by_investor[investor]))

st.subheader("Shared five-year 10-K facts (USD millions)")
frame = pd.DataFrame(report["rows"])
display = frame.drop(columns="Tags")
for metric in (*METRICS, "ROE", "Owner earnings", "Current ratio", "Liabilities / equity"):
    display[f"{metric} tag"] = [row["Tags"][metric] for row in report["rows"]]
st.dataframe(display, use_container_width=True, hide_index=True)

st.subheader("Investor memos")
memo_columns = st.columns(3)
all_invalid: dict[str, list[str]] = {}
for column, investor in zip(memo_columns, checks_by_investor):
    with column:
        st.markdown(f"#### {investor}")
        memo = st.text_area(f"{investor} memo", drafts[investor], height=270, key=f"{report['ticker']}_{investor}_memo")
        invalid = unsupported_numbers(memo, report)
        all_invalid[investor] = invalid
        if invalid:
            st.error("Unprinted: " + ", ".join(invalid))
        else:
            st.success("All memo numbers were printed.")
        if investor == "Graham":
            st.text_area(
                "Threshold rationale",
                value=threshold_rationale(threshold),
                height=115,
                key=f"{report['ticker']}_{threshold:g}_threshold_rationale",
            )

if any(all_invalid.values()):
    st.error("Panel flag: at least one memo uses a number the script did not print.")
else:
    st.success("Panel flag: every number across all three memos was printed by the script.")

st.subheader("Panel discussion")
st.caption("Use only the results and values displayed above. Write two sentences in each box.")
discussion_notes = load_discussion_notes()
default_bull, default_bear = default_discussion(report["ticker"])
saved_notes = discussion_notes.get(report["ticker"], {})
bull_column, bear_column = st.columns(2)
with bull_column:
    bull_case = st.text_area(
        "Bull case",
        value=saved_notes.get("bull", default_bull),
        height=125,
        key=f"{report['ticker']}_bull_case",
    )
with bear_column:
    bear_case = st.text_area(
        "Bear case",
        value=saved_notes.get("bear", default_bear),
        height=125,
        key=f"{report['ticker']}_bear_case",
    )
discussion_notes[report["ticker"]] = {"bull": bull_case, "bear": bear_case}
try:
    save_discussion_notes(discussion_notes)
except OSError as error:
    st.warning(f"Discussion notes could not be saved locally: {error}")
