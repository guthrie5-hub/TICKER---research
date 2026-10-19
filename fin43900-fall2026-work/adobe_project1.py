"""Adobe Project 1: linked five-year pro-forma and FCFF valuation.

All figures are USD millions unless stated otherwise.  Valuation date:
September 24, 2026.  Source locators and assumption labels are in
adobe_project1_sources.md.  This file uses only the Python standard library.
"""

from copy import deepcopy


# ---------------------------------------------------------------------------
# EDITABLE INPUTS
# ---------------------------------------------------------------------------
VALUATION_DATE = "2026-09-24"
MARKET_PRICE = 238.93  # ADBE NASDAQ close on valuation date, USD/share
YEARS = [2026, 2027, 2028, 2029, 2030]

# Opening balance sheet: Adobe FY2025 10-K, November 28, 2025.  The forecast
# therefore runs FY2026E–FY2030E from an audited fiscal-year base.  The cash,
# debt, and share bridge below is separately updated to the valuation date.
OPENING = {
    "cash": 5431.0,
    "short_term_investments": 1164.0,
    "receivables": 2344.0,
    "prepaids": 1224.0,
    "ppe": 1873.0,
    "other_assets": 17460.0,
    "payables": 417.0,
    "accruals": 2648.0,
    "deferred_revenue": 7030.0,  # current plus long-term
    "taxes_payable": 622.0,      # current plus long-term
    "other_liabilities": 946.0, # lease liabilities plus other liabilities
    "debt": 6210.0,
    "equity": 11623.0,
}

# FY2026 revenue is the midpoint of Adobe's September 10, 2026 guidance.
# FY2027–FY2030 are judgmental fade assumptions, not company guidance.
REVENUE = [26601.0, 29261.1, 31602.0, 33498.1, 34838.0]
GROSS_MARGIN = [0.892, 0.892, 0.892, 0.892, 0.892]
OPERATING_MARGIN = [0.350, 0.355, 0.360, 0.3625, 0.365]
TAX_RATE = [0.225, 0.220, 0.220, 0.220, 0.220]
DNA_TO_REVENUE = [0.030, 0.030, 0.030, 0.030, 0.030]
# FY2025 PP&E-only depreciation was $236m; the remainder of D&A is primarily
# amortization of acquired intangibles and reduces other assets instead of PP&E.
PPE_DEPRECIATION_TO_REVENUE = [0.010, 0.010, 0.010, 0.010, 0.010]
CAPEX_TO_REVENUE = [0.013, 0.013, 0.013, 0.013, 0.013]

# Operating working-capital drivers use the FY2025 opening-balance ratios.
# Negative NWC is expected for a subscription business with deferred revenue.
RECEIVABLES_TO_REVENUE = OPENING["receivables"] / REVENUE[0]
PREPAIDS_TO_REVENUE = OPENING["prepaids"] / REVENUE[0]
PAYABLES_TO_REVENUE = OPENING["payables"] / REVENUE[0]
ACCRUALS_TO_REVENUE = OPENING["accruals"] / REVENUE[0]
DEFERRED_REVENUE_TO_REVENUE = OPENING["deferred_revenue"] / REVENUE[0]
TAXES_PAYABLE_TO_REVENUE = OPENING["taxes_payable"] / REVENUE[0]

# Finance assumptions.  Scheduled repayments reflect reported note maturities;
# projected repurchases are an explicit judgment, not guidance.
DEBT_REPAYMENT = [0.0, 1350.0, 800.0, 750.0, 2000.0]
INTEREST_RATE = 0.050
BUYBACK = [6000.0, 6000.0, 6000.0, 6000.0, 6000.0]
MINIMUM_CASH = 1000.0

# Enterprise-value valuation inputs.
WACC = 0.100
TERMINAL_GROWTH = 0.025
# Adobe Q3 FY2026 10-Q: August 28, 2026 cash plus short-term investments and
# debt.  These point-in-time balances, and Sep. 18 point-in-time shares, form
# the Sep. 24 enterprise-to-equity bridge.
NON_OPERATING_CASH = 5639.0
BRIDGE_DEBT = 6363.0
SHARES_OUTSTANDING = 389.2  # point-in-time shares outstanding, millions
WACC_LIST = [0.09, 0.10, 0.11]
TERMINAL_GROWTH_LIST = [0.02, 0.025, 0.03]
REVERSE_SHIFT_LOW = -0.10
REVERSE_SHIFT_HIGH = 0.10
TOLERANCE = 0.01


def operating_nwc(row):
    """Operating assets less operating liabilities; excludes cash, debt, and equity."""
    return (
        row["receivables"]
        + row["prepaids"]
        - row["payables"]
        - row["accruals"]
        - row["deferred_revenue"]
        - row["taxes_payable"]
    )


def totals(row):
    assets = (
        row["cash"] + row["short_term_investments"] + row["receivables"]
        + row["prepaids"] + row["ppe"] + row["other_assets"]
    )
    liabilities = (
        row["payables"] + row["accruals"] + row["deferred_revenue"]
        + row["taxes_payable"] + row["other_liabilities"] + row["debt"]
    )
    return assets, liabilities + row["equity"]


def assert_balanced(year, row, cash_flow_cash):
    """Refuse valuation if a statement does not articulate."""
    assets, liabilities_and_equity = totals(row)
    gap = assets - liabilities_and_equity
    if abs(gap) > TOLERANCE:
        raise ValueError(f"FY{year}: balance-sheet gap is {gap:.2f} million")
    if abs(row["cash"] - cash_flow_cash) > TOLERANCE:
        raise ValueError(
            f"FY{year}: cash-flow cash does not tie to balance-sheet cash "
            f"({row['cash'] - cash_flow_cash:.2f} million)"
        )
    if row["cash"] < MINIMUM_CASH - TOLERANCE:
        raise ValueError(f"FY{year}: cash is below the ${MINIMUM_CASH:.1f}m floor")


def project(inputs):
    """Run linked income statement, balance sheet, cash flow, and FCFF forecast."""
    opening = deepcopy(inputs["opening"])
    opening["revenue"] = inputs["prior_revenue"]
    opening_assets, opening_le = totals(opening)
    if abs(opening_assets - opening_le) > TOLERANCE:
        raise ValueError("Opening FY2025 balance sheet does not reconcile.")

    projections = []
    for i, year in enumerate(YEARS):
        revenue = inputs["revenue"][i]
        gross_profit = revenue * inputs["gross_margin"][i]
        ebit = revenue * inputs["operating_margin"][i]
        dna = revenue * inputs["dna_to_revenue"][i]
        ppe_depreciation = revenue * inputs["ppe_depreciation_to_revenue"][i]
        intangible_amortization = dna - ppe_depreciation
        cash_opex = gross_profit - ebit - dna
        capex = revenue * inputs["capex_to_revenue"][i]
        interest = opening["debt"] * inputs["interest_rate"]
        pretax_income = ebit - interest
        tax = max(0.0, pretax_income) * inputs["tax_rate"][i]
        net_income = pretax_income - tax

        row = {
            "year": year,
            "revenue": revenue,
            "gross_profit": gross_profit,
            "cash_opex": cash_opex,
            "dna": dna,
            "ebit": ebit,
            "interest": interest,
            "pretax_income": pretax_income,
            "tax": tax,
            "net_income": net_income,
            "short_term_investments": opening["short_term_investments"],
            "other_assets": opening["other_assets"] - intangible_amortization,
            "other_liabilities": opening["other_liabilities"],
        }

        row["receivables"] = revenue * inputs["receivables_to_revenue"]
        row["prepaids"] = revenue * inputs["prepaids_to_revenue"]
        row["payables"] = revenue * inputs["payables_to_revenue"]
        row["accruals"] = revenue * inputs["accruals_to_revenue"]
        row["deferred_revenue"] = revenue * inputs["deferred_revenue_to_revenue"]
        row["taxes_payable"] = revenue * inputs["taxes_payable_to_revenue"]
        row["ppe"] = opening["ppe"] + capex - ppe_depreciation
        row["nwc"] = operating_nwc(row)
        nwc_change = row["nwc"] - operating_nwc(opening)
        repayment = min(inputs["debt_repayment"][i], opening["debt"])
        row["debt"] = opening["debt"] - repayment
        buyback = inputs["buyback"][i]
        row["equity"] = opening["equity"] + net_income - buyback

        # FCFF is before interest and financing; cash flow is after both.
        fcff = ebit * (1.0 - inputs["tax_rate"][i]) + dna - capex - nwc_change
        cash_flow_cash = (
            opening["cash"] + net_income + dna - capex - nwc_change
            - repayment - buyback
        )
        row["cash"] = cash_flow_cash
        row["capex"] = capex
        row["ppe_depreciation"] = ppe_depreciation
        row["intangible_amortization"] = intangible_amortization
        row["nwc_change"] = nwc_change
        row["repayment"] = repayment
        row["buyback"] = buyback
        row["fcff"] = fcff
        row["cash_flow_cash"] = cash_flow_cash
        assert_balanced(year, row, cash_flow_cash)
        projections.append(row)
        opening = row
    return projections


def value_from_fcff(fcff, wacc, terminal_growth, cash, debt, shares):
    if terminal_growth >= wacc:
        raise ValueError("Terminal growth must be strictly less than WACC.")
    pvs = [cash_flow / (1.0 + wacc) ** year for year, cash_flow in enumerate(fcff, 1)]
    terminal_value = fcff[-1] * (1.0 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1.0 + wacc) ** len(fcff)
    enterprise_value = sum(pvs) + pv_terminal
    equity_value = enterprise_value + cash - debt
    if shares <= 0:
        raise ValueError("Shares outstanding must be positive.")
    return {
        "pv_explicit": sum(pvs),
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "per_share": equity_value / shares,
        "tv_share": pv_terminal / enterprise_value,
    }


def project_and_value(inputs):
    projections = project(inputs)
    valuation = value_from_fcff(
        [row["fcff"] for row in projections], inputs["wacc"],
        inputs["terminal_growth"], inputs["non_operating_cash"],
        inputs["bridge_debt"], inputs["shares"],
    )
    return projections, valuation


BASE_INPUTS = {
    "opening": OPENING,
    "prior_revenue": 23769.0,
    "revenue": REVENUE,
    "gross_margin": GROSS_MARGIN,
    "operating_margin": OPERATING_MARGIN,
    "tax_rate": TAX_RATE,
    "dna_to_revenue": DNA_TO_REVENUE,
    "ppe_depreciation_to_revenue": PPE_DEPRECIATION_TO_REVENUE,
    "capex_to_revenue": CAPEX_TO_REVENUE,
    "receivables_to_revenue": RECEIVABLES_TO_REVENUE,
    "prepaids_to_revenue": PREPAIDS_TO_REVENUE,
    "payables_to_revenue": PAYABLES_TO_REVENUE,
    "accruals_to_revenue": ACCRUALS_TO_REVENUE,
    "deferred_revenue_to_revenue": DEFERRED_REVENUE_TO_REVENUE,
    "taxes_payable_to_revenue": TAXES_PAYABLE_TO_REVENUE,
    "debt_repayment": DEBT_REPAYMENT,
    "interest_rate": INTEREST_RATE,
    "buyback": BUYBACK,
    "wacc": WACC,
    "terminal_growth": TERMINAL_GROWTH,
    "non_operating_cash": NON_OPERATING_CASH,
    "bridge_debt": BRIDGE_DEBT,
    "shares": SHARES_OUTSTANDING,
}


def print_table(title, rows, projections):
    width = 14
    print(f"\n{title}")
    print("Line item".ljust(33) + "".join(str(row["year"]).rjust(width) for row in projections))
    print("-" * (33 + width * len(projections)))
    for label, key in rows:
        print(label.ljust(33) + "".join(f"{row[key]:>{width},.1f}" for row in projections))


def print_checks(projections):
    print("\nArticulation checks")
    print("Check".ljust(33) + "".join(str(row["year"]).rjust(14) for row in projections))
    print("-" * 103)
    gaps = []
    for row in projections:
        assets, le = totals(row)
        gaps.append(assets - le)
    print("Assets − liabilities − equity".ljust(33) + "".join(f"{gap:>14,.1f}" for gap in gaps))
    print("Cash-flow cash ties to balance cash".ljust(33) + "".join(
        ("OK" if abs(row["cash"] - row["cash_flow_cash"]) <= TOLERANCE else "FAIL").rjust(14)
        for row in projections
    ))
    print("Cash at or above floor".ljust(33) + "".join(
        ("OK" if row["cash"] >= MINIMUM_CASH else "FAIL").rjust(14)
        for row in projections
    ))


def print_valuation(valuation):
    print("\nFCFF enterprise-value valuation")
    print(f"PV explicit FCFF:                 ${valuation['pv_explicit']:,.1f}m")
    print(f"Terminal value at FY2030E:        ${valuation['terminal_value']:,.1f}m")
    print(f"PV terminal value:                ${valuation['pv_terminal']:,.1f}m")
    print(f"Enterprise value:                 ${valuation['enterprise_value']:,.1f}m")
    print(f"Non-operating cash + investments: ${NON_OPERATING_CASH:,.1f}m")
    print(f"Debt:                            -${BRIDGE_DEBT:,.1f}m")
    print(f"Equity value:                     ${valuation['equity_value']:,.1f}m")
    print(f"Value per share:                  ${valuation['per_share']:,.2f}")
    print(f"PV terminal value / EV:           {valuation['tv_share']:.1%}")


def print_sensitivity(base_inputs):
    print("\nWACC / terminal-growth sensitivity: value per share")
    header = "WACC \\ g".ljust(12) + "".join(f"{rate:>14.1%}" for rate in TERMINAL_GROWTH_LIST)
    print(header)
    print("-" * len(header))
    for wacc in WACC_LIST:
        line = f"{wacc:.1%}".ljust(12)
        for growth in TERMINAL_GROWTH_LIST:
            if growth >= wacc:
                line += f"{'invalid':>14}"
                continue
            inputs = deepcopy(base_inputs)
            inputs["wacc"] = wacc
            inputs["terminal_growth"] = growth
            _, valuation = project_and_value(inputs)
            line += f"{valuation['per_share']:>14.2f}"
        print(line)


def assert_dcf_monotonicity(base_inputs):
    """Check the expected directions before relying on the sensitivity table."""
    terminal_values = []
    for growth in TERMINAL_GROWTH_LIST:
        inputs = deepcopy(base_inputs)
        inputs["terminal_growth"] = growth
        terminal_values.append(project_and_value(inputs)[1]["per_share"])
    if terminal_values != sorted(terminal_values):
        raise AssertionError("DCF check failed: value should rise as terminal growth rises.")

    wacc_values = []
    for wacc in WACC_LIST:
        inputs = deepcopy(base_inputs)
        inputs["wacc"] = wacc
        wacc_values.append(project_and_value(inputs)[1]["per_share"])
    if wacc_values != sorted(wacc_values, reverse=True):
        raise AssertionError("DCF check failed: value should fall as WACC rises.")


def print_cases(base_inputs):
    print("\nCausal cases: low / base / high")
    cases = {
        "Low (AI/competition downside)": {
            "revenue": [26601.0, 28197.1, 29325.0, 30204.8, 30808.9],
            "operating_margin": [0.345, 0.345, 0.3475, 0.350, 0.350],
        },
        "Base": {"revenue": REVENUE, "operating_margin": OPERATING_MARGIN},
        "High": {
            "revenue": [26601.0, 29793.1, 32772.4, 35394.2, 37517.8],
            "operating_margin": [0.350, 0.360, 0.365, 0.370, 0.370],
        },
    }
    print("Case".ljust(32) + "FY2030E EBIT".rjust(16) + "FY2030E FCFF".rjust(18) + "Value/share".rjust(16))
    print("-" * 82)
    for name, updates in cases.items():
        inputs = deepcopy(base_inputs)
        inputs.update(updates)
        projections, valuation = project_and_value(inputs)
        last = projections[-1]
        print(f"{name:<32}{last['ebit']:>16,.1f}{last['fcff']:>18,.1f}${valuation['per_share']:>15,.2f}")


def reverse_dcf(base_inputs):
    """Solve a uniform FY2027–FY2030 revenue-growth shift for market price."""
    base_revenue = base_inputs["revenue"]
    base_growth = [base_revenue[i] / base_revenue[i - 1] - 1.0 for i in range(1, len(base_revenue))]

    def value_at_shift(shift):
        if any(growth + shift <= -1.0 for growth in base_growth):
            raise ValueError("Reverse-DCF bracket implies revenue growth of -100% or below.")
        inputs = deepcopy(base_inputs)
        revenue = [base_revenue[0]]
        for growth in base_growth:
            revenue.append(revenue[-1] * (1.0 + growth + shift))
        inputs["revenue"] = revenue
        return project_and_value(inputs)[1]["per_share"]

    low_value = value_at_shift(REVERSE_SHIFT_LOW)
    high_value = value_at_shift(REVERSE_SHIFT_HIGH)
    print("\nReverse DCF: market-implied revenue-growth shift")
    if not low_value <= MARKET_PRICE <= high_value:
        print(f"No solution in [{REVERSE_SHIFT_LOW:+.1%}, {REVERSE_SHIFT_HIGH:+.1%}].")
        print(f"Value at lower bound: ${low_value:.2f}; upper bound: ${high_value:.2f}")
        return
    low, high = REVERSE_SHIFT_LOW, REVERSE_SHIFT_HIGH
    for _ in range(100):
        middle = (low + high) / 2.0
        if value_at_shift(middle) < MARKET_PRICE:
            low = middle
        else:
            high = middle
    solved = (low + high) / 2.0
    print(f"Target market price:                ${MARKET_PRICE:.2f}")
    print(f"Solved FY2027–FY2030 growth shift: {solved:+.2%}")
    print("Held fixed: FY2026 guidance revenue, gross margin, operating-margin path,")
    print("tax, D&A, capex, working-capital ratios, debt schedule, buybacks, WACC,")
    print("terminal growth, cash/debt bridge, and point-in-time share count.")


def main():
    projections, valuation = project_and_value(deepcopy(BASE_INPUTS))
    opening_assets, opening_le = totals(OPENING)
    print(f"Adobe Project 1 FCFF model — valuation date {VALUATION_DATE}")
    print(f"FY2025 opening balance reconciliation: ${opening_assets:,.1f}m = ${opening_le:,.1f}m")
    print_table("Income statement (USD millions)", [
        ("Revenue", "revenue"), ("Gross profit", "gross_profit"),
        ("Cash operating expenses", "cash_opex"), ("D&A", "dna"),
        ("EBIT", "ebit"), ("Interest", "interest"),
        ("Pretax income", "pretax_income"), ("Tax", "tax"), ("Net income", "net_income"),
    ], projections)
    print_table("Balance sheet (USD millions)", [
        ("Cash", "cash"), ("Short-term investments", "short_term_investments"),
        ("Receivables", "receivables"), ("Prepaids", "prepaids"), ("PP&E", "ppe"),
        ("Other assets", "other_assets"), ("Payables", "payables"), ("Accruals", "accruals"),
        ("Deferred revenue", "deferred_revenue"), ("Taxes payable", "taxes_payable"),
        ("Other liabilities", "other_liabilities"), ("Debt", "debt"), ("Equity", "equity"),
    ], projections)
    print_table("Cash flow and FCFF (USD millions)", [
        ("Net income", "net_income"), ("D&A", "dna"), ("Capital spending", "capex"),
        ("Change in operating NWC", "nwc_change"), ("Debt repayment", "repayment"),
        ("Share repurchases", "buyback"), ("FCFF", "fcff"),
    ], projections)
    print_checks(projections)
    print_valuation(valuation)
    assert_dcf_monotonicity(BASE_INPUTS)
    print("DCF monotonicity checks: PASS (value rises with terminal growth and falls with WACC)")
    print_sensitivity(BASE_INPUTS)
    print_cases(BASE_INPUTS)
    reverse_dcf(BASE_INPUTS)


if __name__ == "__main__":
    main()
