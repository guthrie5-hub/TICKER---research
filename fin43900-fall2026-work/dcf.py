"""Five-year FCFF DCF (all currency inputs are USD millions)."""

# Editable inputs (USD millions, except per-share amounts)
STARTING_FCFF = 10067.66  # FY2025 estimate; see Table.md
GROWTH_RATES = [0.10, 0.09, 0.08, 0.07, 0.06]  # Analyst forecast
WACC = 0.1033  # Calculated estimate
TERMINAL_GROWTH = 0.03  # Valuation assumption
NON_OPERATING_CASH = 5626.0  # As of 2026-05-29
DEBT = 6645.0  # As of 2026-05-29
DILUTED_SHARES = 427.0  # FY2025 weighted-average diluted shares

# Editable sensitivity and reverse-DCF inputs
SENSITIVITY_WACCS = [0.09, 0.10, 0.11]
SENSITIVITY_TERMINAL_GROWTHS = [0.02, 0.03, 0.04]
TARGET_SHARE_PRICE = 250.35
REVERSE_SHIFT_LOWER_BOUND = -0.05
REVERSE_SHIFT_UPPER_BOUND = 0.10


def calculate_value_per_share(wacc, terminal_growth, growth_rates):
    """Return the DCF value per diluted share for a complete input set."""
    fcff = STARTING_FCFF
    pv_explicit_fcff = 0.0
    for year, growth_rate in enumerate(growth_rates, start=1):
        fcff *= 1.0 + growth_rate
        pv_explicit_fcff += fcff / (1.0 + wacc) ** year

    terminal_value = fcff * (1.0 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal_value = terminal_value / (1.0 + wacc) ** 5
    equity_value = pv_explicit_fcff + pv_terminal_value + NON_OPERATING_CASH - DEBT
    return equity_value / DILUTED_SHARES


def print_sensitivity_grid():
    """Print value per share for each terminal-growth/WACC combination."""
    print("\nSensitivity Grid: Value per Diluted Share")
    column_width = 16
    header = "Terminal Growth \\ WACC".ljust(column_width)
    header += "".join(f"{wacc:.2%}".rjust(column_width) for wacc in SENSITIVITY_WACCS)
    print(header)
    print("-" * len(header))

    for terminal_growth in SENSITIVITY_TERMINAL_GROWTHS:
        row = f"{terminal_growth:.2%}".ljust(column_width)
        for wacc in SENSITIVITY_WACCS:
            if terminal_growth >= wacc:
                cell = "invalid"
            else:
                cell = f"{calculate_value_per_share(wacc, terminal_growth, GROWTH_RATES):.4f}"
            row += cell.rjust(column_width)
        print(row)


def print_reverse_dcf():
    """Solve for a uniform shift to all explicit growth rates by bisection."""
    print("\nReverse DCF: Uniform Shift to All Five Explicit Growth Rates")
    held_fixed = (
        f"starting FCFF={STARTING_FCFF:.4f}; WACC={WACC:.2%}; "
        f"terminal growth={TERMINAL_GROWTH:.2%}; cash={NON_OPERATING_CASH:.4f}; "
        f"debt={DEBT:.4f}; diluted shares={DILUTED_SHARES:.4f}; "
        f"base growth rates={GROWTH_RATES}"
    )
    print(f"Target share price: {TARGET_SHARE_PRICE:.4f}")
    print(f"Inputs held fixed: {held_fixed}")

    lower = REVERSE_SHIFT_LOWER_BOUND
    upper = REVERSE_SHIFT_UPPER_BOUND
    if lower > upper:
        print("No solution: lower bound is greater than upper bound.")
        return
    if any(growth_rate + bound <= -1.0 for growth_rate in GROWTH_RATES for bound in (lower, upper)):
        print("No solution: this bracket pushes at least one annual growth rate to -100% or below.")
        return

    def value_at_shift(shift):
        shifted_growth_rates = [growth_rate + shift for growth_rate in GROWTH_RATES]
        return calculate_value_per_share(WACC, TERMINAL_GROWTH, shifted_growth_rates)

    lower_value = value_at_shift(lower)
    upper_value = value_at_shift(upper)
    minimum_value = min(lower_value, upper_value)
    maximum_value = max(lower_value, upper_value)
    if not minimum_value <= TARGET_SHARE_PRICE <= maximum_value:
        print(
            "No solution in this bracket: target is outside the range "
            f"{minimum_value:.4f} to {maximum_value:.4f}."
        )
        return

    for _ in range(100):
        midpoint = (lower + upper) / 2.0
        midpoint_value = value_at_shift(midpoint)
        if abs(midpoint_value - TARGET_SHARE_PRICE) < 0.00000001:
            print(f"Solved uniform growth-rate shift: {midpoint:.8%}")
            return
        if midpoint_value < TARGET_SHARE_PRICE:
            lower = midpoint
        else:
            upper = midpoint

    midpoint = (lower + upper) / 2.0
    midpoint_value = value_at_shift(midpoint)
    if abs(midpoint_value - TARGET_SHARE_PRICE) < 0.0001:
        print(f"Solved uniform growth-rate shift: {midpoint:.8%}")
    else:
        print("No solution in this bracket: bisection did not meet the solution tolerance.")


def main():
    if TERMINAL_GROWTH >= WACC:
        raise SystemExit(
            "Error: terminal growth must be less than WACC for the Gordon-growth formula."
        )

    if len(GROWTH_RATES) != 5:
        raise SystemExit("Error: provide exactly five yearly growth rates.")

    fcff = STARTING_FCFF
    explicit_fcff = []
    for growth_rate in GROWTH_RATES:
        fcff *= 1.0 + growth_rate
        explicit_fcff.append(fcff)

    pv_explicit_fcff = sum(
        cash_flow / (1.0 + WACC) ** year
        for year, cash_flow in enumerate(explicit_fcff, start=1)
    )
    terminal_value_year_5 = (
        explicit_fcff[-1] * (1.0 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    )
    pv_terminal_value = terminal_value_year_5 / (1.0 + WACC) ** 5
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    value_per_diluted_share = equity_value / DILUTED_SHARES
    terminal_value_share_of_ev = pv_terminal_value / enterprise_value

    for year, cash_flow in enumerate(explicit_fcff, start=1):
        print(f"FCFF Year {year}: {cash_flow:.4f}")
    print(f"PV of Explicit FCFF: {pv_explicit_fcff:.4f}")
    print(f"Terminal Value at Year 5: {terminal_value_year_5:.4f}")
    print(f"PV of Terminal Value: {pv_terminal_value:.4f}")
    print(f"Enterprise Value: {enterprise_value:.4f}")
    print(f"Equity Value: {equity_value:.4f}")
    print(f"Value per Diluted Share: {value_per_diluted_share:.4f}")
    print(f"PV Terminal Value as Share of EV: {terminal_value_share_of_ev:.4f}")
    print_sensitivity_grid()
    print_reverse_dcf()


if __name__ == "__main__":
    main()
