# Adobe Inc. (ADBE) DCF Valuation & Research

Course project for **FIN 43900 — AI Finance Applications** (Purdue, Fall 2026).

## Files

- **dcf.py** — Five-year free cash flow to firm (FCFF) discounted cash flow model
  - Calculates equity value per diluted share
  - Includes sensitivity analysis (WACC vs. terminal growth)
  - Reverse-DCF solver using bisection
  
- **project-1.md** — Initial research report on Adobe Inc.
  - Business overview and operating metrics
  - Investment thesis and key open questions
  
- **sources.md** — Source log and management guidance tracking
  - Prior 10-K filings and outcomes
  - Recent earnings call data
  
- **Table.md** — Financial data reference
- **Agents.md** — Course guidelines

## Quick start

Run the DCF model:
```bash
python dcf.py
```

This produces:
- Five-year FCFF projections
- Present values and enterprise/equity value
- Sensitivity grid (terminal growth rate × WACC)
- Reverse-DCF solution for a target share price

## Data sources

All data from Adobe Inc. Form 10-K (fiscal year ended November 28, 2025, filed January 15, 2026) and Q4 2025 earnings call transcript.

---

**Disclaimer:** This is a learning exercise, not investment research or financial advice.
