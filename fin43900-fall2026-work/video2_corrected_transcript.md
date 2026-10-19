# Video 2 — Code and Validation: Corrected Transcript

**Duration:** 3:26  
**Source:** Gemini-generated transcript reviewed and corrected for clear speech-recognition, punctuation, and finance-term errors.

**0:01**

This video explains how my submitted code produces a result and how I tested it. The main file is `adobe_project1.py`. It is standard-library Python. The editable inputs at the top include Adobe's FY2025 opening balance sheet, FY2026 guidance-based revenue, future revenue and margin assumptions, working-capital ratios, debt assumptions, WACC, terminal growth, valuation-date cash and debt, and point-in-time shares.

The model forecasts FY2026 through FY2030. It links the income statement, balance sheet, and cash flow. It computes FCFF from EBIT after tax, plus D&A, less capital spending and the change in operating working capital. It then values enterprise value from five years of FCFF plus a Gordon-growth terminal value. The enterprise-to-equity bridge adds $5.639 billion of cash and investments, subtracts $6.363 billion of debt, and divides by 389.2 million shares.

**1:10**

The first validation is the FY2025 opening balance-sheet reconciliation. Assets equal liabilities plus equity at $29.496 billion. For every projected year, the model prints a zero balance-sheet gap, a cash-flow-to-balance-sheet cash tie, and cash above the stated floor. If one of those checks fails, the valuation will not run.

The base FCFF DCF prints $128.416 billion enterprise value, $127.692 billion equity value, and $328.09 per share. The terminal value is 71.8% of enterprise value, which is why I do not treat the result as precise.

The sensitivity table checks that value rises as terminal growth rises and falls as WACC rises. The code also enforces that direction through a monotonicity check.

**2:17**

My locked changed-input test increased WACC from 10% to 11%. I predicted value would fall. It fell from $328.09 to $288.49, a negative $39.60 change, with other inputs held fixed.

My highest-risk WACC test increased WACC to 12%. Value fell to $257.25, still $18.32 above the saved market price. That did not reverse my Initiate call, but it materially narrowed the margin of safety.

The second file calculates comparable-company EV/revenue and P/E multiples. I use Autodesk and DocuSign under a written peer policy. The model keeps DCF, EV/revenue, and P/E outputs separate. It does not average them. The final process check ran both scripts successfully with Python 3.13.16 and no errors.
