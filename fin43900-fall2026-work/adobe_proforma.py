"""Draft Adobe five-year pro forma and FCFE valuation.

USD millions except percentages and value per share. Source history and input
labels are in adobe_proforma_research.md. Inputs marked PLACEHOLDER need
company-specific sourcing before this becomes an investment conclusion.
"""


# Opening FY2025 balance sheet, from Adobe FY2025 10-K (USD millions).
# Other assets is the balancing aggregate of investments, receivables, prepaid
# assets, lease assets, goodwill, intangibles, deferred taxes, and other assets.
OPENING = {
    "revenue": 23769.0,
    "cash": 5431.0,
    "inventory": 0.0,       # none reported as a discrete balance
    "ppe": 1873.0,
    "other_assets": 22192.0,
    "floor_plan": 0.0,      # none: Adobe has no inventory-financing line
    "debt": 6210.0,
    "revolver": 0.0,
    "other_liabilities": 11663.0,
    "equity": 11623.0,
}

YEARS = [2026, 2027, 2028, 2029, 2030]

# Operating assumptions: history, judgment, and placeholders are labeled in
# adobe_proforma_research.md.
GROWTH = [0.08, 0.07, 0.06, 0.05, 0.04]                 # judgment
GROSS_MARGIN = [0.89, 0.89, 0.89, 0.89, 0.89]            # judgment
SGA_TO_GROSS_PROFIT = [0.385, 0.38, 0.38, 0.38, 0.38]    # judgment
DEPRECIATION_TO_OPENING_PPE = 236.0 / 1873.0             # FY2025 history
IMPAIRMENT = [0.0, 0.0, 0.0, 0.0, 0.0]                   # judgment
CAPEX = [200.0, 200.0, 200.0, 200.0, 200.0]              # judgment
TAX_RATE = [0.19, 0.19, 0.19, 0.19, 0.19]                # judgment

# Adobe-specific replacements for dealership inventory/floor-plan mechanics.
INVENTORY_DAYS = 0.0                                      # none
FLOOR_PLAN_TO_INVENTORY = 0.0                             # none
OTHER_WORKING_CAPITAL_TO_REVENUE_CHANGE = 0.0             # PLACEHOLDER
MINIMUM_CASH = 1000.0                                     # PLACEHOLDER
REVOLVER_LIMIT = 0.0                                      # PLACEHOLDER: no draw permitted
RATE_FLOOR_PLAN = 0.0                                     # none
RATE_DEBT = 263.0 / (1499.0 + 4129.0)                     # FY25 interest / FY24 debt
RATE_REVOLVER = 0.0                                       # PLACEHOLDER
DEBT_REPAYMENT = [0.0, 0.0, 0.0, 0.0, 0.0]               # PLACEHOLDER
BUYBACK = [0.0, 0.0, 0.0, 0.0, 0.0]                      # PLACEHOLDER

COST_OF_EQUITY = 0.1033                                  # Week 3 judgment
TERMINAL_GROWTH = 0.03                                   # Week 3 judgment
SHARES_OUTSTANDING = 427.0                               # FY2025 diluted shares, millions
TOLERANCE = 0.0001


def assert_balanced(year, gap, cash, minimum_cash):
    """Raise a specific error before valuation if a check fails."""
    if abs(gap) > TOLERANCE:
        raise ValueError(f"FY{year}E: balance sheet gap is {gap:.4f} million")
    if cash < minimum_cash - TOLERANCE:
        raise ValueError(
            f"FY{year}E: cash is {cash:.4f} million, below the {minimum_cash:.4f} million minimum"
        )


def project_year(opening, index):
    """Build one forecast year, then return it as the next opening balance sheet."""
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

    inventory = (revenue - gross_profit) * INVENTORY_DAYS / 365.0
    floor_plan = inventory * FLOOR_PLAN_TO_INVENTORY
    ppe = opening["ppe"] + CAPEX[index] - depreciation
    revenue_change = revenue - opening["revenue"]
    other_working_capital_change = OTHER_WORKING_CAPITAL_TO_REVENUE_CHANGE * revenue_change
    other_assets = opening["other_assets"] + other_working_capital_change - impairment
    repayment = min(DEBT_REPAYMENT[index], opening["debt"])
    debt = opening["debt"] - repayment
    equity = opening["equity"] + net_income - BUYBACK[index]

    inventory_change = inventory - opening["inventory"]
    floor_plan_change = floor_plan - opening["floor_plan"]
    fcfe = (
        net_income + depreciation + impairment - CAPEX[index]
        - inventory_change - other_working_capital_change
        + floor_plan_change - repayment
    )

    cash = opening["cash"] + fcfe - BUYBACK[index]
    revolver = opening["revolver"]
    revolver_repayment = min(revolver, max(0.0, cash - MINIMUM_CASH))
    cash -= revolver_repayment
    revolver -= revolver_repayment
    if cash < MINIMUM_CASH:
        draw = MINIMUM_CASH - cash
        available = REVOLVER_LIMIT - revolver
        if draw > available + TOLERANCE:
            raise ValueError(
                f"FY{YEARS[index]}E: revolver draw {draw:.4f} exceeds available capacity {available:.4f}"
            )
        cash += draw
        revolver += draw
    else:
        draw = 0.0

    total_assets = cash + inventory + ppe + other_assets
    total_liabilities_equity = floor_plan + debt + revolver + opening["other_liabilities"] + equity
    gap = total_assets - total_liabilities_equity
    assert_balanced(YEARS[index], gap, cash, MINIMUM_CASH)

    return {
        "year": YEARS[index], "revenue": revenue, "gross_profit": gross_profit,
        "sga": sga, "depreciation": depreciation, "impairment": impairment,
        "operating_income": operating_income, "interest": interest,
        "pretax_income": pretax_income, "tax": tax, "net_income": net_income,
        "cash": cash, "inventory": inventory, "ppe": ppe, "other_assets": other_assets,
        "total_assets": total_assets, "floor_plan": floor_plan, "debt": debt,
        "revolver": revolver, "other_liabilities": opening["other_liabilities"],
        "equity": equity, "total_liabilities_equity": total_liabilities_equity,
        "gap": gap, "capex": CAPEX[index], "inventory_change": inventory_change,
        "other_working_capital_change": other_working_capital_change,
        "floor_plan_change": floor_plan_change, "repayment": repayment,
        "fcfe": fcfe, "revolver_draw": draw,
    }


def print_table(title, rows, years):
    width = 15
    print(f"\n{title}")
    print("Line item".ljust(31) + "".join(str(row["year"]).rjust(width) for row in years))
    print("-" * (31 + width * len(years)))
    for label, key in rows:
        print(label.ljust(31) + "".join(f"{row[key]:>{width}.1f}" for row in years))


def main():
    if TERMINAL_GROWTH >= COST_OF_EQUITY:
        raise ValueError("Terminal growth must be less than the cost of equity.")

    projections = []
    opening = OPENING.copy()
    for index in range(len(YEARS)):
        year = project_year(opening, index)
        projections.append(year)
        opening = year

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
    print("Check".ljust(31) + "".join(str(row["year"]).rjust(15) for row in projections))
    print("-" * 106)
    print("Assets − liabilities − equity".ljust(31) + "".join(f"{row['gap']:15.1f}" for row in projections))
    print("Cash at or above minimum".ljust(31) + "".join(
        ("OK" if row["cash"] >= MINIMUM_CASH else "FAIL").rjust(15) for row in projections
    ))

    factors = [1 / (1 + COST_OF_EQUITY) ** period for period in range(1, 6)]
    pv_explicit = sum(row["fcfe"] * factor for row, factor in zip(projections, factors))
    terminal_cash_flow = (projections[-1]["fcfe"] + projections[-1]["repayment"]) * (1 + TERMINAL_GROWTH)
    pv_terminal = terminal_cash_flow / (COST_OF_EQUITY - TERMINAL_GROWTH) * factors[-1]
    equity_value = pv_explicit + pv_terminal

    print("\nEquity Valuation")
    print(f"Equity value: ${equity_value:,.2f} million")
    print(f"Share of value after 2030: {pv_terminal / equity_value:.2%}")
    print(f"Value per share: ${equity_value / SHARES_OUTSTANDING:,.2f}")


if __name__ == "__main__":
    main()
