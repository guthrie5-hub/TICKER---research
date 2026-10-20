"""Meridian Foundation Reserve mandate checker."""

# Editable inputs
HOLDINGS = {
    "Cash": {"issuer": "none", "redeem_days": 0, "reserve_eligible": True},
    "Treasury bills": {
        "issuer": "U.S. Treasury",
        "redeem_days": 1,
        "reserve_eligible": True,
    },
    "Treasury 10-year note": {
        "issuer": "U.S. Treasury",
        "redeem_days": 1,
        "reserve_eligible": True,
    },
    "Global equity index fund": {
        "issuer": "diversified fund",
        "redeem_days": 2,
        "reserve_eligible": False,
    },
    "Investment-grade bond fund": {
        "issuer": "diversified fund",
        "redeem_days": 3,
        "reserve_eligible": False,
    },
    "Private real estate fund": {
        "issuer": "diversified fund",
        "redeem_days": 90,
        "reserve_eligible": False,
    },
    "Acme Corp bonds": {
        "issuer": "Acme Corp",
        "redeem_days": 4,
        "reserve_eligible": False,
    },
    "Acme Corp stock": {
        "issuer": "Acme Corp",
        "redeem_days": 1,
        "reserve_eligible": False,
    },
}

CANDIDATES = {
    "A": {
        "Cash": 2,
        "Treasury bills": 2,
        "Treasury 10-year note": 10,
        "Global equity index fund": 60,
        "Investment-grade bond fund": 26,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1,
        "Treasury bills": 0,
        "Treasury 10-year note": 0,
        "Global equity index fund": 55,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 15,
        "Acme Corp bonds": 5,
        "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1,
        "Treasury bills": 1,
        "Treasury 10-year note": 0,
        "Global equity index fund": 70,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 8,
    },
    "D": {
        "Cash": 0,
        "Treasury bills": 0,
        "Treasury 10-year note": 100,
        "Global equity index fund": 0,
        "Investment-grade bond fund": 0,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
    "E": {
        "Cash": 0,
        "Treasury bills": 0,
        "Treasury 10-year note": 0,
        "Global equity index fund": 60,
        "Investment-grade bond fund": 40,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
}

RESERVE_SIZE = 100.0  # USD millions
QUARTERLY_DISTRIBUTION = 0.75  # USD millions
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_DAYS = 5
MINIMUM_LIQUID_SHARE = 90.0  # percent
ISSUER_LIMIT = 8.0  # percent
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def status(passes: bool) -> str:
    return "pass" if passes else "FAIL"


def check_candidate(name: str, weights: dict[str, float], reserve_minimum: float) -> None:
    total_weight = sum(weights.values())
    lowest_weight = min(weights.values())
    reserve_eligible_weight = sum(
        weight for holding, weight in weights.items() if HOLDINGS[holding]["reserve_eligible"]
    )
    liquid_weight = sum(
        weight
        for holding, weight in weights.items()
        if HOLDINGS[holding]["redeem_days"] <= LIQUIDITY_WINDOW_DAYS
    )

    company_weights: dict[str, float] = {}
    for holding, weight in weights.items():
        issuer = HOLDINGS[holding]["issuer"]
        if issuer not in EXEMPT_ISSUERS:
            company_weights[issuer] = company_weights.get(issuer, 0.0) + weight
    largest_company_weight = max(company_weights.values(), default=0.0)

    checks = [
        ("Weights sum to 100", total_weight, total_weight == 100.0),
        ("Lowest weight not negative", lowest_weight, lowest_weight >= 0.0),
        (
            "Reserve-eligible weight at least reserve minimum",
            reserve_eligible_weight,
            reserve_eligible_weight >= reserve_minimum,
        ),
        (
            "Weight redeemable within liquidity window at least minimum liquid share",
            liquid_weight,
            liquid_weight >= MINIMUM_LIQUID_SHARE,
        ),
        (
            "Largest single company at most issuer limit",
            largest_company_weight,
            largest_company_weight <= ISSUER_LIMIT,
        ),
    ]

    print(f"\nCandidate {name}")
    for label, value, passes in checks:
        print(f"{label}: {value:.1f}% — {status(passes)}")
    print("Calendar-year loss rule: requires CIO clarification")

    failures = sum(not passes for _, _, passes in checks)
    if failures == 0:
        print("passes every checkable rule")
    else:
        print(f"fails {failures} rule(s)")


def main() -> None:
    reserve_minimum = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    print(f"Reserve minimum: {reserve_minimum:.1f}%")
    for name, weights in CANDIDATES.items():
        check_candidate(name, weights, reserve_minimum)


if __name__ == "__main__":
    main()
