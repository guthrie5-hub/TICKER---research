"""Adobe Project 1 comparable-company calculation.

All monetary inputs are USD millions except share price and EPS.  Values are
entered from filings and dated price records in adobe_project1_sources.md; this
file deliberately does not download market data.  It uses the standard library
only.
"""

from statistics import median


# ---------------------------------------------------------------------------
# EDITABLE INPUTS — valuation date: September 24, 2026
# ---------------------------------------------------------------------------
TARGET = {
    "ticker": "ADBE",
    "price": 238.93,
    "point_shares": 389.2,
    "cash_and_investments": 5639.0,
    "debt": 6363.0,
    "ltm_revenue": 25970.0,
    "annual_diluted_eps": 16.70,  # FY2025 GAAP, not adjusted EPS
}

# Only the two candidates admitted by the written peer policy appear here.
# Their last-reported balance-sheet figures predate the valuation date; that
# timing limitation belongs in the source record and interpretation.
PEERS = [
    {
        "ticker": "ADSK",
        "price": 211.35,
        "point_shares": 209.0,
        "cash_and_investments": 4360.0,
        "debt": 3484.0,
        "ltm_revenue": 7790.0,
        "annual_diluted_eps": 5.23,  # FY2026 GAAP
    },
    {
        "ticker": "DOCU",
        "price": 68.99,
        "point_shares": 186.902452,
        "cash_and_investments": 990.4,
        "debt": 0.0,
        "ltm_revenue": 3361.191,
        "annual_diluted_eps": 1.48,  # FY2026 GAAP
    },
]


def calculate(company):
    """Return point-in-time EV and the two defined multiples."""
    market_cap = company["price"] * company["point_shares"]
    enterprise_value = market_cap + company["debt"] - company["cash_and_investments"]
    revenue = company["ltm_revenue"]
    eps = company["annual_diluted_eps"]
    return {
        **company,
        "market_cap": market_cap,
        "enterprise_value": enterprise_value,
        "ev_revenue": enterprise_value / revenue if revenue > 0 else None,
        "pe": company["price"] / eps if eps > 0 and company["price"] > 0 else None,
    }


def implied_ev_revenue_price(target, multiple):
    implied_ev = target["ltm_revenue"] * multiple
    implied_equity = implied_ev + target["cash_and_investments"] - target["debt"]
    return implied_equity / target["point_shares"]


def implied_pe_price(target, multiple):
    return target["annual_diluted_eps"] * multiple


def print_multiples(rows):
    print("Comparable-company multiples — 2026-09-24 price date")
    print("Ticker     Market cap       EV      EV / LTM revenue       P / reported diluted EPS")
    print("-" * 82)
    for row in rows:
        ev_rev = "not meaningful" if row["ev_revenue"] is None else f"{row['ev_revenue']:.6f}x"
        pe = "not meaningful" if row["pe"] is None else f"{row['pe']:.6f}x"
        print(
            f"{row['ticker']:<7}${row['market_cap']:>10,.1f}m ${row['enterprise_value']:>10,.1f}m"
            f" {ev_rev:>18} {pe:>25}"
        )


def print_implied_prices(target, peers):
    ev_multiples = [row["ev_revenue"] for row in peers if row["ev_revenue"] is not None]
    pe_multiples = [row["pe"] for row in peers if row["pe"] is not None]
    print("\nImplied ADBE prices — methods shown separately; never averaged")
    if ev_multiples:
        print("EV / LTM revenue")
        for label, multiple in (
            ("Minimum", min(ev_multiples)), ("Median", median(ev_multiples)),
            ("Maximum", max(ev_multiples)),
        ):
            print(f"{label:<8} {multiple:.6f}x  ->  ${implied_ev_revenue_price(target, multiple):.2f} per share")
    else:
        print("EV / LTM revenue: no usable peers")

    if pe_multiples:
        print("\nP / reported annual diluted EPS")
        for label, multiple in (
            ("Minimum", min(pe_multiples)), ("Median", median(pe_multiples)),
            ("Maximum", max(pe_multiples)),
        ):
            print(f"{label:<8} {multiple:.6f}x  ->  ${implied_pe_price(target, multiple):.2f} per share")
    else:
        print("P / reported annual diluted EPS: no usable peers")


def main():
    target = calculate(TARGET)
    peers = [calculate(peer) for peer in PEERS if peer["ticker"] != TARGET["ticker"]]
    print_multiples([target, *peers])
    print_implied_prices(target, peers)
    print("\nDefinitions: EV = price × point-in-time shares + debt − cash and short-term investments.")
    print("P/E uses each issuer's latest annual GAAP diluted EPS public by the price date.")


if __name__ == "__main__":
    main()
