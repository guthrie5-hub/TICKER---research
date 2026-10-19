# Adobe Project 1 — sources and assumption challenge record

All money is USD millions unless stated otherwise. The common valuation date is **September 24, 2026**. The security is Adobe common stock (NASDAQ: ADBE); the per-share bridge uses **389.2 million point-in-time shares outstanding**, not a weighted-average EPS denominator.

## Scope and dated facts

| Item | Value / definition | As-of | Primary locator |
|---|---|---|---|
| FY2025 opening financial statements | Audited fiscal-year base for FY2026E–FY2030E model | November 28, 2025 | [Adobe FY2025 10-K](https://www.sec.gov/Archives/edgar/data/796343/000079634326000003/adbe-20251128.htm), Consolidated Balance Sheets, Statements of Income and Cash Flows; Notes 6, 15 and 17. |
| Valuation-date cash and investments | $5,639 = $4,359 cash + $1,280 short-term investments | August 28, 2026 balance sheet, available by September 24 | [Adobe Q3 FY2026 10-Q](https://www.sec.gov/Archives/edgar/data/796343/000079634326000156/adbe-20260828.htm), Condensed Consolidated Balance Sheets. |
| Valuation-date debt | $6,363 = $1,597 current + $4,766 long-term carrying amount | August 28, 2026 | Same Q3 10-Q, Condensed Consolidated Balance Sheets and debt note. |
| Share basis | 389.2 million shares outstanding | September 18, 2026 | Same Q3 10-Q, cover page. |
| ADBE price | $238.93 close | September 24, 2026 | [StockAnalysis ADBE price history](https://stockanalysis.com/stocks/adbe/history/), historical daily-price table. Secondary market-data source; the date and close should be rechecked before final submission. |
| FY2026 revenue guidance | $26,576–$26,626; model uses midpoint $26,601 | September 10, 2026 | [Adobe Q3 FY2026 release](https://www.sec.gov/Archives/edgar/data/796343/000079634326000147/adbeex991q326.htm), “Financial Targets,” updated FY2026 targets. |
| FY2026 GAAP operating-margin and tax assumptions | 35% GAAP operating margin and 22.5% GAAP tax rate | September 10, 2026 | Same release, FY2026 targets and assumptions. |

## Base-year reconciliation and normalization

The model begins with the FY2025 audited balance sheet: cash $5,431; short-term investments $1,164; receivables $2,344; prepaids $1,224; PP&E $1,873; other assets $17,460; liabilities $17,873; and equity $11,623. Assets and liabilities plus equity each equal **$29,496**. This is printed at the start of `adobe_project1.py`.

The income-statement base remains GAAP. The forecast does **not** carry forward the Q2 FY2026 $70 million goodwill impairment or $30 million loss contingency shown in Adobe’s Q3 release non-GAAP reconciliation; treating those as recurring operating costs would be a normalization choice, not a reported fact. Adobe’s Semrush acquisition and other acquisition effects remain a risk rather than being treated as a separately modeled benefit. This is a limitation to monitor, not evidence that the items cannot recur.

## Load-bearing model assumptions

| Driver | Value in `adobe_project1.py` | Label / basis | Challenge | Evidence that would change it |
|---|---|---|---|---|
| FY2026 revenue | $26,601 | Guidance midpoint | Guidance can change or actual Q4 can differ. | FY2026 10-K / Q4 release. |
| FY2027–FY2030 revenue | $29,261; $31,602; $33,498; $34,838 | Judgment: 10%, 8%, 6%, 4% growth fade after guided FY2026 | AI monetization may accelerate revenue; competition, pricing, or execution can reduce it. | Reported subscription revenue, ARR/RPO trends, management guidance. |
| Gross margin | 89.2% each year | History: FY2025 gross profit ÷ revenue was about 89.3%; held near that level | Cloud/AI inference or partner costs could pressure gross margin. | Reported cost of revenue and gross margin. |
| Operating margin | 35.0%, 35.5%, 36.0%, 36.25%, 36.5% | FY2026 guidance then judgmental modest leverage | This assumes efficiency despite AI investment and sales expense. | GAAP operating-margin guidance and reported R&D, S&M, G&A. |
| Tax | 22.5%, then 22.0% | FY2026 GAAP guidance then judgment | Mix and discrete tax items can move the effective rate. | Reported tax provision / earnings releases. |
| Total D&A / revenue | 3.0% | FY2026 Q3 cash-flow D&A annualized is a rough history anchor; held flat | Annualized quarterly D&A is not a forecast. | FY2026 10-K cash-flow statement. |
| PP&E depreciation / revenue | 1.0% | FY2025 PP&E depreciation $236 and Q3 balance-sheet PP&E; judgmental simplification | PP&E depreciation differs from total D&A and could change with infrastructure spend. | PP&E note and capex guidance. |
| Capex / revenue | 1.3% | Judgment near FY2025 capex $179m / revenue and Q3 FY2026 capex $85m | AI infrastructure needs can make this too low. | FY2026 capex and purchase-obligation disclosures. |
| Operating working capital | FY2025 balance-sheet ratios for receivables, prepaids, payables, accruals, deferred revenue, taxes payable | History | Ratios can move with billings and revenue recognition; deferred revenue is material. | Quarterly balance sheets and billings/RPO disclosure. |
| Debt repayment | $0; $1,350; $800; $750; $2,000 | Judgment based on debt notes / maturities, capped at debt | Refinancing or new borrowing makes the schedule wrong. | Debt maturities, new notes, and credit agreement updates. |
| Buybacks | $6,000 annually | Judgment; FY2026 Q3 repurchases were $2,232 in one quarter | Board authorization and cash priorities can change; this affects projected cash/equity, not FCFF valuation. | Repurchase authorization and cash-flow disclosures. |
| WACC | 10.0% | Judgment; stress-tested at 9%–11% | Cost of equity and capital structure are not directly observed. | Recomputed beta, risk-free rate, ERP, debt yields, and capital structure. |
| Terminal growth | 2.5% | Judgment below WACC and long-run nominal economic growth | Terminal value is 71.8% of EV, so small changes matter. | Long-run growth rationale; a different sustained-margin/reinvestment view. |

## Comparable-company policy and source bases

Policy set before selection: use listed operating companies with primarily subscription-based software revenue and digital/creative, document, or enterprise-software economics. Exclude major hardware, advertising, financial-services, or non-software operations. Autodesk and DocuSign are admitted; Intuit is qualified but not used because payments/financial-services economics are material; Microsoft is excluded as too diversified; Canva is private.

| Company | Decision | Business-model source | September 24 price / share basis / financial inputs |
|---|---|---|---|
| Autodesk (ADSK) | Use; recurring professional design software, but AEC/manufacturing exposure differs from Adobe’s creative/document mix. | [FY2026 10-K](https://www.sec.gov/Archives/edgar/data/769397/000076939726000015/adsk-20260131.htm), Business and revenue discussion. | $211.35 close: [ChartExchange history](https://chartexchange.com/symbol/nasdaq-adsk/historical/). 209.0m shares, $4,360m cash/investments, $3,484m debt: [Q2 FY2027 10-Q](https://www.sec.gov/Archives/edgar/data/769397/000076939726000061/adsk-20260731.htm), cover page and balance-sheet/debt notes. LTM revenue $7,790 = FY2026 $7,206 − first-half FY2026 $3,396 + first-half FY2027 $3,980. FY2026 GAAP diluted EPS $5.23. |
| DocuSign (DOCU) | Use; subscription document/e-signature overlap, but narrower product scope and different maturity. | [FY2026 10-K](https://www.sec.gov/Archives/edgar/data/1261333/000126133326000021/docu-20260131.htm), Business section. | $68.99 close: [StockAnalysis DOCU history](https://stockanalysis.com/stocks/docu/history/). 186.902452m shares, $990.4m cash/investments, no reported debt: [Q2 FY2027 10-Q](https://www.sec.gov/Archives/edgar/data/1261333/000126133326000099/docu-20260731.htm), cover page, liquidity and debt notes. LTM revenue $3,361.191 = FY2026 $3,219.5 − first-half FY2026 $1,564.290 + first-half FY2027 $1,705.981. FY2026 GAAP diluted EPS $1.48. |

`adobe_ev_comps.py` defines EV as price × point-in-time shares + debt − cash and short-term investments. Its EV/revenue price range is $234.46–$369.00, with a $301.73 median reference. The annual-GAAP P/E reference is printed separately; it is not blended with EV/revenue or DCF because the annual EPS fiscal periods differ and the resulting $674.87–$778.47 range is not an economically comparable decision range.

## Independent check already performed

The Adobe Q3 release reports FY2026 revenue guidance of $26.576bn–$26.626bn; the model’s $26.601bn FY2026 input is the arithmetic midpoint: ($26.576bn + $26.626bn) ÷ 2. This check ties one load-bearing forecast input directly to Adobe’s filed release.

