"""Streamlit viewer for the SEC EDGAR Buffett-style owner-earnings analysis."""

import re

import streamlit as st

from edgar_owner_earnings import analyse_ticker, display_value, memo_text


def memo_unprinted_numbers(memo, result):
    """Flag numeric tokens in the memo that the report did not print."""
    printed = set(re.findall(r"\d+(?:\.\d+)?", " ".join(
        [row["fiscal_year_end"] for row in result["rows"]]
        + [display_value(row[key]["value"]) for row in result["rows"] for key in (
            "revenue", "net_income", "operating_cash_flow", "capital_spending", "equity"
        )]
        + [display_value(row["roe"], percent=True) for row in result["rows"]]
        + [display_value(row["owner_earnings"]) for row in result["rows"]]
        + ["15", result["download_date"], "10"]
    )))
    memo_values = set(re.findall(r"\d+(?:\.\d+)?", memo))
    return sorted(value for value in memo_values if value not in printed)


st.set_page_config(page_title="EDGAR Buffett-style review", layout="wide")
st.title("SEC EDGAR Buffett-style business review")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")

ticker = st.sidebar.text_input("Ticker", value="COST").strip().upper()
if st.sidebar.button("Run 10-K analysis"):
    st.cache_data.clear()

try:
    result = analyse_ticker(ticker)
except ValueError as error:
    st.error(str(error))
    st.stop()

st.subheader(f"{result['company_name']} ({result['ticker']}) — last five 10-K fiscal years")
chart_rows = []
for row in result["rows"]:
    chart_rows.append({
        "Fiscal year end": row["fiscal_year_end"],
        "Owner earnings (USD m)": None if row["owner_earnings"] is None else row["owner_earnings"] / 1_000_000,
        "Net income (USD m)": None if row["net_income"]["value"] is None else row["net_income"]["value"] / 1_000_000,
    })
st.line_chart(chart_rows, x="Fiscal year end", y=["Owner earnings (USD m)", "Net income (USD m)"], width="stretch")

table_rows = []
for row in result["rows"]:
    table_rows.append({
        "Fiscal year end": row["fiscal_year_end"],
        "Revenue": display_value(row["revenue"]["value"]),
        "Revenue tag": row["revenue"]["tag"],
        "Net income": display_value(row["net_income"]["value"]),
        "Net income tag": row["net_income"]["tag"],
        "Operating cash flow": display_value(row["operating_cash_flow"]["value"]),
        "Operating cash flow tag": row["operating_cash_flow"]["tag"],
        "Capital spending": display_value(row["capital_spending"]["value"]),
        "Capital spending tag": row["capital_spending"]["tag"],
        "Equity": display_value(row["equity"]["value"]),
        "Equity tag": row["equity"]["tag"],
        "ROE": display_value(row["roe"], percent=True),
        "Owner earnings": display_value(row["owner_earnings"]),
        "Owner earnings tag": row["owner_earnings_tag"],
    })
st.dataframe(table_rows, hide_index=True, width="stretch")

st.subheader("Buffett-style checks")
for label, outcome in result["checks"].items():
    st.write(f"**{label}:** {outcome}")

memo = memo_text(result)
st.subheader("Memo")
memo_to_check = st.text_area(
    "Memo to check (edit here to test unsupported numbers)",
    value=memo,
    height=150,
)
unprinted = memo_unprinted_numbers(memo_to_check, result)
if unprinted:
    st.error(f"Memo number(s) not printed by the script: {', '.join(unprinted)}")
else:
    st.success("Every number in the memo appears in the script output.")
