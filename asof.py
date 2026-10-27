"""Lab 16: point-in-time (as-of) data filter.  Standard library only."""

import csv
from datetime import date
from io import StringIO


# Editable inputs
DECISION_DATE = "2026-03-31"
TABLE = """row,ticker,month,published_on,index
1,AAA,2026-01,2026-02-10,101.0
2,AAA,2026-02,2026-03-10,104.0
3,AAA,2026-03,2026-04-10,109.0
4,AAA,2026-02,2026-03-25,103.0
5,BBB,2026-01,2026-02-10,98.0
6,BBB,2026-02,2026-03-10,97.0
7,BBB,2026-02,2026-03-10,97.0
8,BBB,2026-03,2026-04-10,92.0
9,CCC,2026-01,2026-02-10,110.0
10,CCC,2026-02,2026-04-05,112.0
11,,2026-02,2026-03-10,99.0
12,CCC,2026-02,2026-03-10,111.0
"""


def read_rows(table):
    """Convert the editable CSV text into typed row dictionaries."""
    rows = []
    for row in csv.DictReader(StringIO(table.strip())):
        rows.append(
            {
                "row": int(row["row"]),
                "ticker": row["ticker"].strip(),
                "month": row["month"],
                "published_on": date.fromisoformat(row["published_on"]),
                "index": float(row["index"]),
            }
        )
    return rows


def show_removal(label, removed):
    numbers = ", ".join(str(row["row"]) for row in removed) or "none"
    print(f"{label}: {len(removed)} removed (rows: {numbers})")


def keep_latest_revision(rows):
    """For each ticker/month, retain the row with the latest publication date."""
    latest_by_series = {}
    for row in rows:
        key = (row["ticker"], row["month"])
        if key not in latest_by_series or row["published_on"] > latest_by_series[key]["published_on"]:
            latest_by_series[key] = row

    kept = list(latest_by_series.values())
    kept_row_numbers = {row["row"] for row in kept}
    removed = [row for row in rows if row["row"] not in kept_row_numbers]
    return sorted(kept, key=lambda row: row["row"]), removed


def month_name(month_text):
    """Turn an ISO month such as 2026-02 into February."""
    names = (
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    )
    return names[int(month_text[5:7]) - 1]


def print_signals(title, rows, revised_ticker_months=(), mark_revisions=False):
    print(f"\n{title}")
    by_ticker = {}
    for row in rows:
        by_ticker.setdefault(row["ticker"], []).append(row)

    for ticker in sorted(by_ticker):
        series = sorted(by_ticker[ticker], key=lambda row: row["month"])
        if len(series) < 2:
            print(f"{ticker}: not enough monthly observations")
            continue
        previous, latest = series[-2], series[-1]
        change = (latest["index"] / previous["index"] - 1) * 100
        label = month_name(latest["month"])
        if mark_revisions and (ticker, latest["month"]) in revised_ticker_months:
            label += ", revised"
        print(f"{ticker}: {change:+.2f}% ({label})")


def main():
    decision_date = date.fromisoformat(DECISION_DATE)
    original_rows = read_rows(TABLE)

    # Rule 1: quarantine rows that cannot be assigned to a ticker.
    rows = [row for row in original_rows if row["ticker"]]
    quarantined = [row for row in original_rows if not row["ticker"]]

    # Rule 2: remove exact duplicate observations, keeping the first instance.
    seen = set()
    deduplicated = []
    duplicates = []
    for row in rows:
        fingerprint = (row["ticker"], row["month"], row["published_on"], row["index"])
        if fingerprint in seen:
            duplicates.append(row)
        else:
            seen.add(fingerprint)
            deduplicated.append(row)
    rows = deduplicated

    # Rule 3: discard publications that were unavailable on the decision date.
    after_decision = [row for row in rows if row["published_on"] > decision_date]
    rows = [row for row in rows if row["published_on"] <= decision_date]

    # Rule 4: for each ticker/month, use the newest publication available then.
    asof_rows, superseded = keep_latest_revision(rows)

    print(f"Decision date: {decision_date.isoformat()}")
    print("\nRow funnel")
    show_removal("Quarantined: no ticker", quarantined)
    show_removal("Exact duplicate", duplicates)
    show_removal(f"Published after {decision_date.isoformat()}", after_decision)
    show_removal("Older vintage replaced by a revision", superseded)

    print("\nAs-of panel")
    for row in asof_rows:
        print(
            f"row {row['row']}: {row['ticker']} {row['month']} "
            f"published {row['published_on'].isoformat()} index {row['index']:.1f}"
        )
    print_signals("As-of signals", asof_rows)

    # Naive comparison: ignore publication date, but still use the newest revision.
    naive_source = [row for row in original_rows if row["ticker"]]
    naive_no_duplicates = []
    seen = set()
    for row in naive_source:
        fingerprint = (row["ticker"], row["month"], row["published_on"], row["index"])
        if fingerprint not in seen:
            seen.add(fingerprint)
            naive_no_duplicates.append(row)
    naive_rows, _ = keep_latest_revision(naive_no_duplicates)
    revision_counts = {}
    for row in naive_no_duplicates:
        key = (row["ticker"], row["month"])
        revision_counts[key] = revision_counts.get(key, 0) + 1
    revised_ticker_months = {
        key for key, count in revision_counts.items() if count > 1
    }
    print_signals(
        "Naive signals (ignoring publication date)",
        naive_rows,
        revised_ticker_months,
        mark_revisions=True,
    )


if __name__ == "__main__":
    main()
