"""A point-in-time FRED and ALFRED rate-data viewer."""

import csv
import ssl
from datetime import date
from io import StringIO
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import certifi
import altair as alt
import streamlit as st


SERIES_NAMES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv"
ALFRED_CSV = "https://alfred.stlouisfed.org/graph/alfredgraph.csv"
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())


def fetch_csv(url, parameters):
    """Download one public FRED or ALFRED CSV request and parse valid values."""
    request_url = f"{url}?{urlencode(parameters)}"
    request = Request(request_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(request, timeout=30, context=SSL_CONTEXT) as response:
            text = response.read().decode("utf-8-sig")
    except HTTPError as error:
        raise ValueError(f"FRED returned HTTP {error.code} for {parameters['id']}.") from error
    except URLError as error:
        raise ValueError(f"Could not reach FRED for {parameters['id']}: {error.reason}") from error

    reader = csv.DictReader(StringIO(text))
    fields = reader.fieldnames or []
    if len(fields) < 2:
        raise ValueError(f"No usable CSV data returned for {parameters['id']}.")
    date_column, value_column = fields[0], fields[1]
    rows = []
    for row in reader:
        raw_value = row.get(value_column, "")
        if raw_value in ("", "."):
            continue
        try:
            rows.append((date.fromisoformat(row[date_column]), float(raw_value)))
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid observation in FRED data for {parameters['id']}.") from error
    if not rows:
        raise ValueError(f"No numeric observations returned for {parameters['id']}.")
    return rows


@st.cache_data(show_spinner=False)
def download_fred(series_id):
    """Download current FRED values for one series."""
    return fetch_csv(FRED_CSV, {"id": series_id})


@st.cache_data(show_spinner=False)
def download_alfred(series_id, vintage_date):
    """Download the ALFRED vintage available on one specified date."""
    return fetch_csv(ALFRED_CSV, {"id": series_id, "vintage_date": vintage_date.isoformat()})


def last_observation(rows):
    """Return the latest measured observation in a nonempty list."""
    return max(rows, key=lambda row: row[0])


def revisions_since_vintage(today_rows, vintage_rows):
    """Count later-measured observations and same-date values that changed."""
    today_by_date = dict(today_rows)
    vintage_by_date = dict(vintage_rows)
    last_known_date, _ = last_observation(vintage_rows)
    later_values = sum(observation_date > last_known_date for observation_date in today_by_date)
    revised_values = sum(
        observation_date in today_by_date and today_by_date[observation_date] != vintage_value
        for observation_date, vintage_value in vintage_by_date.items()
    )
    return later_values, revised_values


def rate_chart(series_id, current_rows, start_date, vintage_rows):
    """Render one current-value line chart and its latest as-of observation."""
    chart_rows = [
        {"Date": observation_date, "Value": value}
        for observation_date, value in current_rows
        if observation_date >= start_date
    ]
    st.subheader(f"{series_id} — {SERIES_NAMES.get(series_id, 'Custom FRED series')}")
    if not chart_rows:
        st.warning("No current observations on or after the selected start date.")
    else:
        st.line_chart(chart_rows, x="Date", y="Value", width="stretch")
    known_date, known_value = last_observation(vintage_rows)
    st.caption(f"Last date in data known on the selected date: {known_date.isoformat()} — {known_value:g}")


def combined_index_chart(series_rows, start_date):
    """Compare selected current series on a common monthly, indexed basis."""
    indexed_by_date = {}
    usable_ids = []
    for series_id, rows in series_rows.items():
        monthly_last = {}
        for observation_date, value in rows:
            if observation_date >= start_date:
                month = observation_date.replace(day=1)
                monthly_last[month] = (observation_date, value)
        filtered = [monthly_last[month] for month in sorted(monthly_last)]
        if not filtered or filtered[0][1] == 0.0:
            continue
        usable_ids.append(series_id)
        base_value = filtered[0][1]
        for observation_date, value in filtered:
            month = observation_date.replace(day=1)
            indexed_by_date.setdefault(month, {"Date": month})[series_id] = value / base_value * 100.0
    if len(usable_ids) < 2:
        return
    chart_rows = []
    for observation_date in sorted(indexed_by_date):
        row = {"Date": observation_date, **{series_id: None for series_id in usable_ids}}
        row.update(indexed_by_date[observation_date])
        chart_rows.append(row)
    st.subheader("Combined current-series comparison")
    st.caption("Each series uses its last available observation each month and equals 100 at its first month; this compares change, not yield level.")
    st.line_chart(chart_rows, x="Date", y=usable_ids, width="stretch")


def dgs10_candlestick_chart(rows, start_date):
    """Render real monthly OHLC candles from DGS10's daily observations."""
    monthly_values = {}
    for observation_date, value in rows:
        if observation_date >= start_date:
            monthly_values.setdefault(observation_date.replace(day=1), []).append(value)
    candles = []
    for month, values in sorted(monthly_values.items()):
        opening, closing = values[0], values[-1]
        candles.append(
            {
                "Month": month.isoformat(),
                "Open": opening,
                "High": max(values),
                "Low": min(values),
                "Close": closing,
                "Body low": min(opening, closing),
                "Body high": max(opening, closing),
            }
        )
    if not candles:
        return
    base = alt.Chart(alt.Data(values=candles)).encode(x=alt.X("Month:T", title="Month"))
    wicks = base.mark_rule().encode(
        y=alt.Y("Low:Q", title="DGS10 yield (%)", scale=alt.Scale(zero=False)),
        y2="High:Q",
    )
    bodies = base.mark_bar(size=8).encode(
        y=alt.Y("Body low:Q", scale=alt.Scale(zero=False)),
        y2="Body high:Q",
        color=alt.condition("datum.Close >= datum.Open", alt.value("#2ca02c"), alt.value("#d62728")),
        tooltip=["Month:T", "Open:Q", "High:Q", "Low:Q", "Close:Q"],
    )
    st.subheader("DGS10 monthly candlestick chart")
    st.caption("Green: the month closed at or above its opening yield. Red: it closed below. This uses DGS10 only, not a mixed-series candle.")
    st.altair_chart(wicks + bodies, width="stretch")


def markdown_table(rows):
    """Render the required series comparison table with linked FRED IDs."""
    st.subheader("Point-in-time comparison")
    header = (
        "| Series | Last date known then | Value known then | Value today, same date | "
        "Last measured today | Today's values after then | Same-date revisions since then |\n"
        "|---|---:|---:|---:|---:|---:|---:|"
    )
    lines = [header]
    for row in rows:
        link = f"[{row['id']}](https://fred.stlouisfed.org/series/{row['id']})"
        lines.append(
            f"| {link} | {row['known_date']} | {row['known_value']:g} | "
            f"{row['same_date_value']:g} | {row['today_date']} — {row['today_value']:g} | "
            f"{row['later']} | {row['revised']} |"
        )
    st.markdown("\n".join(lines))


st.set_page_config(page_title="FRED Point-in-Time Rates", layout="wide")
st.title("FRED point-in-time interest-rate viewer")
st.caption(
    f"Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded {date.today().isoformat()}; "
    "built with AI help, a learning demonstration, not investment advice."
)

with st.sidebar:
    st.header("Data inputs")
    selected = st.multiselect(
        "Series IDs",
        options=list(SERIES_NAMES),
        default=list(SERIES_NAMES),
        format_func=lambda series_id: f"{series_id} — {SERIES_NAMES[series_id]}",
    )
    extra_id = st.text_input("Add another FRED series ID").strip().upper()
    start_date = st.date_input("Start date", value=date(2020, 1, 1))
    as_known_on = st.date_input("As known on", value=date.today())

if extra_id and extra_id not in selected:
    selected.append(extra_id)
if not selected:
    st.info("Select at least one series ID.")
    st.stop()

table_rows = []
current_series_rows = {}
for series_id in selected:
    try:
        current_rows = download_fred(series_id)
        vintage_rows = download_alfred(series_id, as_known_on)
        rate_chart(series_id, current_rows, start_date, vintage_rows)
        current_series_rows[series_id] = current_rows
        known_date, known_value = last_observation(vintage_rows)
        today_date, today_value = last_observation(current_rows)
        later_values, revised_values = revisions_since_vintage(current_rows, vintage_rows)
        current_by_date = dict(current_rows)
        if known_date not in current_by_date:
            raise ValueError("Today's FRED data does not contain the last date in the selected vintage.")
        table_rows.append(
            {
                "id": series_id,
                "known_date": known_date.isoformat(),
                "known_value": known_value,
                "same_date_value": current_by_date[known_date],
                "today_date": today_date.isoformat(),
                "today_value": today_value,
                "later": later_values,
                "revised": revised_values,
            }
        )
    except ValueError as error:
        st.error(f"{series_id}: {error}")

combined_index_chart(current_series_rows, start_date)
if "DGS10" in current_series_rows:
    dgs10_candlestick_chart(current_series_rows["DGS10"], start_date)

if table_rows:
    markdown_table(table_rows)
