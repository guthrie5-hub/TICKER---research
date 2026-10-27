"""Point-in-time filter for the fictional retail card-spend training table."""

from collections import defaultdict
from datetime import date, datetime


# ---------------- Editable inputs ----------------
DECISION_DATE = "2026-03-31"

ROWS = [
    {"row": 1, "ticker": "AAA", "month": "2026-01", "published_on": "2026-02-10", "index": 101.0},
    {"row": 2, "ticker": "AAA", "month": "2026-02", "published_on": "2026-03-10", "index": 104.0},
    {"row": 3, "ticker": "AAA", "month": "2026-03", "published_on": "2026-04-10", "index": 109.0},
    {"row": 4, "ticker": "AAA", "month": "2026-02", "published_on": "2026-03-25", "index": 103.0},
    {"row": 5, "ticker": "BBB", "month": "2026-01", "published_on": "2026-02-10", "index": 98.0},
    {"row": 6, "ticker": "BBB", "month": "2026-02", "published_on": "2026-03-10", "index": 97.0},
    {"row": 7, "ticker": "BBB", "month": "2026-02", "published_on": "2026-03-10", "index": 97.0},
    {"row": 8, "ticker": "BBB", "month": "2026-03", "published_on": "2026-04-10", "index": 92.0},
    {"row": 9, "ticker": "CCC", "month": "2026-01", "published_on": "2026-02-10", "index": 110.0},
    {"row": 10, "ticker": "CCC", "month": "2026-02", "published_on": "2026-04-05", "index": 112.0},
    {"row": 11, "ticker": "", "month": "2026-02", "published_on": "2026-03-10", "index": 99.0},
    {"row": 12, "ticker": "CCC", "month": "2026-02", "published_on": "2026-03-10", "index": 111.0},
]


def publication_date(row):
    """Convert a row's publication date to a date object."""
    return date.fromisoformat(row["published_on"])


def quarantine_missing_ticker(rows):
    """Remove rows without a ticker, returning kept and removed rows."""
    removed = [row for row in rows if not row["ticker"].strip()]
    kept = [row for row in rows if row["ticker"].strip()]
    return kept, removed


def remove_exact_duplicates(rows):
    """Keep the first occurrence of an otherwise identical data row."""
    seen = set()
    kept, removed = [], []
    for row in rows:
        key = (row["ticker"], row["month"], row["published_on"], row["index"])
        if key in seen:
            removed.append(row)
        else:
            seen.add(key)
            kept.append(row)
    return kept, removed


def remove_late_publications(rows, decision_date):
    """Keep only rows published on or before the decision date."""
    cutoff = date.fromisoformat(decision_date)
    kept = [row for row in rows if publication_date(row) <= cutoff]
    removed = [row for row in rows if publication_date(row) > cutoff]
    return kept, removed


def keep_latest_revisions(rows):
    """Keep the latest publication for each ticker and measured month."""
    latest = {}
    for row in rows:
        key = (row["ticker"], row["month"])
        if key not in latest or publication_date(row) > publication_date(latest[key]):
            latest[key] = row
    kept_row_numbers = {row["row"] for row in latest.values()}
    kept = [row for row in rows if row["row"] in kept_row_numbers]
    removed = [row for row in rows if row["row"] not in kept_row_numbers]
    return kept, removed


def print_funnel_step(label, removed):
    """Print one filter step and its preserved row numbers."""
    row_numbers = ", ".join(str(row["row"]) for row in removed) or "none"
    print(f"{label}: removed {len(removed)} row(s): {row_numbers}")


def print_panel(rows):
    """Print the remaining as-of rows in a readable table."""
    print("\nAs-of panel")
    print("Row  Ticker  Month measured  Published on  Index")
    for row in sorted(rows, key=lambda value: (value["ticker"], value["month"], value["row"])):
        print(f"{row['row']:>3}  {row['ticker']:<6}  {row['month']:<14}  {row['published_on']:<12}  {row['index']:.1f}")


def signals(rows):
    """Return each ticker's latest-month change from the preceding measured month."""
    by_ticker = defaultdict(list)
    for row in rows:
        by_ticker[row["ticker"]].append(row)
    result = {}
    for ticker, ticker_rows in by_ticker.items():
        ticker_rows.sort(key=lambda row: datetime.strptime(row["month"], "%Y-%m"))
        if len(ticker_rows) < 2:
            result[ticker] = None
            continue
        previous, latest = ticker_rows[-2:]
        result[ticker] = (latest["month"], latest["index"] / previous["index"] - 1.0)
    return result


def print_signals(title, rows):
    """Print signals from a supplied panel."""
    print(f"\n{title}")
    for ticker, result in signals(rows).items():
        if result is None:
            print(f"{ticker}: unavailable (fewer than two months)")
        else:
            month, change = result
            print(f"{ticker}: {month} {change * 100:+.2f}%")


def main():
    print(f"Decision date: {DECISION_DATE}\n")
    print("Row funnel")
    after_quarantine, removed = quarantine_missing_ticker(ROWS)
    print_funnel_step("Quarantine missing ticker", removed)
    after_duplicates, removed = remove_exact_duplicates(after_quarantine)
    print_funnel_step("Remove exact duplicates", removed)
    after_late, removed = remove_late_publications(after_duplicates, DECISION_DATE)
    print_funnel_step("Remove late publications", removed)
    asof_panel, removed = keep_latest_revisions(after_late)
    print_funnel_step("Keep latest knowable revision", removed)

    print_panel(asof_panel)
    print_signals("As-of signals", asof_panel)

    # Naive comparison still applies basic data-quality rules, but incorrectly keeps
    # all publication dates before choosing the latest revision for each month.
    naive_panel, _ = keep_latest_revisions(after_duplicates)
    print_signals("Naive signals (ignores publication date)", naive_panel)


if __name__ == "__main__":
    main()
