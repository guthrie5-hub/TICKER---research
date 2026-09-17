"""Comparable-company P/E valuation. All inputs are entered manually."""

from decimal import Decimal, InvalidOperation
from statistics import median


# Editable inputs. Use None for missing values.
TARGET = {
    "ticker": "ADBE",
    "diluted_eps": "12.36",  # Adobe FY2024 GAAP diluted EPS
}

PEERS = [
    {"ticker": "ADSK", "price": "297.18", "diluted_eps": "5.12"},
    {"ticker": "DOCU", "price": "69.70", "diluted_eps": "5.08"},
]


def decimal_or_none(value):
    """Convert a manual input to Decimal, treating blanks and invalid values as missing."""
    if value is None or value == "":
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def format_multiple(value):
    return "not meaningful" if value is None else f"{value:.6f}x"


def format_price(value):
    return "not meaningful" if value is None else f"${value:,.2f}"


def format_dollar_change(value):
    if value is None:
        return "not meaningful"
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):,.2f}"


def implied_price(multiple, target_eps):
    if multiple is None or target_eps is None or target_eps <= 0:
        return None
    return multiple * target_eps


def main():
    target_ticker = str(TARGET.get("ticker", "")).strip().upper()
    target_eps = decimal_or_none(TARGET.get("diluted_eps"))
    if target_eps is not None and target_eps <= 0:
        target_eps = None

    unique_peers = []
    seen_tickers = set()
    for peer in PEERS:
        ticker = str(peer.get("ticker", "")).strip().upper()
        if not ticker or ticker == target_ticker or ticker in seen_tickers:
            continue
        seen_tickers.add(ticker)
        unique_peers.append(peer)

    valid_peers = []
    print(f"Target: {target_ticker or 'not provided'}")
    print(f"Target diluted EPS: {target_eps if target_eps is not None else 'not meaningful'}")
    print("\nPeer P/E Multiples")
    for peer in unique_peers:
        ticker = str(peer.get("ticker", "")).strip().upper()
        price = decimal_or_none(peer.get("price"))
        eps = decimal_or_none(peer.get("diluted_eps"))
        pe = price / eps if price is not None and eps is not None and price > 0 and eps > 0 else None
        print(f"{ticker}: {format_multiple(pe)}")
        if pe is not None:
            valid_peers.append((ticker, pe))

    print("\nFull-Peer Valuation")
    if not valid_peers:
        print("No usable peers.")
    else:
        multiples = [pe for _, pe in valid_peers]
        minimum_pe = min(multiples)
        median_pe = median(multiples)
        maximum_pe = max(multiples)

        if len(valid_peers) == 1:
            print(f"Reference peer P/E: {format_multiple(median_pe)}")
            print(f"Reference implied price: {format_price(implied_price(median_pe, target_eps))}")
            print("Range: no range (one valid peer).")
        else:
            print(f"Minimum peer P/E: {format_multiple(minimum_pe)}")
            print(f"Median peer P/E: {format_multiple(median_pe)}")
            print(f"Maximum peer P/E: {format_multiple(maximum_pe)}")
            print(f"Minimum implied price: {format_price(implied_price(minimum_pe, target_eps))}")
            print(f"Median implied price: {format_price(implied_price(median_pe, target_eps))}")
            print(f"Maximum implied price: {format_price(implied_price(maximum_pe, target_eps))}")

    print("\nPeer-Removal Sensitivity")
    if not valid_peers:
        print("No estimate: no usable peers.")
        return

    full_median = median([pe for _, pe in valid_peers])
    full_estimate = implied_price(full_median, target_eps)
    for removed_ticker, _ in valid_peers:
        remaining = [pe for ticker, pe in valid_peers if ticker != removed_ticker]
        if not remaining:
            print(f"Remove {removed_ticker}: no estimate (no usable peers remain).")
            continue
        remaining_estimate = implied_price(median(remaining), target_eps)
        if full_estimate is None or remaining_estimate is None:
            change = None
        else:
            change = remaining_estimate - full_estimate
        change_text = format_dollar_change(change)
        print(
            f"Remove {removed_ticker}: median implied price {format_price(remaining_estimate)}; "
            f"change from full-peer estimate {change_text}."
        )


if __name__ == "__main__":
    main()
