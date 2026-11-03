"""SEC EDGAR 10-K owner-earnings report for a single ticker."""

import json
import os
import ssl
import sys
from datetime import date
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import certifi


TICKER_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
FLOW_TAGS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"],
    "net_income": ["NetIncomeLoss"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capital_spending": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
}
INSTANT_TAGS = {"equity": ["StockholdersEquity"]}


def user_agent():
    """Require a temporary, SEC-compliant contact without saving it in this project."""
    value = os.environ.get("SEC_USER_AGENT", "").strip()
    if not value or "@" not in value:
        raise ValueError(
            "Set SEC_USER_AGENT to your name and email for this session; for example: "
            "SEC_USER_AGENT='Your Name your.email@school.edu'"
        )
    return value


def get_json(url):
    """Download one keyless SEC JSON endpoint."""
    request = Request(url, headers={"User-Agent": user_agent()})
    try:
        with urlopen(request, timeout=30, context=SSL_CONTEXT) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise ValueError(f"SEC returned HTTP {error.code}.") from error
    except URLError as error:
        raise ValueError(f"Could not reach SEC EDGAR: {error.reason}") from error


def ticker_to_cik(ticker):
    """Look up a ticker in SEC's public ticker-to-CIK file."""
    ticker = ticker.upper().strip()
    for company in get_json(TICKER_URL).values():
        if company["ticker"].upper() == ticker:
            return int(company["cik_str"]), company["title"]
    raise ValueError(f"Ticker {ticker!r} was not found in SEC's company_tickers.json.")


def annual_duration(fact):
    """Return whether a flow fact represents approximately one fiscal year."""
    if "start" not in fact or "end" not in fact:
        return False
    days = (date.fromisoformat(fact["end"]) - date.fromisoformat(fact["start"])).days
    return 300 <= days <= 380


def candidates(company_facts, tag, end, is_flow):
    """Return 10-K facts for one tag and fiscal-year end, latest filing first."""
    fact = company_facts.get("facts", {}).get("us-gaap", {}).get(tag, {})
    units = fact.get("units", {}).get("USD", [])
    selected = [
        row for row in units
        if row.get("form") == "10-K" and row.get("end") == end
        and (annual_duration(row) if is_flow else True)
    ]
    return sorted(selected, key=lambda row: (row.get("filed", ""), row.get("accn", "")), reverse=True)


def resolve_metric(company_facts, tags, end, is_flow):
    """Resolve the first allowed XBRL tag that has a valid 10-K fact for this year-end."""
    for tag in tags:
        rows = candidates(company_facts, tag, end, is_flow)
        if rows:
            return {"value": rows[0]["val"], "tag": tag, "filed": rows[0].get("filed", "")}
    return {"value": None, "tag": "not found", "filed": ""}


def fiscal_year_ends(company_facts):
    """Find the five latest 10-K fiscal-year ends represented by required facts."""
    ends = set()
    for tag in [tag for tags in FLOW_TAGS.values() for tag in tags] + ["StockholdersEquity"]:
        fact = company_facts.get("facts", {}).get("us-gaap", {}).get(tag, {})
        for row in fact.get("units", {}).get("USD", []):
            if row.get("form") == "10-K" and (annual_duration(row) if tag in sum(FLOW_TAGS.values(), []) else True):
                ends.add(row["end"])
    return sorted(ends)[-5:]


def ratio_or_not_known(numerator, denominator):
    """Return a ratio only when both inputs support it."""
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator / denominator


def owner_earnings(operating_cash_flow, capital_spending):
    """Compute owner earnings only from found cash-flow inputs."""
    if operating_cash_flow is None or capital_spending is None:
        return None
    return operating_cash_flow - capital_spending


def check_all(values, predicate):
    """Return pass, fail, or not known for a yearly check."""
    if any(value is None for value in values):
        return "not known"
    return "pass" if all(predicate(value) for value in values) else "fail"


def check_growth(values):
    """Check owner-earnings growth from the first year to the last year."""
    if len(values) < 2 or values[0] is None or values[-1] is None:
        return "not known"
    return "pass" if values[-1] > values[0] else "fail"


def analyse_ticker(ticker):
    """Return the required five-year 10-K-only analysis and checks."""
    cik, company_name = ticker_to_cik(ticker)
    facts = get_json(FACTS_URL.format(cik=cik))
    rows = []
    for end in fiscal_year_ends(facts):
        row = {"fiscal_year_end": end}
        for name, tags in FLOW_TAGS.items():
            row[name] = resolve_metric(facts, tags, end, True)
        for name, tags in INSTANT_TAGS.items():
            row[name] = resolve_metric(facts, tags, end, False)
        row["roe"] = ratio_or_not_known(row["net_income"]["value"], row["equity"]["value"])
        row["owner_earnings"] = owner_earnings(
            row["operating_cash_flow"]["value"], row["capital_spending"]["value"]
        )
        row["owner_earnings_tag"] = (
            f"{row['operating_cash_flow']['tag']} − {row['capital_spending']['tag']}"
            if row["owner_earnings"] is not None else "not found"
        )
        rows.append(row)

    roe_values = [row["roe"] for row in rows]
    owner_values = [row["owner_earnings"] for row in rows]
    checks = {
        "ROE >= 15% every year": check_all(roe_values, lambda value: value >= 0.15),
        "Owner earnings positive every year": check_all(owner_values, lambda value: value > 0),
        "Owner earnings grew, first year to last": check_growth(owner_values),
    }
    return {
        "ticker": ticker.upper(), "company_name": company_name, "cik": f"{cik:010d}",
        "rows": rows, "checks": checks, "download_date": date.today().isoformat(),
    }


def display_value(value, percent=False):
    """Format values without inventing a missing number."""
    if value is None:
        return "not known" if percent else "not found"
    return f"{value * 100:.2f}%" if percent else f"${value / 1_000_000:,.1f}m"


def report_text(result):
    """Build the terminal report; this is the canonical set of displayed numbers."""
    print(f"{result['company_name']} ({result['ticker']}) | CIK {result['cik']} | 10-K only")
    print(f"Download date: {result['download_date']}")
    print("Amounts in USD millions; XBRL tag follows each input.")
    print("Fiscal year end | Revenue | Net income | Operating cash flow | Capital spending | Equity | ROE | Owner earnings")
    for row in result["rows"]:
        cells = [
            row["fiscal_year_end"],
            f"{display_value(row['revenue']['value'])} [{row['revenue']['tag']}]",
            f"{display_value(row['net_income']['value'])} [{row['net_income']['tag']}]",
            f"{display_value(row['operating_cash_flow']['value'])} [{row['operating_cash_flow']['tag']}]",
            f"{display_value(row['capital_spending']['value'])} [{row['capital_spending']['tag']}]",
            f"{display_value(row['equity']['value'])} [{row['equity']['tag']}]",
            f"{display_value(row['roe'], percent=True)} [NetIncomeLoss / StockholdersEquity]",
            f"{display_value(row['owner_earnings'])} [{row['owner_earnings_tag']}]",
        ]
        print(" | ".join(cells))
    print("\nBuffett-style checks")
    for label, outcome in result["checks"].items():
        print(f"{label}: {outcome}")


def memo_text(result):
    """Write a short judgment using only the displayed analysis and check outcomes."""
    checks = result["checks"]
    if all(outcome == "pass" for outcome in checks.values()):
        action = "Own the business"
        reason = "The defined ROE and owner-earnings checks all pass."
    elif checks["Owner earnings positive every year"] == "fail":
        action = "Pass"
        reason = "Owner earnings were not positive in every known year."
    else:
        action = "Watch it"
        reason = "The defined business-quality checks do not all pass or are not known."
    return (
        f"# {result['ticker']} Buffett-style business memo\n\n"
        f"**Decision: {action}.** {reason} This evaluates the business only, not its market price.\n\n"
        "## Decision on this verdict\n\n"
        "I trust this verdict as a limited business-quality screen because it uses five years of "
        "reported 10-K facts, but it does not establish whether the current share price is attractive.\n\n"
        "Source: SEC EDGAR 10-K XBRL facts printed by `edgar_owner_earnings.py`. "
        f"Downloaded {result['download_date']}.\n"
    )


def write_memo(result, path):
    """Save the memo beside the script output."""
    Path(path).write_text(memo_text(result), encoding="utf-8")


def main():
    ticker = sys.argv[1] if len(sys.argv) > 1 else "COST"
    result = analyse_ticker(ticker)
    report_text(result)
    output_path = f"{result['ticker']}_buffett_memo.md"
    write_memo(result, output_path)
    print(f"\nMemo saved: {output_path}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"Error: {error}")
        raise SystemExit(1)
