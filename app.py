"""Streamlit interface for the Lab 18 Legend Investor skill."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from edgar_buffett import METRICS, analyze_ticker, format_number
from memo_validation import unsupported_numbers

MEMO_DIR = Path(__file__).parent / "memos"


def default_memo(report: dict) -> str:
    """A constrained draft. The skill instructs the AI to revise only from this report."""
    checks = report["checks"]
    if "not known" in checks.values():
        verdict = "Watch it"
        rationale = "Important evidence is unavailable, so I cannot complete the owner-earnings judgment."
    elif all(result == "pass" for result in checks.values()):
        verdict = "Own the business"
        rationale = "The five-year record clears each stated business-quality check."
    else:
        verdict = "Pass"
        rationale = "The reported five-year record does not clear every stated business-quality check."
    return f"# Buffett-style memo: {report['ticker']}\n\n**Verdict: {verdict}.** {rationale}\n\nThis memo evaluates the business, not its market price.\n"


st.set_page_config(page_title="Legend Investor", layout="wide")
st.markdown(
    """
    <style>
      .stApp { background: #f8f7f2; color: #111111; }
      .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
      .stApp span, .stApp label, .stApp li, .stApp div { color: #111111; }
      [data-testid="stSidebar"] { background: #eeeade; border-right: 1px solid #cfc8b7; }
      [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
      [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p,
      [data-testid="stSidebar"] label { color: #111111 !important; }
      [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color: #333333 !important; }
      [data-testid="stSidebar"] input {
        color: #111111 !important; background: #ffffff !important;
        border-color: #aaa18e !important;
      }
      [data-testid="stSidebar"] button { color: #111111 !important; background: #e4c36a !important; border: 1px solid #8d6a12 !important; }
      .hero { padding: 2.1rem 2.25rem; border-radius: 12px; color: #111111;
              background: #ece4c8; border: 1px solid #c6b778; margin-bottom: 1.4rem; }
      .hero h1 { margin: 0; font-size: 2.5rem; color: #111111 !important; }
      .hero p { margin: .4rem 0 0; color: #111111 !important; font-size: 1.05rem; }
      .eyebrow { color: #111111 !important; font-weight: 700; letter-spacing: .12em; font-size: .75rem; }
      .verdict { padding: 1rem 1.2rem; border-radius: 10px; background: #ffffff;
                 border: 1px solid #b9b19e; border-left: 6px solid #4b8065; font-size: 1.1rem; margin: .5rem 0 1.25rem; }
      .check-pass, .check-fail, .check-unknown { color: #111111 !important; font-weight: 700; }
      [data-testid="stMetric"] { background: #ffffff; border: 1px solid #d5d0c3; border-radius: 10px; padding: .55rem .75rem; }
      [data-testid="stDataFrame"] { border: 1px solid #d5d0c3; border-radius: 10px; }
      [data-testid="stTextArea"] textarea { color: #ffffff !important; background: #171717 !important;
                                             border: 1px solid #171717 !important; font-family: Georgia, serif; }
      [data-testid="stTextArea"] textarea::placeholder { color: #dedede !important; }
    </style>
    <div class="hero">
      <div class="eyebrow">SEC EDGAR · 10-K ONLY · BUSINESS QUALITY</div>
      <h1>Legend Investor</h1>
      <p>Reproducible Buffett-style evidence, with calculations in code and judgment kept visible.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")

with st.sidebar:
    st.markdown("### Analyze a business")
    st.caption("The SEC requires a User-Agent that identifies you. It is used for this request only.")
    ticker = st.text_input("Ticker", "COST").strip().upper()
    user_agent = st.text_input("SEC User-Agent (your name and email)", type="password", help="Used only for this request; it is not saved.")
    run = st.button("Analyze 10-K data", type="primary")

if run:
    if "@" not in user_agent:
        st.error("Enter your name and email in the SEC User-Agent field before running.")
    else:
        try:
            with st.spinner("Downloading 10-K facts from SEC EDGAR..."):
                st.session_state.report = analyze_ticker(ticker, user_agent)
                memo_path = MEMO_DIR / f"{ticker}_buffett_memo.md"
                st.session_state.memo = memo_path.read_text(encoding="utf-8") if memo_path.exists() else default_memo(st.session_state.report)
        except Exception as error:
            st.error(f"EDGAR analysis failed: {error}")

if "report" not in st.session_state:
    st.info("Enter a ticker and SEC User-Agent, then select Analyze 10-K data.")
    st.stop()

report = st.session_state.report
memo = st.session_state.memo
frame = pd.DataFrame(report["rows"])
chart_data = frame.set_index("Fiscal year end")[["Owner earnings", "Net income"]].apply(pd.to_numeric, errors="coerce")

checks = report["checks"]
if all(result == "pass" for result in checks.values()):
    verdict, verdict_class = "OWN THE BUSINESS", "check-pass"
elif "not known" in checks.values():
    verdict, verdict_class = "WATCH — EVIDENCE GAP", "check-unknown"
else:
    verdict, verdict_class = "PASS — CHECK NOT CLEARED", "check-fail"
st.markdown(f'<div class="verdict"><span class="{verdict_class}">{verdict}</span> &nbsp;·&nbsp; {report["ticker"]} | CIK {report["cik"]}</div>', unsafe_allow_html=True)

latest = report["rows"][-1]
prior = report["rows"][0]
metrics = st.columns(4)
metrics[0].metric("Latest revenue", f"${format_number(latest['Revenue'])}M")
metrics[1].metric("Latest net income", f"${format_number(latest['Net income'])}M")
metrics[2].metric("Latest owner earnings", f"${format_number(latest['Owner earnings'])}M")
metrics[3].metric("Latest ROE", format_number(latest["ROE"], "%"))

left, right = st.columns([1.35, 1])
with left:
    st.subheader(f"{report['ticker']}: earnings trend")
    st.caption("USD millions · fiscal year-end dates")
    st.line_chart(chart_data, color=["#3e9368", "#e0a441"], height=330)
with right:
    st.subheader("Buffett checks")
    for check, result in checks.items():
        css = "check-pass" if result == "pass" else "check-fail" if result == "fail" else "check-unknown"
        symbol = "✓" if result == "pass" else "!" if result == "not known" else "×"
        st.markdown(f"<span class=\"{css}\">{symbol} {result.upper()}</span>  \\n+{check}", unsafe_allow_html=True)
    st.caption(f"Owner earnings changed from {format_number(prior['Owner earnings'])}M to {format_number(latest['Owner earnings'])}M when both values are available.")

st.subheader("10-K table (USD millions)")
display = frame.drop(columns="Tags")
for metric in (*METRICS, "ROE", "Owner earnings"):
    display[f"{metric} tag"] = [row["Tags"][metric] for row in report["rows"]]
st.dataframe(display, use_container_width=True, hide_index=True)

st.subheader("Buffett-style memo")
st.caption("Edit only with numbers printed by the calculator.")
edited_memo = st.text_area("Memo text", memo, height=180)
invalid = unsupported_numbers(edited_memo, report)
if invalid:
    st.error("Unsupported number(s): " + ", ".join(invalid) + ". They were not printed by the script.")
else:
    st.success("Every number in this memo was printed by the script.")
