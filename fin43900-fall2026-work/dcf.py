"""
FIN 43900: Five-Year FCFF DCF Model, Sensitivity Grid, and Reverse DCF
Company: Adobe Inc. (NASDAQ: ADBE)
"""

# ==============================================================================
# INPUTS BLOCK (Editable by hand)
# ==============================================================================
# Mode: Set to 'ADBE' for Adobe Inc. or 'TRAINING' for Lab 05/06 training case
MODE = 'ADBE'

if MODE == 'TRAINING':
    # Lab 05 / 06 Official Training Case Inputs
    FCFF_0 = 100.0                       # Starting FCFF ($M)
    GROWTH_RATES = [0.08, 0.06, 0.05, 0.04, 0.03]  # Growth Years 1-5
    WACC = 0.10                          # Discount rate (10%)
    G_TERMINAL = 0.03                    # Terminal growth rate (3%)
    CASH = 50.0                          # Non-operating cash ($M)
    DEBT = 300.0                         # Debt ($M)
    SHARES = 50.0                        # Diluted shares (M)
    TARGET_PRICE = 30.00                 # Target share price for Reverse DCF ($)
    WACC_LIST = [0.09, 0.10, 0.11]       # Sensitivity grid WACC
    G_TERM_LIST = [0.02, 0.03, 0.04]     # Sensitivity grid terminal growth
    BOUND_LOW = -0.05                    # Reverse DCF lower bound shift (-5 ppt)
    BOUND_HIGH = 0.10                    # Reverse DCF upper bound shift (+10 ppt)
else:
    # Adobe Inc. (ADBE) Inputs — FY2025 Form 10-K & Market Data (Valuation Date: Sept 8, 2026)
    # Sourced from Form 10-K ended Nov 28, 2025:
    # Operating Cash Flow: $10,031M, Capex: $360M, Cash interest: $246M, Effective tax: 18.4%
    # Starting FCFF = OCF ($10,031M) + After-tax Interest ($200.7M) - Capex ($360M) = $9,871.7M
    FCFF_0 = 9871.7                      # Starting FCFF ($M)
    # Baseline forecast: Fading from recent Digital Media ARR growth (11.5% YoY) towards terminal
    GROWTH_RATES = [0.11, 0.095, 0.08, 0.065, 0.05]  # Stated 5-year fade
    WACC = 0.10                          # Estimated WACC (~9.7%-10.0%, baseline 10.0%)
    G_TERMINAL = 0.03                    # Long-run economic terminal growth (3.0%)
    CASH = 5431.0                        # Cash & cash equivalents ($M, Form 10-K p. 47)
    DEBT = 6210.0                        # Total long-term debt carrying value ($M, Form 10-K p. 47)
    SHARES = 427.0                       # Diluted weighted-average shares (M, Form 10-K p. 48)
    TARGET_PRICE = 257.60                # Current market share price ($ as of Sept 8, 2026)
    WACC_LIST = [0.09, 0.10, 0.11]       # Sensitivity grid WACC values
    G_TERM_LIST = [0.02, 0.03, 0.04]     # Sensitivity grid terminal growth values
    BOUND_LOW = -0.20                    # Reverse DCF lower bound shift (-20 ppt)
    BOUND_HIGH = 0.20                    # Reverse DCF upper bound shift (+20 ppt)


def compute_dcf(fcff_0, growths, wacc, g_term, cash, debt, shares):
    """Computes full 5-year FCFF DCF model."""
    if g_term >= wacc:
        return None

    fcff_list = []
    pv_explicit_list = []
    current_fcff = fcff_0

    for t, g in enumerate(growths, start=1):
        current_fcff = current_fcff * (1.0 + g)
        fcff_list.append(current_fcff)
        pv_fcff = current_fcff / ((1.0 + wacc) ** t)
        pv_explicit_list.append(pv_fcff)

    pv_explicit = sum(pv_explicit_list)
    fcff_5 = fcff_list[-1]
    tv_5 = fcff_5 * (1.0 + g_term) / (wacc - g_term)
    pv_tv = tv_5 / ((1.0 + wacc) ** 5)

    ev = pv_explicit + pv_tv
    eq_val = ev + cash - debt
    val_per_share = eq_val / shares
    tv_share_of_ev = pv_tv / ev

    return {
        'fcff_list': fcff_list,
        'pv_explicit': pv_explicit,
        'tv_5': tv_5,
        'pv_tv': pv_tv,
        'ev': ev,
        'eq_val': eq_val,
        'val_per_share': val_per_share,
        'tv_share_of_ev': tv_share_of_ev,
    }


def main():
    if G_TERMINAL >= WACC:
        print(f"Error: Terminal growth ({G_TERMINAL:.2%}) must be strictly less than WACC ({WACC:.2%}).")
        return

    base_res = compute_dcf(FCFF_0, GROWTH_RATES, WACC, G_TERMINAL, CASH, DEBT, SHARES)

    # --------------------------------------------------------------------------
    # BLOCK 1: TWELVE LABELLED LINES (BASE CASE)
    # --------------------------------------------------------------------------
    print("=" * 65)
    print(f"FCFF DCF MODEL OUTPUT ({MODE} BASE CASE)")
    print("=" * 65)
    for t, fcff in enumerate(base_res['fcff_list'], start=1):
        print(f"FCFF Year {t}: {fcff:,.4f}")
    print(f"Present value of the explicit FCFF: {base_res['pv_explicit']:,.4f}")
    print(f"Terminal value at Year 5: {base_res['tv_5']:,.4f}")
    print(f"Present value of the terminal value: {base_res['pv_tv']:,.4f}")
    print(f"Enterprise value: {base_res['ev']:,.4f}")
    print(f"Equity value: {base_res['eq_val']:,.4f}")
    print(f"Value per diluted share: {base_res['val_per_share']:,.4f}")
    print(f"Present value of the terminal value as a share of enterprise value: {base_res['tv_share_of_ev']:.4f}")

    # --------------------------------------------------------------------------
    # BLOCK 2: SENSITIVITY GRID (VALUE PER DILUTED SHARE)
    # --------------------------------------------------------------------------
    print("\n" + "=" * 65)
    print("SENSITIVITY GRID: Value per diluted share ($)")
    print("=" * 65)
    header = f"{'WACC \\ g':<12}" + "".join([f"{g_t:>14.1%}" for g_t in G_TERM_LIST])
    print(header)
    print("-" * len(header))

    for w in WACC_LIST:
        row_str = f"{w:<12.1%}"
        for gt in G_TERM_LIST:
            if gt >= w:
                row_str += f"{'Invalid':>14}"
            else:
                grid_res = compute_dcf(FCFF_0, GROWTH_RATES, w, gt, CASH, DEBT, SHARES)
                row_str += f"{grid_res['val_per_share']:>14.2f}"
        print(row_str)

    # --------------------------------------------------------------------------
    # BLOCK 3: REVERSE DCF (SOLVE UNIFORM GROWTH SHIFT FOR TARGET PRICE)
    # --------------------------------------------------------------------------
    print("\n" + "=" * 65)
    print(f"REVERSE DCF: Target Share Price = ${TARGET_PRICE:.2f}")
    print("=" * 65)

    # Validation: refuse bracket that pushes any growth to <= -100%
    for g in GROWTH_RATES:
        if (g + BOUND_LOW) <= -1.0:
            print(f"Error: Lower bound shift pushes growth to <= -100% ({g + BOUND_LOW:.2%}).")
            return

    # Check bounds
    res_low = compute_dcf(FCFF_0, [g + BOUND_LOW for g in GROWTH_RATES], WACC, G_TERMINAL, CASH, DEBT, SHARES)
    res_high = compute_dcf(FCFF_0, [g + BOUND_HIGH for g in GROWTH_RATES], WACC, G_TERMINAL, CASH, DEBT, SHARES)

    if not (res_low['val_per_share'] <= TARGET_PRICE <= res_high['val_per_share']):
        print(f"No solution inside bracket [{BOUND_LOW*100:+.2f} ppt, {BOUND_HIGH*100:+.2f} ppt].")
        print(f"Value at lower bound: ${res_low['val_per_share']:.2f}; Value at upper bound: ${res_high['val_per_share']:.2f}")
    else:
        # Bisection search
        low = BOUND_LOW
        high = BOUND_HIGH
        for _ in range(100):
            mid = (low + high) / 2.0
            shifted_g = [g + mid for g in GROWTH_RATES]
            r = compute_dcf(FCFF_0, shifted_g, WACC, G_TERMINAL, CASH, DEBT, SHARES)
            if r['val_per_share'] < TARGET_PRICE:
                low = mid
            else:
                high = mid

        solved_shift = mid
        solved_growths = [g + solved_shift for g in GROWTH_RATES]

        print(f"Solved uniform growth shift: {solved_shift * 100:+.2f} percentage points (shift = {solved_shift:+.4f})")
        print(f"Target share price: ${TARGET_PRICE:.2f}")
        print("Inputs held fixed:")
        print(f"  - Starting FCFF: ${FCFF_0:,.1f}M")
        print(f"  - WACC: {WACC:.2%}")
        print(f"  - Terminal growth: {G_TERMINAL:.2%}")
        print(f"  - Non-operating cash: ${CASH:,.1f}M")
        print(f"  - Debt: ${DEBT:,.1f}M")
        print(f"  - Diluted shares: {SHARES:.1f}M")
        print("\nImplied 5-year explicit growth path:")
        for t, (orig, sg) in enumerate(zip(GROWTH_RATES, solved_growths), start=1):
            print(f"  Year {t}: {orig:.1%} baseline -> {sg:.2%} implied")


if __name__ == '__main__':
    main()

