# Visible executed output — Adobe Project 1 system

**Run date:** 2026-10-18  
**Valuation date:** 2026-09-24  
**Currency / scale:** USD millions except per-share amounts.

Commands completed successfully:

```sh
./.uv/bin/python3.13 adobe_project1.py
./.uv/bin/python3.13 adobe_ev_comps.py
```

## Linked pro-forma and FCFF DCF

The FY2025 opening balance-sheet reconciliation printed **$29,496.0m = $29,496.0m**. Every forecast year FY2026E–FY2030E printed a **0.0** assets-minus-liabilities-minus-equity gap, an `OK` cash-flow-to-balance-sheet cash tie, and `OK` cash above the $1,000m floor.

| Output | FY2026E | FY2030E |
|---|---:|---:|
| Revenue | $26,601.0m | $34,838.0m |
| EBIT | $9,310.3m | $12,715.9m |
| FCFF | $7,667.7m | $10,870.7m |
| Cash | $6,858.1m | $18,015.2m |

| FCFF valuation output | Result |
|---|---:|
| PV of explicit FCFF | $36,168.2m |
| PV of terminal value | $92,248.1m |
| Enterprise value | $128,416.4m |
| Equity value | $127,692.4m |
| Value per 389.2m point-in-time shares | **$328.09** |
| PV terminal value / enterprise value | **71.8%** |

The DCF monotonicity check printed `PASS`: value rises as terminal growth rises and falls as WACC rises.

| WACC / terminal growth | 2.0% | 2.5% | 3.0% |
|---|---:|---:|---:|
| 9.0% | $358.15 | $379.90 | $405.27 |
| 10.0% | $312.19 | $328.09 | $346.26 |
| 11.0% | $276.47 | $288.49 | $302.02 |

| Causal case | FY2030E EBIT | FY2030E FCFF | Value per share |
|---|---:|---:|---:|
| Low — AI/competition downside | $10,783.1m | $9,096.9m | $279.39 |
| Base | $12,715.9m | $10,870.7m | $328.09 |
| High | $13,881.6m | $12,036.2m | $359.20 |

The reverse DCF solved a **−7.72 percentage-point** uniform shift to FY2027–FY2030 revenue growth to match the September 24 market price of $238.93, holding the printed inputs fixed.

## Comparable companies

| Company | EV / LTM revenue | P / reported annual diluted EPS |
|---|---:|---:|
| ADBE | 3.608608x | 14.307186x |
| ADSK | 5.557914x | 40.411090x |
| DOCU | 3.541602x | 46.614865x |

| Peer output for ADBE | Minimum | Median | Maximum |
|---|---:|---:|---:|
| EV / LTM revenue implied price | $234.46 | $301.73 | $369.00 |
| P / annual GAAP diluted EPS implied price | $674.87 | $726.67 | $778.47 |

The two methods are shown separately and are not averaged. See [adobe_project1_sources.md](adobe_project1_sources.md) for data dates, definitions, and why the P/E reference is not used as a committee range.
