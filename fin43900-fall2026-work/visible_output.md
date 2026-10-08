# Visible executed output — 2026-10-07

Commands run successfully:

```sh
./.uv/bin/python3.13 adobe_proforma.py
./.uv/bin/python3.13 dcf.py
./.uv/bin/python3.13 peer_valuation.py
```

## Adobe pro-forma draft

All annual balance checks printed `0.0` for FY2026E–FY2030E. Cash was at or above the stated minimum in every projected year.

| Output | FY2030E |
|---|---:|
| Revenue (USD millions) | 31,794.1 |
| Operating income (USD millions) | 17,323.0 |
| FCFE (USD millions) | 13,817.6 |
| Value per share | Unavailable — placeholder working-capital, financing, debt-repayment, and buyback inputs |

The base-reset sensitivity check reran successfully and printed FY2030E FCFE of $13,817.6m.

## Standalone FCFF DCF

| Output | Current run |
|---|---:|
| Enterprise value (USD millions) | 180,430.9460 |
| Equity value (USD millions) | 179,651.9460 |
| Value per diluted share | $420.7306 |
| Terminal-value PV share of enterprise value | 73.38% |
| Reverse-DCF target price | $257.60 |
| Solved uniform explicit-growth shift | −11.42 percentage points |

This output remains a standalone, later-date model and is not a final same-date Project 1 conclusion.

## Peer P/E calculator

| Output | Current run |
|---|---:|
| ADSK P/E | 58.042969x |
| DOCU P/E | 13.720472x |
| Adobe minimum implied price | $169.59 |
| Adobe median implied price | $443.50 |
| Adobe maximum implied price | $717.41 |

Removing ADSK produced the DOCU-only $169.59 reference. Removing DOCU produced the ADSK-only $717.41 reference.
