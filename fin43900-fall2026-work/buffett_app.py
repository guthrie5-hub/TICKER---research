"""Streamlit panel for three SEC EDGAR 10-K investor screens."""

import re

import streamlit as st

from edgar_owner_earnings import (
    GRAHAM_CURRENT_RATIO_THRESHOLD,
    analyse_ticker,
    display_ratio,
    display_value,
    memo_text,
    panel_verdict,
)


def memo_unprinted_numbers(memo, result):
    """Flag numeric tokens in any memo that the shared report did not print."""
    printed_values = []
    for row in result["rows"]:
        printed_values.append(row["fiscal_year_end"])
        for key in (
            "revenue", "net_income", "operating_cash_flow", "capital_spending", "equity",
            "liabilities", "current_assets", "current_liabilities",
        ):
            printed_values.append(display_value(row[key]["value"]))
        printed_values.extend((
            display_value(row["roe"], percent=True),
            display_ratio(row["current_ratio"]),
            display_ratio(row["liabilities_to_equity"]),
            display_value(row["owner_earnings"]),
        ))
    printed_values.extend((
        "15",
        "2",
        f"{GRAHAM_CURRENT_RATIO_THRESHOLD:.2f}",
        result["download_date"],
        "10-K",
    ))
    printed = set(re.findall(r"\d+(?:\.\d+)?", " ".join(printed_values)))
    memo_values = set(re.findall(r"\d+(?:\.\d+)?", memo))
    return sorted(value for value in memo_values if value not in printed)


st.set_page_config(page_title="SEC EDGAR investor panel", layout="wide")
st.title("SEC EDGAR investor panel")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")

ticker = st.sidebar.text_input("Ticker", value="COST").strip().upper()
if st.sidebar.button("Run 10-K panel"):
    st.cache_data.clear()

try:
    result = analyse_ticker(ticker)
except ValueError as error:
    st.error(str(error))
    st.stop()

st.subheader(f"{result['company_name']} ({result['ticker']}) — last five 10-K fiscal years")
chart_rows = [
    {
        "Fiscal year end": row["fiscal_year_end"],
        "Owner earnings (USD m)": None if row["owner_earnings"] is None else row["owner_earnings"] / 1_000_000,
        "Net income (USD m)": None if row["net_income"]["value"] is None else row["net_income"]["value"] / 1_000_000,
    }
    for row in result["rows"]
]
st.line_chart(chart_rows, x="Fiscal year end", y=["Owner earnings (USD m)", "Net income (USD m)"], width="stretch")

table_rows = []
for row in result["rows"]:
    table_rows.append({
        "Fiscal year end": row["fiscal_year_end"],
        "Revenue": display_value(row["revenue"]["value"]), "Revenue tag": row["revenue"]["tag"],
        "Net income": display_value(row["net_income"]["value"]), "Net income tag": row["net_income"]["tag"],
        "Operating cash flow": display_value(row["operating_cash_flow"]["value"]), "OCF tag": row["operating_cash_flow"]["tag"],
        "Capital spending": display_value(row["capital_spending"]["value"]), "Capex tag": row["capital_spending"]["tag"],
        "Equity": display_value(row["equity"]["value"]), "Equity tag": row["equity"]["tag"],
        "Liabilities": display_value(row["liabilities"]["value"]), "Liabilities tag": row["liabilities"]["tag"],
        "Current assets": display_value(row["current_assets"]["value"]), "Current assets tag": row["current_assets"]["tag"],
        "Current liabilities": display_value(row["current_liabilities"]["value"]), "Current liabilities tag": row["current_liabilities"]["tag"],
        "ROE": display_value(row["roe"], percent=True),
        "Current ratio": display_ratio(row["current_ratio"]),
        "Liabilities / equity": display_ratio(row["liabilities_to_equity"]),
        "Owner earnings": display_value(row["owner_earnings"]),
    })
st.dataframe(table_rows, hide_index=True, width="stretch")

st.subheader("Investor panel")
check_names = sorted({name for checks in result["panels"].values() for name in checks})
panel_rows = []
for investor, checks in result["panels"].items():
    panel_rows.append({
        "Investor": investor,
        **{name: checks.get(name, "—") for name in check_names},
        "Verdict": panel_verdict(checks),
    })
st.dataframe(panel_rows, hide_index=True, width="stretch")

st.subheader("Memos")
columns = st.columns(3)
memo_entries = []
for column, investor in zip(columns, ("Buffett", "Graham", "Burry")):
    with column:
        memo = memo_text(result, investor)
        edited_memo = st.text_area(
            f"{investor} memo to check",
            value=memo,
            height=210,
            key=f"{result['ticker']}_{investor}_memo",
        )
        memo_entries.append((investor, edited_memo))

for investor, memo in memo_entries:
    unprinted = memo_unprinted_numbers(memo, result)
    if unprinted:
        st.error(f"{investor}: memo number(s) not printed by the script: {', '.join(unprinted)}")
    else:
        st.success(f"{investor}: every memo number appears in the script output.")
