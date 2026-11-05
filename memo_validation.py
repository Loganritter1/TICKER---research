"""Validate that a memo uses only numeric evidence printed by the calculator."""

import re
from decimal import Decimal, InvalidOperation

from edgar_buffett import METRICS, format_number

CALCULATED_METRICS = ("ROE", "Owner earnings", "Current ratio", "Liabilities / equity")

# Do not treat the filing label "10-K" as a financial claim in a memo.
NUMBER_PATTERN = re.compile(r"(?<![\w.])-?\$?\d[\d,]*(?:\.\d+)?%?(?![\d,]*(?:\.\d+)?%?-K\b)")


def normalized_number(text: str) -> str | None:
    cleaned = text.replace("$", "").replace(",", "").replace("%", "")
    try:
        return str(Decimal(cleaned).normalize())
    except InvalidOperation:
        return None


def printed_numbers(report: dict) -> set[str]:
    allowed = {normalized_number(str(report["cik"]))}
    for row in report["rows"]:
        for piece in row["Fiscal year end"].split("-"):
            allowed.add(normalized_number(piece))
        for metric in (*METRICS, *CALCULATED_METRICS):
            allowed.add(normalized_number(format_number(row[metric], "%" if metric == "ROE" else "")))
    allowed.update({normalized_number("15%"), normalized_number("2")})
    return {value for value in allowed if value is not None}


def unsupported_numbers(memo: str, report: dict) -> list[str]:
    allowed = printed_numbers(report)
    invalid = []
    for token in NUMBER_PATTERN.findall(memo):
        normalized = normalized_number(token)
        if normalized is not None and normalized not in allowed and token not in invalid:
            invalid.append(token)
    return invalid
