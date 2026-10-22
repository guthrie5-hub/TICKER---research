"""Meridian baseline portfolios: return, volatility, and mandate reserve test."""

import csv
from datetime import date
from math import sqrt
from statistics import mean, stdev


# ---------------- Editable inputs ----------------
SLEEVES = {
    "Treasury bills": {"return": 0.035, "volatility": 0.005, "reserve_eligible": True},
    "Treasury 10-year note": {"return": 0.043, "volatility": 0.070, "reserve_eligible": True},
    "Investment-grade bond fund": {"return": 0.050, "volatility": 0.060, "reserve_eligible": False},
    "Global equity index fund": {"return": 0.080, "volatility": 0.160, "reserve_eligible": False},
}

CORRELATION = {
    "Treasury bills": {
        "Treasury bills": 1.00, "Treasury 10-year note": 0.10,
        "Investment-grade bond fund": 0.05, "Global equity index fund": 0.00,
    },
    "Treasury 10-year note": {
        "Treasury bills": 0.10, "Treasury 10-year note": 1.00,
        "Investment-grade bond fund": 0.80, "Global equity index fund": -0.10,
    },
    "Investment-grade bond fund": {
        "Treasury bills": 0.05, "Treasury 10-year note": 0.80,
        "Investment-grade bond fund": 1.00, "Global equity index fund": 0.25,
    },
    "Global equity index fund": {
        "Treasury bills": 0.00, "Treasury 10-year note": -0.10,
        "Investment-grade bond fund": 0.25, "Global equity index fund": 1.00,
    },
}

OBJECTIVE_RETURN = 0.065
MINIMUM_RESERVE_ELIGIBLE_WEIGHT = 0.03


def validate_correlation(correlation, sleeves):
    """Raise a clear error if the correlation table is invalid."""
    for left in sleeves:
        if left not in correlation:
            raise ValueError(f"Correlation table is missing row: {left}")
        for right in sleeves:
            if right not in correlation[left]:
                raise ValueError(f"Correlation table is missing {left} / {right}")
            value = correlation[left][right]
            if not -1.0 <= value <= 1.0:
                raise ValueError(f"Correlation for {left} / {right} is outside -1 to 1: {value}")
            if abs(value - correlation[right][left]) > 1e-12:
                raise ValueError(f"Correlation table is not symmetric at {left} / {right}")


def covariance_matrix(sleeves, correlation):
    """Return covariance[sleeve][sleeve] = correlation × volatilities."""
    return {
        left: {
            right: correlation[left][right] * sleeves[left]["volatility"] * sleeves[right]["volatility"]
            for right in sleeves
        }
        for left in sleeves
    }


def benchmark_weights(sleeves):
    """Return Meridian's stated 40% IG bond / 60% equity benchmark."""
    return {name: (0.40 if name == "Investment-grade bond fund" else 0.60 if name == "Global equity index fund" else 0.0) for name in sleeves}


def equal_weight_weights(sleeves):
    """Return equal weights across all sleeves."""
    return {name: 1.0 / len(sleeves) for name in sleeves}


def inverse_volatility_weights(sleeves):
    """Return weights proportional to 1 / volatility."""
    inverse = {name: 1.0 / values["volatility"] for name, values in sleeves.items()}
    total = sum(inverse.values())
    return {name: value / total for name, value in inverse.items()}


def expected_return(weights, sleeves):
    """Return the weighted expected return."""
    return sum(weights[name] * sleeves[name]["return"] for name in sleeves)


def portfolio_volatility(weights, covariance, sleeves):
    """Return sqrt(w' covariance w)."""
    variance = sum(
        weights[left] * weights[right] * covariance[left][right]
        for left in sleeves for right in sleeves
    )
    if variance < -1e-12:
        raise ValueError(f"Portfolio variance is negative: {variance}")
    return sqrt(max(0.0, variance))


def reserve_eligible_weight(weights, sleeves):
    """Return the bills plus 10-year-note weight."""
    return sum(weights[name] for name in sleeves if sleeves[name]["reserve_eligible"])


def search_lowest_risk_mix(sleeves, correlation, objective_return, minimum_reserve_weight=0.0, step=0.05):
    """Search long-only weight mixes and return the valid mix with lowest volatility.

    `step` is a decimal weight: 0.05 means five percentage-point steps.
    Returns None when no mix satisfies both requirements.
    """
    validate_correlation(correlation, sleeves)
    names = list(sleeves)
    units = round(1.0 / step)
    if units <= 0 or abs(units * step - 1.0) > 1e-10:
        raise ValueError("Search step must divide 100% exactly.")
    covariance = covariance_matrix(sleeves, correlation)
    best = None

    def try_weights(position, units_left, partial):
        nonlocal best
        if position == len(names) - 1:
            weights = dict(partial)
            weights[names[position]] = units_left / units
            portfolio_return = expected_return(weights, sleeves)
            reserve_weight = reserve_eligible_weight(weights, sleeves)
            if portfolio_return < objective_return or reserve_weight < minimum_reserve_weight:
                return
            volatility = portfolio_volatility(weights, covariance, sleeves)
            candidate = {
                "weights": weights,
                "return": portfolio_return,
                "volatility": volatility,
                "reserve_eligible_weight": reserve_weight,
            }
            if best is None or candidate["volatility"] < best["volatility"]:
                best = candidate
            return
        for asset_units in range(units_left + 1):
            partial[names[position]] = asset_units / units
            try_weights(position + 1, units_left - asset_units, partial)
        partial.pop(names[position], None)

    try_weights(0, units, {})
    return best


def estimate_from_prices(csv_source, last_36_months=False):
    """Estimate annual returns, volatility, and correlations from monthly Adj Close CSV data.

    The CSV must have Date first, oldest date first, and one positive-price column
    per asset. Estimated returns are historical averages, not forecasts.
    """
    close_after = False
    if isinstance(csv_source, (str, bytes)):
        csv_source = open(csv_source, newline="")
        close_after = True
    try:
        reader = csv.DictReader(csv_source)
        columns = reader.fieldnames or []
        if len(columns) < 3 or columns[0] != "Date":
            raise ValueError("CSV must have Date as the first column and at least two asset columns.")
        names = columns[1:]
        prices = {name: [] for name in names}
        previous_date = None
        for row_number, row in enumerate(reader, start=2):
            try:
                current_date = date.fromisoformat(row["Date"])
            except (TypeError, ValueError) as error:
                raise ValueError(f"Invalid ISO date in row {row_number}: {row.get('Date')!r}") from error
            if previous_date is not None and current_date <= previous_date:
                raise ValueError("CSV dates must be oldest first with no duplicates.")
            previous_date = current_date
            for name in names:
                try:
                    price = float(row[name])
                except (TypeError, ValueError) as error:
                    raise ValueError(f"Invalid price for {name} in row {row_number}.") from error
                if price <= 0:
                    raise ValueError(f"Price for {name} in row {row_number} must be positive.")
                prices[name].append(price)
    finally:
        if close_after:
            csv_source.close()

    if any(len(values) < 3 for values in prices.values()):
        raise ValueError("CSV needs at least three monthly price rows.")
    monthly_returns = {
        name: [later / earlier - 1.0 for earlier, later in zip(values, values[1:])]
        for name, values in prices.items()
    }
    if last_36_months:
        monthly_returns = {name: values[-36:] for name, values in monthly_returns.items()}
    observations = len(next(iter(monthly_returns.values())))
    if observations < 2:
        raise ValueError("At least two monthly returns are required.")

    sleeves = {
        name: {"return": mean(values) * 12.0, "volatility": stdev(values) * sqrt(12.0), "reserve_eligible": False}
        for name, values in monthly_returns.items()
    }
    if any(values["volatility"] == 0.0 for values in sleeves.values()):
        raise ValueError("A zero-volatility asset cannot produce a correlation estimate.")
    correlation = {}
    for left in sleeves:
        correlation[left] = {}
        for right in sleeves:
            covariance = sum(
                (a - mean(monthly_returns[left])) * (b - mean(monthly_returns[right]))
                for a, b in zip(monthly_returns[left], monthly_returns[right])
            ) / (observations - 1)
            calculated = covariance / (stdev(monthly_returns[left]) * stdev(monthly_returns[right]))
            # Floating-point arithmetic can make a diagonal value 1.0000000000000002.
            correlation[left][right] = max(-1.0, min(1.0, calculated))
    return sleeves, correlation


def print_portfolio(name, weights, sleeves, covariance, objective_return):
    """Print one baseline portfolio."""
    ret = expected_return(weights, sleeves)
    vol = portfolio_volatility(weights, covariance, sleeves)
    reserve = reserve_eligible_weight(weights, sleeves)
    print(f"\n{name}")
    print("Weights:")
    for sleeve in sleeves:
        print(f"  {sleeve}: {weights[sleeve] * 100:.1f}%")
    print(f"Expected return: {ret * 100:.2f}%")
    print(f"Volatility: {vol * 100:.2f}%")
    print(f"Reserve-eligible weight: {reserve * 100:.1f}%")
    print(f"Expected return meets {objective_return * 100:.1f}% objective: {'yes' if ret >= objective_return else 'no'}")


def main():
    validate_correlation(CORRELATION, SLEEVES)
    covariance = covariance_matrix(SLEEVES, CORRELATION)
    portfolios = {
        "Benchmark (40% IG bonds / 60% global equity)": benchmark_weights(SLEEVES),
        "Equal weight": equal_weight_weights(SLEEVES),
        "Inverse volatility": inverse_volatility_weights(SLEEVES),
    }
    for name, weights in portfolios.items():
        print_portfolio(name, weights, SLEEVES, covariance, OBJECTIVE_RETURN)


if __name__ == "__main__":
    main()
