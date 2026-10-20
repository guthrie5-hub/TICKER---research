"""Meridian baseline portfolios: return, volatility, and mandate reserve test."""

from math import sqrt


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
