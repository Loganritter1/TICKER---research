"""Compute Buffett-style business-quality evidence from SEC EDGAR company facts.

Usage:
  python edgar_buffett.py COST --user-agent "Your Name your.email@school.edu" --json-out cost.json
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
NOT_FOUND = "not found"
NOT_KNOWN = "not known"

# Ordered tags implement the lab's required fallback rules.
METRICS = {
    "Revenue": (["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"], "flow"),
    "Net income": (["NetIncomeLoss"], "flow"),
    "Operating cash flow": (["NetCashProvidedByUsedInOperatingActivities"], "flow"),
    "Capital spending": (["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"], "flow"),
    "Equity": (["StockholdersEquity"], "instant"),
}


def get_json(url: str, user_agent: str, ca_bundle: str | None = None) -> dict[str, Any]:
    """Fetch SEC JSON with the required identifying User-Agent."""
    if "@" not in user_agent:
        raise ValueError("Pass --user-agent with your name and email address (it must contain @).")
    verify = ca_bundle or os.environ.get("REQUESTS_CA_BUNDLE") or True
    response = requests.get(url, headers={"User-Agent": user_agent, "Accept-Encoding": "gzip, deflate"}, timeout=30, verify=verify)
    response.raise_for_status()
    return response.json()


def cik_for_ticker(ticker: str, user_agent: str, ca_bundle: str | None = None) -> int:
    companies = get_json(TICKERS_URL, user_agent, ca_bundle)
    wanted = ticker.upper()
    for company in companies.values():
        if company["ticker"].upper() == wanted:
            return int(company["cik_str"])
    raise ValueError(f"Ticker {wanted!r} was not found in SEC's ticker list.")


def annual_candidates(fact: dict[str, Any], kind: str) -> list[dict[str, Any]]:
    """Return only 10-K facts for one fiscal year; flows must span one year."""
    units = fact.get("units", {}).get("USD", [])
    candidates = []
    for item in units:
        if item.get("form") != "10-K" or item.get("fp") != "FY" or not item.get("end"):
            continue
        if kind == "flow":
            start = item.get("start")
            if not start:
                continue
            days = (datetime.fromisoformat(item["end"]) - datetime.fromisoformat(start)).days
            if not 300 <= days <= 380:
                continue
        candidates.append(item)
    return candidates


def latest_by_end(fact: dict[str, Any], kind: str) -> dict[str, dict[str, Any]]:
    """Choose the latest filed 10-K where the same fiscal period appears more than once."""
    selected: dict[str, dict[str, Any]] = {}
    for item in annual_candidates(fact, kind):
        end = item["end"]
        if end not in selected or item.get("filed", "") > selected[end].get("filed", ""):
            selected[end] = item
    return selected


def us_gaap_facts(company_facts: dict[str, Any]) -> dict[str, Any]:
    return company_facts.get("facts", {}).get("us-gaap", {})


def available_fiscal_ends(company_facts: dict[str, Any]) -> list[str]:
    """Derive fiscal-year-end dates from annual 10-K income-statement facts."""
    facts = us_gaap_facts(company_facts)
    ends: set[str] = set()
    for tag in ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "NetIncomeLoss"):
        if tag in facts:
            ends.update(latest_by_end(facts[tag], "flow"))
    return sorted(ends)[-5:]


def metric_value(facts: dict[str, Any], tags: list[str], kind: str, fiscal_end: str) -> tuple[float | str, str]:
    """Pick the first permitted tag that has a latest-filed fact for this year."""
    for tag in tags:
        fact = facts.get(tag)
        if not fact:
            continue
        item = latest_by_end(fact, kind).get(fiscal_end)
        if item is not None:
            return item["val"] / 1_000_000, tag
    return NOT_FOUND, NOT_FOUND


def value_or_not_found(value: float | str) -> float | str:
    return round(value, 1) if isinstance(value, (int, float)) else NOT_FOUND


def build_year_row(company_facts: dict[str, Any], fiscal_end: str) -> dict[str, Any]:
    """Turn EDGAR company facts into one lab table row; missing inputs stay explicit."""
    facts = us_gaap_facts(company_facts)
    row: dict[str, Any] = {"Fiscal year end": fiscal_end, "Tags": {}}
    for metric, (tags, kind) in METRICS.items():
        value, tag = metric_value(facts, tags, kind, fiscal_end)
        row[metric] = value_or_not_found(value)
        row["Tags"][metric] = tag

    net_income, equity = row["Net income"], row["Equity"]
    row["ROE"] = (
        round((net_income / equity) * 100, 1)
        if isinstance(net_income, float) and isinstance(equity, float) and equity > 0
        else NOT_KNOWN
    )
    row["Tags"]["ROE"] = "NetIncomeLoss / StockholdersEquity"
    cash_flow, capex = row["Operating cash flow"], row["Capital spending"]
    row["Owner earnings"] = (
        round(cash_flow - capex, 1)
        if isinstance(cash_flow, float) and isinstance(capex, float)
        else NOT_FOUND
    )
    row["Tags"]["Owner earnings"] = "NetCashProvidedByUsedInOperatingActivities - capital spending tag"
    return row


def all_check(values: list[Any], predicate) -> str:
    if not all(isinstance(value, float) for value in values):
        return NOT_KNOWN
    return "pass" if all(predicate(value) for value in values) else "fail"


def buffett_checks(rows: list[dict[str, Any]]) -> dict[str, str]:
    roe = [row["ROE"] for row in rows]
    owner_earnings = [row["Owner earnings"] for row in rows]
    growth = NOT_KNOWN
    if all(isinstance(value, float) for value in owner_earnings):
        growth = "pass" if owner_earnings[-1] > owner_earnings[0] else "fail"
    return {
        "ROE of 15% or more every year": all_check(roe, lambda value: value >= 15),
        "Owner earnings positive every year": all_check(owner_earnings, lambda value: value > 0),
        "Owner earnings grew, first year to last": growth,
    }


def analyze_ticker(ticker: str, user_agent: str, ca_bundle: str | None = None) -> dict[str, Any]:
    cik = cik_for_ticker(ticker, user_agent, ca_bundle)
    facts = get_json(FACTS_URL.format(cik=cik), user_agent, ca_bundle)
    rows = [build_year_row(facts, end) for end in available_fiscal_ends(facts)]
    if len(rows) != 5:
        raise ValueError(f"SEC returned {len(rows)} usable annual 10-K periods; expected five.")
    return {"ticker": ticker.upper(), "cik": f"{cik:010d}", "units": "USD millions", "rows": rows, "checks": buffett_checks(rows)}


def format_number(value: Any, suffix: str = "") -> str:
    if not isinstance(value, float):
        return str(value)
    number = f"{value:,.1f}" if suffix or not value.is_integer() else f"{value:,.0f}"
    return f"{number}{suffix}"


def print_report(report: dict[str, Any]) -> None:
    print(f"{report['ticker']} | CIK {report['cik']} | USD millions")
    for row in report["rows"]:
        print(f"\nFY end {row['Fiscal year end']}")
        for metric in (*METRICS, "ROE", "Owner earnings"):
            suffix = "%" if metric == "ROE" else ""
            print(f"  {metric}: {format_number(row[metric], suffix)} [{row['Tags'][metric]}]")
    print("\nBuffett checks")
    for check, result in report["checks"].items():
        print(f"  {check}: {result}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute 10-K-only Buffett evidence from SEC EDGAR.")
    parser.add_argument("ticker")
    parser.add_argument("--user-agent", required=True, help="Your name and email, required by SEC.")
    parser.add_argument("--ca-bundle", help="Path to your school's trusted CA bundle, if required by its network.")
    parser.add_argument("--json-out", type=Path, help="Optional file for the app or memo workflow.")
    args = parser.parse_args()
    report = analyze_ticker(args.ticker, args.user_agent, args.ca_bundle)
    print_report(report)
    if args.json_out:
        args.json_out.write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
