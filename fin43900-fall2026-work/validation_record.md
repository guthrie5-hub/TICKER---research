# Project 1 validation record — working evidence

## Completed code and source checks

| Requirement | Evidence | Status |
|---|---|---|
| Synthetic known answer | `proforma.py` is the ABG course training engine; prior lab work documented the known $291.75/share result. It remains unchanged. | Existing course-lab evidence; rerun before final freeze. |
| Base-year reconciliation | `adobe_project1.py` prints Adobe FY2025 assets $29,496.0m = liabilities plus equity $29,496.0m. | Passed. |
| Five-year articulation | The linked model prints a zero balance gap, cash-flow cash tie, and cash above the floor for each FY2026E–FY2030E. | Passed; results saved in `visible_output.md`. |
| Enterprise-to-equity bridge | Model prints EV, then adds $5,639m point-in-time cash/investments, subtracts $6,363m debt, and divides by 389.2m point-in-time shares. | Passed; inputs traced in `adobe_project1_sources.md`. |
| DCF boundary / monotonicity | `assert_dcf_monotonicity` refuses the model if valuation fails to rise with terminal growth or fall with WACC. The current run passes. | Passed. |
| Independent source / definition check | FY2026 revenue midpoint is ($26.576bn + $26.626bn) ÷ 2 = $26.601bn, matching the linked-model input. | Passed; Adobe Q3 FY2026 release locator in source record. |
| Student source-opening check | Student opened the Adobe Q3 FY2026 release and Q3 FY2026 10-Q and reported that both source checks looked good. | Confirmed by student on 2026-10-18; add exact line/section checked before final freeze. |
| Peer definition check | `adobe_ev_comps.py` defines EV = price × point-in-time shares + debt − cash/investments, and prints separate EV/revenue and P/E outputs. | Passed mechanically; source dates and comparability still require user inspection. |
| Downside case | The low AI/competition case lowers the revenue and margin paths and produces $279.39/share versus $328.09 base. | Passed as a causal what-if, not probability evidence. |

## Corrected AI output

| AI-assisted output | Independent check | Judgment |
|---|---|---|
| Initial linked-model draft used the August 2026 Q3 balance sheet as its opening balance but forecast a full FY2026. | Comparing the period dates showed a timing mismatch: an August-quarter balance sheet is not a full FY2026 opening base. The FY2025 audited balance sheet now begins the FY2026E–FY2030E forecast; the Q3 10-Q supplies the September valuation-date cash/debt/shares bridge. | **Corrected.** The change is documented in `adobe_project1.py` and `adobe_project1_sources.md`. |

## Still must be completed by the student, not invented

| Required evidence | What to record |
|---|---|
| Locked Changed-Input Record | Make an AI-off prediction before running one changed input. Record timestamp or commit, old/new units, expected and actual direction, decision effect, and diagnosis/no-change reason. The earlier lab record in `adobe_proforma_research.md` is historical; decide whether it meets the final-project boundary after checking it yourself. |
| Highest-risk failure test | Name the most decision-relevant plausible change that reverses or withholds the Initiate call; run it and preserve before/after evidence. |
| README-only cold run | A different person receives only `README.md`, records first failure and elapsed time to visible output, without coaching. |
| Source-opening check | Open and verify at least one load-bearing financial fact and one price/share-basis fact against the cited source. Write what you saw. |
| Partner fresh-eyes challenge | Record the actual challenger, their question, your response, and whether evidence changed the assumption. |
| Repository access and freeze | Confirm instructional-team access, obtain the actual commit/tag, update manifest, and save final AI-use record. |
| Videos/transcripts | Record only after the analysis is frozen; correct and save transcripts. |

## Locked Changed-Input Record — WACC test

**Locked before run:** 2026-10-18 (student-authored prediction entered before the model change)

| Field | Record |
|---|---|
| Independent input | WACC only |
| Old → new | 10.0% → 11.0%, a +1.0 percentage-point change |
| Inputs held fixed | Revenue, gross margin, operating margin, tax, D&A, capex, working-capital ratios, debt schedule, buybacks, terminal growth, cash/debt bridge, and shares. |
| Student prediction | “An increase in WACC would cause ADBE valuation to drop because returns would need to be higher for investors, discount rate is increased, and new projects may be expensive.” |
| Expected result | Value per share decreases. |
| Actual run | Base WACC 10.0%: $328.09/share. Changed WACC 11.0%: $288.49/share. Signed change: **−$39.60/share**. |
| Result versus prediction | Supported: value per share fell when the discount rate rose. The higher required return reduces the present value of explicit FCFF and terminal value. |
| Inputs restored | Yes. `adobe_project1.py` remains at its 10.0% base WACC; the test used an independent in-memory copy. |
| Decision effect | No change to the Initiate call in this test: the 11.0% case remains above the saved $238.93 market price. The smaller margin of safety reinforces the need to monitor WACC and terminal-value dependence. |
| Execution note | The first command had a shell-quoting syntax error and did not run the model. The corrected command then completed successfully. |

## README-only cold run — first attempt

| Field | Record |
|---|---|
| What the reviewer reported | “The README identifies one important limitation: the Adobe pro-forma currently withholds its value-per-share estimate because several inputs remain placeholders. The DCF is a separate valuation model.” |
| First failure | The reviewer reached an older README/version in the GitHub repository rather than the current local linked FCFF system. They therefore could not begin a cold run of the current model from the repository. |
| Diagnosis | Local files were updated, but the GitHub repository had not yet been updated to match them. |
| Repair | Push the current local files to GitHub. README now explicitly instructs the reviewer to `cd fin43900-fall2026-work` when starting at repository root and to use portable `python3` commands rather than the untracked local `.uv` interpreter. Repeat the README-only cold run without coaching. |
| Elapsed time | Not reported; obtain it on the repeat run. |

## README-only cold run — repeat after README repair

| Field | Record |
|---|---|
| Environment | Fresh clean download; Python 3.13.16; no repository files modified. |
| `python3 adobe_project1.py` | **Passed.** First and valuation output appeared in 0.034 seconds; value per share was $328.09. |
| `python3 adobe_ev_comps.py` | **Failed**, exit 2, after 0.019 seconds. |
| First issue | The README documents `adobe_ev_comps.py`, but that file was absent from `fin43900-fall2026-work` in the downloaded repository. Python reported it could not open the file. |
| Diagnosis | The current local `adobe_ev_comps.py` file has not yet been pushed to the repository branch used for the cold run. |
| Repair | Add and push `adobe_ev_comps.py` with the updated README, then repeat only `python3 adobe_ev_comps.py` from a clean download. |

## Current highest-risk claim

The Initiate call depends most on the claim that Adobe can move from FY2026 guided revenue into a long-run revenue/margin path that supports more than $10.9bn FY2030 FCFF. It is exposed to terminal-value dependence (71.8% of EV), AI/competition effects on revenue/margins, and the 10% WACC judgment. The code tests directions and downside scenarios; it does not establish their probabilities.
