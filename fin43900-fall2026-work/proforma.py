"""Five-year ABG pro forma and FCFE valuation for Lab 09.

All dollar amounts are USD millions, except value per share. Edit only the
input blocks below.
"""


# ---- Opening FY2025 balance sheet (USD millions) ----
OPENING = {
    "revenue": 17999.0,
    "cash": 40.4,
    "inventory": 2135.8,
    "ppe": 3070.4,
    "other_assets": 6371.6,
    "floor_plan": 2027.0,
    "debt": 3572.0,
    "revolver": 0.0,
    "other_liabilities": 2127.5,
    "equity": 3891.7,
}

# ---- Operating and financing assumptions, FY2026E through FY2030E ----
YEARS = [2026, 2027, 2028, 2029, 2030]
GROWTH = [0.018, 0.018, 0.018, 0.018, 0.018]
GROSS_MARGIN = [0.1705, 0.1705, 0.1705, 0.1705, 0.1705]
SGA_TO_GROSS_PROFIT = [0.665, 0.655, 0.645, 0.645, 0.645]
DEPRECIATION_TO_OPENING_PPE = 82.4 / 3070.4
IMPAIRMENT = [120.0, 120.0, 120.0, 120.0, 120.0]
CAPEX = [250.0, 250.0, 250.0, 250.0, 250.0]
TAX_RATE = [0.255, 0.255, 0.255, 0.255, 0.255]

INVENTORY_DAYS = 2135.8 / (17999.0 - 3071.7) * 365
FLOOR_PLAN_TO_INVENTORY = 2027.0 / 2135.8
OTHER_WORKING_CAPITAL_TO_REVENUE_CHANGE = 0.008
DEBT_REPAYMENT = [150.0, 150.0, 150.0, 150.0, 150.0]
BUYBACK = [150.0, 150.0, 150.0, 150.0, 150.0]
MINIMUM_CASH = 25.0
REVOLVER_LIMIT = 850.0
RATE_FLOOR_PLAN = 0.0467
RATE_DEBT = 0.0544
RATE_REVOLVER = 0.0600

# ---- Equity valuation assumptions ----
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 17.951349  # millions; 10-Q at June 30, 2026

TOLERANCE = 0.0001


def assert_balanced(year, gap, cash, minimum_cash):
    """Stop before valuation if a projected balance sheet or cash floor fails."""
    if abs(gap) > TOLERANCE:
        raise ValueError(f"FY{year}E: balance sheet gap is {gap:.4f} million")
    if cash < minimum_cash - TOLERANCE:
        raise ValueError(
            f"FY{year}E: cash is {cash:.4f} million, below the {minimum_cash:.4f} million minimum"
        )


def project_year(opening, index):
    """Project one year in the exact calculation order specified in the lab."""
    revenue = opening["revenue"] * (1 + GROWTH[index])
    gross_profit = revenue * GROSS_MARGIN[index]
    sga = gross_profit * SGA_TO_GROSS_PROFIT[index]
    depreciation = opening["ppe"] * DEPRECIATION_TO_OPENING_PPE
    impairment = IMPAIRMENT[index]
    operating_income = gross_profit - sga - depreciation - impairment
    interest = (
        opening["floor_plan"] * RATE_FLOOR_PLAN
        + opening["debt"] * RATE_DEBT
        + opening["revolver"] * RATE_REVOLVER
    )
    pretax_income = operating_income - interest
    tax = max(0.0, pretax_income) * TAX_RATE[index]
    net_income = pretax_income - tax

    inventory = (revenue - gross_profit) * INVENTORY_DAYS / 365
    floor_plan = inventory * FLOOR_PLAN_TO_INVENTORY
    ppe = opening["ppe"] + CAPEX[index] - depreciation
    revenue_change = revenue - opening["revenue"]
    other_working_capital_change = OTHER_WORKING_CAPITAL_TO_REVENUE_CHANGE * revenue_change
    other_assets = opening["other_assets"] + other_working_capital_change - impairment
    repayment = min(DEBT_REPAYMENT[index], opening["debt"])
    debt = opening["debt"] - repayment
    other_liabilities = opening["other_liabilities"]
    equity = opening["equity"] + net_income - BUYBACK[index]

    inventory_change = inventory - opening["inventory"]
    floor_plan_change = floor_plan - opening["floor_plan"]
    fcfe = (
        net_income
        + depreciation
        + impairment
        - CAPEX[index]
        - inventory_change
        - other_working_capital_change
        + floor_plan_change
        - repayment
    )

    # First calculate cash before revolver activity, then repay any existing
    # revolver before allowing excess cash above the minimum.
    cash = opening["cash"] + fcfe - BUYBACK[index]
    revolver = opening["revolver"]
    revolver_repayment = min(revolver, max(0.0, cash - MINIMUM_CASH))
    revolver -= revolver_repayment
    cash -= revolver_repayment
    if cash < MINIMUM_CASH:
        draw = MINIMUM_CASH - cash
        available = REVOLVER_LIMIT - revolver
        if draw > available + TOLERANCE:
            raise ValueError(
                f"{YEARS[index]}: revolver draw of {draw:.4f} exceeds available capacity {available:.4f}"
            )
        revolver += draw
        cash += draw
    else:
        draw = 0.0

    total_assets = cash + inventory + ppe + other_assets
    total_liabilities_equity = floor_plan + debt + revolver + other_liabilities + equity
    gap = total_assets - total_liabilities_equity
    assert_balanced(YEARS[index], gap, cash, MINIMUM_CASH)

    return {
        "year": YEARS[index], "revenue": revenue, "gross_profit": gross_profit,
        "sga": sga, "depreciation": depreciation, "impairment": impairment,
        "operating_income": operating_income, "interest": interest,
        "pretax_income": pretax_income, "tax": tax, "net_income": net_income,
        "cash": cash, "inventory": inventory, "ppe": ppe,
        "other_assets": other_assets, "total_assets": total_assets,
        "floor_plan": floor_plan, "debt": debt, "revolver": revolver,
        "other_liabilities": other_liabilities, "equity": equity,
        "total_liabilities_equity": total_liabilities_equity, "gap": gap,
        "inventory_change": inventory_change,
        "other_working_capital_change": other_working_capital_change,
        "floor_plan_change": floor_plan_change, "repayment": repayment,
        "capex": CAPEX[index], "buyback": BUYBACK[index], "revolver_draw": draw,
        "revolver_repayment": revolver_repayment, "fcfe": fcfe,
    }


def print_table(title, rows, projections):
    width = 16
    print(f"\n{title}")
    print("Line item".ljust(31) + "".join(str(y["year"]).rjust(width) for y in projections))
    print("-" * (31 + width * len(projections)))
    for label, key in rows:
        print(label.ljust(31) + "".join(f"{y[key]:>{width}.1f}" for y in projections))


def main():
    if TERMINAL_GROWTH >= COST_OF_EQUITY:
        raise ValueError("Terminal growth must be less than the cost of equity.")

    projections = []
    opening = OPENING.copy()
    for index in range(len(YEARS)):
        projected = project_year(opening, index)
        projections.append(projected)
        opening = projected

    print_table("Income Statement (USD millions)", [
        ("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"),
        ("Depreciation", "depreciation"), ("Impairment", "impairment"),
        ("Operating income", "operating_income"), ("Interest", "interest"),
        ("Pretax income", "pretax_income"), ("Tax", "tax"), ("Net income", "net_income"),
    ], projections)
    print_table("Balance Sheet (USD millions)", [
        ("Cash", "cash"), ("Inventory", "inventory"), ("PP&E", "ppe"),
        ("Other assets", "other_assets"), ("Total assets", "total_assets"),
        ("Floor plan", "floor_plan"), ("Debt", "debt"), ("Revolver", "revolver"),
        ("Other liabilities", "other_liabilities"), ("Equity", "equity"),
        ("Total liabilities and equity", "total_liabilities_equity"),
    ], projections)
    print_table("Cash Flow to Equity (USD millions)", [
        ("Net income", "net_income"), ("Depreciation", "depreciation"),
        ("Impairment", "impairment"), ("Capital spending", "capex"),
        ("Change in inventory", "inventory_change"),
        ("Change in other working capital", "other_working_capital_change"),
        ("Change in floor plan", "floor_plan_change"), ("Debt repayment", "repayment"),
        ("FCFE", "fcfe"),
    ], projections)

    print("\nChecks")
    print("Check".ljust(31) + "".join(str(y["year"]).rjust(16) for y in projections))
    print("-" * 111)
    print("Assets − liabilities − equity".ljust(31) + "".join(f"{y['gap']:16.1f}" for y in projections))
    print("Cash at or above minimum".ljust(31) + "".join(
        ("OK" if y["cash"] >= MINIMUM_CASH else "FAIL").rjust(16) for y in projections
    ))

    discount_factors = [1 / (1 + COST_OF_EQUITY) ** number for number in range(1, 6)]
    pv_explicit = sum(y["fcfe"] * factor for y, factor in zip(projections, discount_factors))
    terminal_cash_flow = (projections[-1]["fcfe"] + projections[-1]["repayment"]) * (1 + TERMINAL_GROWTH)
    terminal_value = terminal_cash_flow / (COST_OF_EQUITY - TERMINAL_GROWTH)
    pv_terminal = terminal_value * discount_factors[-1]
    equity_value = pv_explicit + pv_terminal
    share_after_2030 = pv_terminal / equity_value
    value_per_share = equity_value / SHARES_OUTSTANDING

    print("\nEquity Valuation")
    print(f"Equity value: ${equity_value:,.2f} million")
    print(f"Share of value after 2030: {share_after_2030:.2%}")
    print(f"Value per share: ${value_per_share:,.2f}")


if __name__ == "__main__":
    main()
