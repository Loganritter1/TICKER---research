# Lab 17 — Point-in-Time Audit

## Decision question

Was each number in the selected interest-rate series knowable on the day it would have been traded on, and may Project 2 use it?

## App and known-answer check

The Streamlit app is [asof_app.py](asof_app.py). Run it from this folder:

```powershell
.venv\Scripts\python.exe -m streamlit run asof_app.py
```

It downloads current observations from FRED and a dated vintage from ALFRED separately for every selected ID. It excludes missing `.` observations, restricts the vintage to measurement dates on or before the selected “as known on” date, and compares the current and vintage values only on matching measurement dates. Those controls prevent both a future-release leak and a “today's data twice” revision check.

On 5 October 2026, the app reproduced the required last known observations: BAA September 2026 at 6.47, FEDFUNDS September 2026 at 3.75, DGS10 2 October 2026 at 5.28, and MORTGAGE30US 1 October 2026 at 7.28. The PAYEMS probe on 15 January 2025 returned December 2024 at 159,536 in the vintage, 158,316 today for the same month, and 59 revised same-date values (with the 2020 start-date control).

## Data card — DGS10

| Field | Evidence |
|---|---|
| Source and link | Federal Reserve Bank of St. Louis, [FRED DGS10 page](https://fred.stlouisfed.org/series/DGS10); historical vintages from [ALFRED](https://alfred.stlouisfed.org/series?seid=DGS10). |
| What it measures | Market yield on U.S. Treasury securities at a constant 10-year maturity. |
| Units | Percent, not seasonally adjusted; daily frequency. |
| Publication lag | Usually available for the measurement date or the next business day; the app determines the actual availability date from the ALFRED vintage rather than assuming a fixed lag. |
| Revisions | The audit compares each vintage value to the current FRED value on the same date. A zero revised count in the app supports that daily market-rate revisions were not observed for that selected vintage; it does not establish that revisions can never occur. |
| Download date | 2026-10-29 (the app downloads live FRED and ALFRED CSV files when run). |
| Three values hand-checked | FRED showed DGS10 at 5.29 on 30 September 2026, 5.24 on 1 October, and 5.28 on 2 October; the 2 October ALFRED vintage value known on 5 October also displayed as 5.28 in the app. |

## Partner attack and response

**Attack prompt — confirm this with your partner before submitting.** “I trust the publication-date field least: a daily observation date is not automatically an intraday tradable timestamp, so treating the yield as known at that day's market open could still leak information.”

**Response.** The app's ALFRED download shows which dated observations were available by each decision date, and the “current values after that date” count makes the release lag visible. For Project 2, I will use DGS10 only as known by the prior completed decision date (or explicitly trade after its availability), not as a same-day opening signal.

## Call

**Admit with an as-of rule:** DGS10 may be used for Project 2 only from the ALFRED vintage available on or before each decision date, with a one-completed-business-day buffer for a daily trading decision. I would quarantine it if the app shows missing vintage coverage, a material same-date revision, or if the strategy requires intraday availability that the series cannot document.

## Reflection

The as-known-on control separates the day an interest rate was measured from the day the dataset made that observation available. A backtest using today's FRED values could overstate performance if it trades on a release before it was published or silently relies on a later revision.

## AI-use note

OpenAI Codex assisted with the Streamlit code and this draft. Codex's automated checks reproduced the required known-answer and PAYEMS outputs. Before submitting, I will run the app myself and can explain the two download functions and the date filters.
