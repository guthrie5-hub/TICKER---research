# Adobe DCF Inputs

| Input | Training value | Source and exact locator |
|---|---:|---|
| Starting FCFF | **$10,067.7m USD**<br>FY ended 2025-11-28<br>*Estimated* | Adobe FY2025 annual report:<br>Cash Flows, p. 52, lines 2276 and 2282;<br>interest expense, p. 40, line 1806;<br>effective tax rate, p. 41, line 1831.<br>[Annual report](https://www.adobe.com/cc-shared/assets/investor-relations/pdfs/adbe-2025-annual-report.pdf) |
| Growth, Years 1–5 | **10% · 9% · 8% · 7% · 6%**<br>As of 2026-09-10<br>*Analyst forecast* | Revenue history: FY23 $19,409m; FY24 $21,505m; FY25 $23,769m.<br>Annual report, MD&A, p. 36, lines 1602–1612.<br>FY26 guidance midpoint: $26,550m; Q2 FY26 release, p. 2, lines 47–48.<br>[Annual report](https://www.adobe.com/cc-shared/assets/investor-relations/pdfs/adbe-2025-annual-report.pdf) · [Guidance](https://www.adobe.com/cc-shared/assets/investor-relations/pdfs/11606202/a5543arefgt.pdf) |
| WACC | **10.33%**<br>As of 2026-09-10<br>*Calculated estimate* | Calculation inputs: beta 1.20, risk-free rate 4.80%, and pre-tax debt cost 3.93%.<br>Tax rate: Adobe annual report, p. 41, line 1831.<br>[WACC inputs](https://www.deepviews.dev/en/wacc/adbe) |
| Terminal growth | **3.00%**<br>As of 2026-09-10<br>*Valuation assumption* | FOMC long-run estimates: 2.0% real GDP and 2.0% PCE inflation. The 3.0% rate is a conservative company-terminal-growth assumption, not Adobe guidance.<br>[FOMC projections](https://www.federalreserve.gov/monetarypolicy/2026-07-mpr-part3-accessible.htm) |
| Non-operating cash | **$5,626.0m USD**<br>As of 2026-05-29 | Q2 FY26 10-Q, cash plus short-term investments, lines 147–148.<br>[10-Q](https://www.sec.gov/Archives/edgar/data/796343/000079634326000112/adbe-20260529.htm) |
| Debt | **$6,645.0m USD**<br>As of 2026-05-29 | Q2 FY26 10-Q, current debt plus long-term debt, lines 164 and 170.<br>[10-Q](https://www.sec.gov/Archives/edgar/data/796343/000079634326000112/adbe-20260529.htm) |
| Diluted shares | **427.0m shares**<br>FY ended 2025-11-28 | FY25 annual report, EPS note, p. 80, line 3506: diluted weighted-average shares.<br>[Annual report](https://www.adobe.com/cc-shared/assets/investor-relations/pdfs/adbe-2025-annual-report.pdf) |
| Reverse-DCF price target | **$250.35/share USD**<br>2026-09-10, 11:09 AM EDT | ADBE estimates-page quote header.<br>[Source](https://businessquant.com/stocks/adbe/estimates) |

## Calculation notes

- **Starting FCFF:** $10,031.0m operating cash flow + ($263.0m interest expense × 82%) − $179.0m capital expenditures = **$10,067.7m**. Cash interest paid is not separately disclosed, so interest expense is an explicit proxy.
- **WACC:** cost of equity = 4.80% + (1.20 × 5.00%) = 10.80%; after-tax debt cost = 3.93% × 82% = 3.22%; weighted by 93.84% equity and 6.16% debt = **10.33%**.

## Lab 07 — Adobe P/E comparison

**Comparison-date convention:** November 8, 2025 was a Saturday, so every price below is the regular-market close on the immediately preceding trading day, **November 7, 2025**. All figures are USD per common share. The calculator uses reported **GAAP diluted EPS** only; adjusted/non-GAAP EPS is shown separately and is not mixed into the calculation.

| Company | Policy / calculator treatment | Price: Nov. 7, 2025 close | Annual reported diluted EPS used | Fiscal year-end; publication date | Source and exact locator | Reported vs. adjusted / qualification |
|---|---|---:|---:|---|---|---|
| Adobe (ADBE) | Target | $326.95 | $12.36 GAAP | 2024-11-29; 2024-12-11 | [FY24 earnings release](https://www.adobe.com/content/dam/cc/en/investor-relations/pdfs/11214202/a56sthg53egr.pdf), “Fiscal Year 2024 Financial Highlights,” diluted EPS; [FY24 10-K](https://www.sec.gov/Archives/edgar/data/796343/000079634325000004/adbe-20241129.htm), Consolidated Statements of Income / EPS note; [historical price](https://sg.finance.yahoo.com/quote/ADBE/history/), row “Nov 7, 2025.” | Non-GAAP diluted EPS was $18.42; not used. |
| Autodesk (ADSK) | **USE** — entered | $297.18 | $5.12 GAAP | 2025-01-31; 2025-02-27 | [FY25 earnings release](https://investors.autodesk.com/news-releases/news-release-details/autodesk-inc-announces-fiscal-2025-fourth-quarter-and-full-year), “Fiscal 2025” GAAP diluted EPS; [FY25 10-K](https://www.sec.gov/Archives/edgar/data/769397/000076939725000019/adsk-20250131.htm), Consolidated Statements of Operations; [historical price](https://chartexchange.com/symbol/nasdaq-adsk/historical/), row “2025-11-07.” | Non-GAAP diluted EPS was $8.47; not used. Subscription professional design software supports the policy, but Autodesk is concentrated in AEC/manufacturing design-and-make workflows rather than Adobe’s creative, document, and experience mix. |
| DocuSign (DOCU) | **USE** — entered | $69.70 | $5.08 GAAP | 2025-01-31; 2025-03-13 | [FY25 earnings release](https://investor.docusign.com/news-and-events/press-releases/news-details/2025/Docusign-Announces-Fourth-Quarter-and-Fiscal-Year-2025-Financial-Results/default.aspx), “Fiscal 2025” GAAP diluted EPS; [FY25 10-K](https://www.sec.gov/Archives/edgar/data/1261333/000126133325000024/docu-20250131.htm), Consolidated Statements of Operations; [historical price](https://chartexchange.com/symbol/nasdaq-docu/historical/), row “2025-11-07.” | Non-GAAP diluted EPS was $3.55; not used. Its agreement/e-signature subscription business overlaps Adobe Document Cloud, but is narrower. FY25 GAAP results include a $837.3m valuation-allowance release; see FY25 10-K, income-tax note. |
| Salesforce (CRM) | **USE** — not entered in this two-candidate implementation | Unresolved | Unresolved | Unresolved | Not investigated for this two-candidate calculation. | Policy unchanged; not an exclusion. Enterprise subscription software and marketing/customer-experience overlap support its USE designation. |
| Intuit (INTU) | **QUALIFY** — not entered in this two-candidate implementation | Unresolved | Unresolved | Unresolved | Not investigated for this two-candidate calculation. | Policy unchanged; payments and financial-services exposure makes its economics less comparable. |
| Microsoft (MSFT) | **EXCLUDE** | Not applicable | Not applicable | Not applicable | Policy source: student peer policy. | Diversified cloud infrastructure, hardware, gaming, and advertising businesses exceed the policy scope. |
| Canva | **EXCLUDE** | Not applicable | Not applicable | Not applicable | Policy source: student peer policy. | Strong creative-software overlap, but it is private and has no public share price. |

### Calculator result

Saved command: `./.uv/bin/python3.13 peer_valuation.py`

- Inputs: ADBE FY2024 GAAP diluted EPS $12.36; ADSK Nov. 7, 2025 close $297.18 and FY2025 GAAP diluted EPS $5.12; DOCU Nov. 7, 2025 close $69.70 and FY2025 GAAP diluted EPS $5.08.
- Terminal output: ADSK P/E **58.042969x** and DOCU P/E **13.720472x**; the resulting ADBE implied range is **$169.59 to $717.41**, with a two-peer median-implied price of **$443.50**. This is a peer-relative reference, not evidence that Adobe is fairly valued.
- Leave-one-out check: removing ADSK leaves the DOCU reference estimate of **$169.59** (−$273.91 from the full-peer median); removing DOCU leaves the ADSK reference estimate of **$717.41** (+$273.91). One remaining peer is a reference estimate, not a range.
- Both selected peers and Adobe report positive annual GAAP diluted EPS, so P/E is mathematically meaningful. DOCU’s disclosed tax valuation-allowance release is a material comparability limitation even though its reported EPS is positive.

### Validation — DocuSign peer

- **Source check:** DOCU’s Nov. 7, 2025 close was **$69.70** ([historical-price row](https://chartexchange.com/symbol/nasdaq-docu/historical/)); DocuSign reported FY2025 GAAP diluted EPS of **$5.08**, for the year ended Jan. 31, 2025, in its Mar. 13, 2025 [earnings release](https://investor.docusign.com/news-and-events/press-releases/news-details/2025/Docusign-Announces-Fourth-Quarter-and-Fiscal-Year-2025-Financial-Results/default.aspx) and [10-K](https://www.sec.gov/Archives/edgar/data/1261333/000126133325000024/docu-20250131.htm).
- **Hand check:** $69.70 ÷ $5.08 = **13.720472x**, matching the calculator’s DOCU P/E before display rounding.
- **Prediction:** Removing high-multiple ADSK should lower the full-peer median-implied ADBE price because the remaining DOCU multiple is much lower.
- **Read from calculator:** Removing ADSK gives the DOCU-only reference estimate of **$169.59**, a **−$273.91** change from the $443.50 full-peer median. ADSK remains admitted: the change reflects the two peers’ different reported P/E multiples, not grounds to remove an inconvenient peer. With one peer remaining, there is no peer range; removing that sole usable peer would leave no estimate.

## Valuation comparison and provisional call

| Method | Adobe result and date | Main assumption or limitation |
|---|---|---|
| Week 3 DCF | Sensitivity-grid range: **$341.22–$582.55 per share**; base case: **$407.95**. Inputs are dated through 2026-05-29, with FY2025 FCFF and shares; output run 2026-09-17. | Five-year FCFF growth path of 10%, 9%, 8%, 7%, and 6%; 10.33% WACC; 3.0% terminal growth. The terminal-value present value is 72.54% of enterprise value. Most importantly, this DCF contains information later than the Nov. 7, 2025 peer-price date. |
| Peer P/E | **$169.59–$717.41 per share**; median-implied **$443.50**, based on the Nov. 7, 2025 comparison date. | ADSK and DOCU are the two admitted peers, using annual reported GAAP diluted EPS. DOCU’s $5.08 GAAP EPS includes a disclosed $837.3m tax valuation-allowance release, which weakens comparability; its $3.55 non-GAAP EPS was not substituted. |

**Provisional call sent to the resumed chat:** **Watch—defer.** I will not average the two methods or treat either midpoint as a decision price. I would reconsider after putting both analyses on the same information date and determining whether the DocuSign GAAP tax benefit should materially limit its use as a P/E reference. **Monitor:** Adobe’s next reported recurring-revenue growth and operating margin.

**What could most easily change my mind:** A rebuild of the DCF using only data public by Nov. 8, 2025 could materially alter the FCFF, net-debt, share-count, and valuation inputs; alternatively, evidence that the valuation-allowance release makes DOCU’s FY2025 GAAP EPS nonrepresentative would remove confidence in the low end of the peer range.

### Skeptical-colleague review of the comparison

**Criticism:** The weakest supported assumption is that the DCF and P/E outputs can be compared as if they describe the same valuation date. The P/E table uses Nov. 7, 2025 market prices and financial information public by Nov. 8, 2025; the DCF uses FY2025 FCFF and shares, plus May 29, 2026 cash and debt. That is a look-ahead/date mismatch. There is also an earnings-definition/comparability warning: the peer calculation correctly uses GAAP diluted EPS consistently, but DOCU’s FY2025 GAAP EPS includes the $837.3m valuation-allowance release, whereas the DCF values FCFF rather than EPS. The figures should not be averaged or treated as interchangeable valuation objects.

**Question that could change my decision:** Can the DCF be rebuilt using only Adobe financial data and assumptions that were public on or before Nov. 8, 2025, and does that same-date DCF still place value above the Nov. 7, 2025 price of $326.95?

**Check of the criticism: ACCEPT.** The DCF source table itself dates cash and debt to 2026-05-29 and its output to 2026-09-17, while the P/E table dates every price to 2025-11-07. DocuSign’s FY2025 10-K says the $837.3m valuation-allowance release was the primary cause of its $819.9m income-tax benefit ([income-tax note](https://www.sec.gov/Archives/edgar/data/1261333/000126133325000024/docu-20250131.htm)); therefore the warning is supported. This does not justify excluding DOCU under the stated policy, but it does justify treating the comparison as provisional.

## Reflection — Adobe conclusion

My policy is to use listed companies with primarily subscription-based software revenue and economics similar to Adobe’s creative, document, or enterprise-software businesses. I admitted **Autodesk** because its subscription-based professional-design software has recurring software economics, while qualifying that its AEC/manufacturing design-and-make focus differs from Adobe’s broader creative, document, and digital-experience mix. I admitted **DocuSign** because its subscription agreement and e-signature business overlaps Adobe Document Cloud, while qualifying that it is a narrower business and that its FY2025 GAAP EPS includes the disclosed tax valuation-allowance release. I did not remove either peer after seeing the valuation result. Microsoft remains excluded for its broad non-software and diversified businesses; Canva remains excluded because it is private. The DOCU hand check ($69.70 ÷ $5.08 = 13.720472x) supports the calculator input.

The peer comparison adds a market-based cross-check: on the common Nov. 7, 2025 price date, the two GAAP P/E references imply **$169.59–$717.41** for Adobe, with a median of **$443.50**. It also exposes how dependent the result is on peer selection: removing ADSK leaves only the DOCU reference of $169.59, while removing DOCU leaves only the ADSK reference of $717.41. The DCF instead gives a $341.22–$582.55 sensitivity range (base $407.95), based on forecast FCFF, WACC, terminal growth, and a terminal value that is 72.54% of enterprise value.

I do **not** combine or average these outputs. They differ partly because P/E capitalizes reported accounting earnings and the DCF values forecast cash flow, but the more decisive problem is comparability: the peer prices are Nov. 7, 2025, while the saved DCF uses FY2025 and 2026 information. The P/E range is also unusually wide, and DOCU’s reported EPS has a material, sourced tax item. I can defend the two results only as separate references, not as a single Adobe valuation range.

**Call: Watch—defer.** I withhold a combined price target. I would change this decision if a DCF rebuilt solely with information public by Nov. 8, 2025 still supported value above Adobe’s $326.95 Nov. 7 price, and if updated results supported the assumed FCFF growth and margin path. Evidence that DOCU’s tax benefit makes its GAAP EPS nonrepresentative would further reduce confidence in the low-P/E peer reference, but would not retroactively justify removing it under the stated peer policy.

**Answer to the skeptical question:** The saved DCF cannot answer whether a same-date DCF still exceeds $326.95 because it relies on later inputs. The proper answer is therefore unresolved pending a cutoff-date rebuild—not an inference from the later DCF or an average with P/E.
