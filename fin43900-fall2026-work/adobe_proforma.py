"""Draft Adobe five-year pro forma and FCFE valuation.

USD millions except percentages and value per share. Source history and input
labels are in adobe_proforma_research.md. Inputs marked PLACEHOLDER need
company-specific sourcing before this becomes an investment conclusion.
"""

from copy import deepcopy


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

# The base set is never edited in a sensitivity run. Each run starts with a
# fresh deepcopy of this dictionary, then changes one listed driver only.
BASE_INPUTS = {
    "opening": OPENING,
    "growth": GROWTH,
    "gross_margin": GROSS_MARGIN,
    "sga_to_gross_profit": SGA_TO_GROSS_PROFIT,
    "depreciation_to_opening_ppe": DEPRECIATION_TO_OPENING_PPE,
    "impairment": IMPAIRMENT,
    "capex": CAPEX,
    "tax_rate": TAX_RATE,
    "inventory_days": INVENTORY_DAYS,
    "floor_plan_to_inventory": FLOOR_PLAN_TO_INVENTORY,
    "other_working_capital_to_revenue_change": OTHER_WORKING_CAPITAL_TO_REVENUE_CHANGE,
    "minimum_cash": MINIMUM_CASH,
    "revolver_limit": REVOLVER_LIMIT,
    "rate_floor_plan": RATE_FLOOR_PLAN,
    "rate_debt": RATE_DEBT,
    "rate_revolver": RATE_REVOLVER,
    "debt_repayment": DEBT_REPAYMENT,
    "buyback": BUYBACK,
    "cost_of_equity": COST_OF_EQUITY,
    "terminal_growth": TERMINAL_GROWTH,
    "shares_outstanding": SHARES_OUTSTANDING,
    "valuation_valid": False,
    "valuation_limitation": (
        "working-capital, financing, debt-repayment, and buyback inputs are placeholders"
    ),
}

# Existing ranges from adobe_proforma_research.md. Percentages are decimal
# inputs; the displayed values below identify percentage-point changes.
SENSITIVITY_DRIVERS = [
    {
        "name": "Revenue growth",
        "field": "growth",
        "units": "annual revenue growth (%)",
        "cases": {
            "Lower": [0.06, 0.05, 0.04, 0.03, 0.02],
            "Base": [0.08, 0.07, 0.06, 0.05, 0.04],
            "Higher": [0.10, 0.09, 0.08, 0.07, 0.06],
        },
    },
    {
        "name": "SG&A / gross profit",
        "field": "sga_to_gross_profit",
        "units": "percentage of gross profit",
        "cases": {
            "Lower": [0.375, 0.37, 0.37, 0.37, 0.37],
            "Base": [0.385, 0.38, 0.38, 0.38, 0.38],
            "Higher": [0.395, 0.39, 0.39, 0.39, 0.39],
        },
    },
]


def assert_balanced(year, gap, cash, minimum_cash):
    """Raise a specific error before valuation if a check fails."""
    if abs(gap) > TOLERANCE:
        raise ValueError(f"FY{year}E: balance sheet gap is {gap:.4f} million")
    if cash < minimum_cash - TOLERANCE:
        raise ValueError(
            f"FY{year}E: cash is {cash:.4f} million, below the {minimum_cash:.4f} million minimum"
        )


def project_year(opening, index, inputs):
    """Build one forecast year, then return it as the next opening balance sheet."""
    revenue = opening["revenue"] * (1 + inputs["growth"][index])
    gross_profit = revenue * inputs["gross_margin"][index]
    sga = gross_profit * inputs["sga_to_gross_profit"][index]
    depreciation = opening["ppe"] * inputs["depreciation_to_opening_ppe"]
    impairment = inputs["impairment"][index]
    operating_income = gross_profit - sga - depreciation - impairment
    interest = (
        opening["floor_plan"] * inputs["rate_floor_plan"]
        + opening["debt"] * inputs["rate_debt"]
        + opening["revolver"] * inputs["rate_revolver"]
    )
    pretax_income = operating_income - interest
    tax = max(0.0, pretax_income) * inputs["tax_rate"][index]
    net_income = pretax_income - tax

    inventory = (revenue - gross_profit) * inputs["inventory_days"] / 365.0
    floor_plan = inventory * inputs["floor_plan_to_inventory"]
    ppe = opening["ppe"] + inputs["capex"][index] - depreciation
    revenue_change = revenue - opening["revenue"]
    other_working_capital_change = inputs["other_working_capital_to_revenue_change"] * revenue_change
    other_assets = opening["other_assets"] + other_working_capital_change - impairment
    repayment = min(inputs["debt_repayment"][index], opening["debt"])
    debt = opening["debt"] - repayment
    equity = opening["equity"] + net_income - inputs["buyback"][index]

    inventory_change = inventory - opening["inventory"]
    floor_plan_change = floor_plan - opening["floor_plan"]
    fcfe = (
        net_income + depreciation + impairment - inputs["capex"][index]
        - inventory_change - other_working_capital_change
        + floor_plan_change - repayment
    )

    cash = opening["cash"] + fcfe - inputs["buyback"][index]
    revolver = opening["revolver"]
    revolver_repayment = min(revolver, max(0.0, cash - inputs["minimum_cash"]))
    cash -= revolver_repayment
    revolver -= revolver_repayment
    if cash < inputs["minimum_cash"]:
        draw = inputs["minimum_cash"] - cash
        available = inputs["revolver_limit"] - revolver
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
    assert_balanced(YEARS[index], gap, cash, inputs["minimum_cash"])

    return {
        "year": YEARS[index], "revenue": revenue, "gross_profit": gross_profit,
        "sga": sga, "depreciation": depreciation, "impairment": impairment,
        "operating_income": operating_income, "interest": interest,
        "pretax_income": pretax_income, "tax": tax, "net_income": net_income,
        "cash": cash, "inventory": inventory, "ppe": ppe, "other_assets": other_assets,
        "total_assets": total_assets, "floor_plan": floor_plan, "debt": debt,
        "revolver": revolver, "other_liabilities": opening["other_liabilities"],
        "equity": equity, "total_liabilities_equity": total_liabilities_equity,
        "gap": gap, "capex": inputs["capex"][index], "inventory_change": inventory_change,
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


def run_model(inputs):
    """Run a full linked model from an independent input copy."""
    if inputs["terminal_growth"] >= inputs["cost_of_equity"]:
        raise ValueError("Terminal growth must be less than the cost of equity.")
    projections = []
    opening = deepcopy(inputs["opening"])
    for index in range(len(YEARS)):
        year = project_year(opening, index, inputs)
        projections.append(year)
        opening = year
    return projections


def print_checks(projections, inputs):
    """Print the same visible accounting checks for a model run."""
    print("\nChecks")
    print("Check".ljust(31) + "".join(str(row["year"]).rjust(15) for row in projections))
    print("-" * 106)
    print("Assets − liabilities − equity".ljust(31) + "".join(f"{row['gap']:15.1f}" for row in projections))
    print("Cash at or above minimum".ljust(31) + "".join(
        ("OK" if row["cash"] >= inputs["minimum_cash"] else "FAIL").rjust(15)
        for row in projections
    ))


def format_input_path(values):
    """Show the actual percentage inputs used in FY2026E–FY2030E."""
    return ", ".join(f"{value:.1%}" for value in values)


def signed_change(value, base):
    return f"{value - base:+,.1f}"


def run_sensitivities():
    """Run lower/base/higher cases one driver at a time from fresh base copies."""
    print("\nOne-at-a-Time Sensitivity Analysis")
    print("Value per share is unavailable: " + BASE_INPUTS["valuation_limitation"] + ".")
    for driver in SENSITIVITY_DRIVERS:
        results = {}
        for case_name, path in driver["cases"].items():
            inputs = deepcopy(BASE_INPUTS)
            inputs[driver["field"]] = list(path)
            try:
                projections = run_model(inputs)
                results[case_name] = {"projections": projections, "error": None}
            except ValueError as error:
                results[case_name] = {"projections": None, "error": str(error)}

        print(f"\nDriver: {driver['name']} ({driver['units']}; FY2026E–FY2030E)")
        print("Case".ljust(10) + "Actual inputs".ljust(43) + "FY2030E op. profit".rjust(23)
              + "  change".rjust(12) + "FY2030E FCFE".rjust(18) + "  change".rjust(12) + "  checks")
        print("-" * 130)
        base_result = results["Base"]
        base_last = base_result["projections"][-1] if base_result["error"] is None else None
        for case_name in ("Lower", "Base", "Higher"):
            result = results[case_name]
            path = driver["cases"][case_name]
            if result["error"] is not None:
                print(f"{case_name:<10}{format_input_path(path):<43}INVALID: {result['error']}")
                continue
            last = result["projections"][-1]
            op_change = signed_change(last["operating_income"], base_last["operating_income"])
            fcfe_change = signed_change(last["fcfe"], base_last["fcfe"])
            print(f"{case_name:<10}{format_input_path(path):<43}{last['operating_income']:>23,.1f}"
                  f"{op_change:>12}{last['fcfe']:>18,.1f}{fcfe_change:>12}  OK")

        valid_last = [result["projections"][-1] for result in results.values() if result["error"] is None]
        if valid_last:
            op_span = max(row["operating_income"] for row in valid_last) - min(row["operating_income"] for row in valid_last)
            fcfe_span = max(row["fcfe"] for row in valid_last) - min(row["fcfe"] for row in valid_last)
            print(f"Output span (max − min): FY2030E operating profit ${op_span:,.1f}m; "
                  f"FY2030E FCFE ${fcfe_span:,.1f}m; value per share unavailable.")

    # The global/base independent inputs are not modified by any run.
    return run_model(deepcopy(BASE_INPUTS))


def main():
    projections = run_model(deepcopy(BASE_INPUTS))

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

    print_checks(projections, BASE_INPUTS)
    print("\nEquity Valuation")
    print("Value per share unavailable: " + BASE_INPUTS["valuation_limitation"] + ".")
    restored_base = run_sensitivities()
    print("\nBase reset check: rerun completed; FY2030E FCFE = "
          f"${restored_base[-1]['fcfe']:,.1f}m.")


if __name__ == "__main__":
    main()
