# Project 1 validation record — readiness draft

## Existing evidence

| Requirement | Evidence | Status |
|---|---|---|
| Synthetic known answer | `proforma.py` is the ABG training model. Its prior documented output matched the course FY2026E/FY2030E lines and $291.75 per share. | Existing lab evidence |
| Articulation checks | `adobe_proforma.py` printed assets minus liabilities minus equity of 0.0 and cash above the floor in FY2026E–FY2030E on 2026-10-07. | Passed for the current draft |
| Directional changed-input test | The locked revenue-growth change in `adobe_proforma_research.md` predicts and records higher FY2030E revenue, operating income, and FCFE when FY2030E growth changes from 4% to 6%. | Existing lab evidence |
| Independent source check | `adobe_proforma_research.md` records checks of Adobe FY2025 10-K revenue and PP&E against the named statements/notes. | Existing lab evidence |
| Peer arithmetic check | The recorded DOCU check is $69.70 ÷ $5.08 = 13.720472x, matching `peer_valuation.py`. | Existing lab evidence |
| Sensitivity/base reset | `adobe_proforma.py` ran lower/base/higher revenue growth and SG&A/gross-profit cases, then reran base. | Passed for the current draft |

## Current high-risk limitation

The final project requires an FCFF enterprise-value DCF driven by the five-year pro-forma, with a full enterprise-to-equity bridge. The current pro-forma is FCFE-based and withholds valuation because inputs for working capital, financing, debt repayment, and buybacks are placeholders. The standalone FCFF DCF is not linked to it and uses a different information date.

## Required before final Project 1 submission

- Rebuild or revise the Adobe pro-forma to an FCFF enterprise-value architecture and source all load-bearing working-capital, financing, and share-basis inputs.
- Run and document WACC/growth boundary and monotonicity checks plus the enterprise-to-equity bridge check.
- Add one consistent enterprise-value multiple, alongside the existing equity P/E work.
- Create an assumption-challenge record for every load-bearing driver with value, basis, challenge, and evidence that would change it.
- Perform a README-only cold run in a fresh environment with another person; preserve the first failure and elapsed time.
- Write the current decision, highest-risk claim, and three possible failures yourself without AI, as required by the readiness protocol.
- Record an independently verified AI counterexample/test and the accept, correct, qualify, or reject decision.
- Record the three Project 1 videos and corrected transcripts when the project is ready.

## Readiness feedback request

Please pressure-test whether the FCFE-to-FCFF architecture gap and valuation-date mismatch are the right highest-priority repairs before further Adobe analysis.
