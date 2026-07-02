import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="📈 Yahoo Finance Dashboard",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.metric-box{
    background:#1E1E1E;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 0px 10px rgba(255,255,255,0.05);
}

.title{
    text-align:center;
    color:#00FFAA;
    font-size:40px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:gray;
    margin-bottom:30px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------

st.markdown("<div class='title'>📈 Live Stock Market Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Powered by Yahoo Finance</div>", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("Search Stock")

stocks = {
    "Apple":"AAPL",
    "Microsoft":"MSFT",
    "Tesla":"TSLA",
    "NVIDIA":"NVDA",
    "Amazon":"AMZN",
    "Google":"GOOG",
    "Meta":"META",
    "Reliance":"RELIANCE.NS",
    "TCS":"TCS.NS",
    "Infosys":"INFY.NS",
    "HDFC Bank":"HDFCBANK.NS",
    "ICICI Bank":"ICICIBANK.NS",
    "State Bank of India":"SBIN.NS"
}

selected = st.sidebar.selectbox(
    "Popular Stocks",
    list(stocks.keys())
)

ticker = st.sidebar.text_input(
    "Or Enter Stock Symbol",
    value=stocks[selected]
).upper()

period = st.sidebar.selectbox(
    "Select Time Period",
    [
        "1d",
        "5d",
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "max"
    ]
)

st.sidebar.markdown("---")

refresh = st.sidebar.button("🔄 Refresh Data")

# -----------------------------
# FETCH DATA
# -----------------------------

with st.spinner("Fetching Live Data..."):

    stock = yf.Ticker(ticker)

    history = stock.history(period=period)

    info = stock.info

if history.empty:
    st.error("Invalid ticker or no data available.")
    st.stop()

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="📈 Yahoo Finance Dashboard",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.metric-box{
    background:#1E1E1E;
    padding:20px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 0px 10px rgba(255,255,255,0.05);
}

.title{
    text-align:center;
    color:#00FFAA;
    font-size:40px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:gray;
    margin-bottom:30px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------

st.markdown("<div class='title'>📈 Live Stock Market Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Powered by Yahoo Finance</div>", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("Search Stock")

stocks = {
    "Apple":"AAPL",
    "Microsoft":"MSFT",
    "Tesla":"TSLA",
    "NVIDIA":"NVDA",
    "Amazon":"AMZN",
    "Google":"GOOG",
    "Meta":"META",
    "Reliance":"RELIANCE.NS",
    "TCS":"TCS.NS",
    "Infosys":"INFY.NS",
    "HDFC Bank":"HDFCBANK.NS",
    "ICICI Bank":"ICICIBANK.NS",
    "State Bank of India":"SBIN.NS"
}

selected = st.sidebar.selectbox(
    "Popular Stocks",
    list(stocks.keys())
)

ticker = st.sidebar.text_input(
    "Or Enter Stock Symbol",
    value=stocks[selected]
).upper()

period = st.sidebar.selectbox(
    "Select Time Period",
    [
        "1d",
        "5d",
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "max"
    ]
)

st.sidebar.markdown("---")

refresh = st.sidebar.button("🔄 Refresh Data")

# -----------------------------
# FETCH DATA
# -----------------------------

with st.spinner("Fetching Live Data..."):

    stock = yf.Ticker(ticker)

    history = stock.history(period=period)

    info = stock.info

if history.empty:
    st.error("Invalid ticker or no data available.")
    st.stop()

# -----------------------------
# INTERACTIVE STOCK CHART
# -----------------------------

st.write("")
st.subheader("📈 Stock Price Chart")

fig = go.Figure()

# Closing Price
fig.add_trace(
    go.Scatter(
        x=history.index,
        y=history["Close"],
        mode="lines",
        name="Close Price",
        line=dict(color="#00CC96", width=3)
    )
)

# 20-Day Moving Average
if history["MA20"].notna().sum() > 0:
    fig.add_trace(
        go.Scatter(
            x=history.index,
            y=history["MA20"],
            mode="lines",
            name="20-Day MA",
            line=dict(color="orange", width=2)
        )
    )

# 50-Day Moving Average
if history["MA50"].notna().sum() > 0:
    fig.add_trace(
        go.Scatter(
            x=history.index,
            y=history["MA50"],
            mode="lines",
            name="50-Day MA",
            line=dict(color="red", width=2)
        )
    )

fig.update_layout(
    template="plotly_dark",
    height=600,
    xaxis_title="Date",
    yaxis_title="Price",
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig, use_container_width=True)


# -----------------------------
# HISTORICAL DATA
# -----------------------------

st.write("")
st.subheader("📋 Historical Data")

st.dataframe(
    history[["Open", "High", "Low", "Close", "Volume"]].tail(15),
    use_container_width=True
)


# -----------------------------
# DOWNLOAD CSV
# -----------------------------

csv = history.to_csv().encode("utf-8")

st.download_button(
    label="⬇ Download Historical Data",
    data=csv,
    file_name=f"{ticker}_history.csv",
    mime="text/csv"
)


# -----------------------------
# COMPANY INFORMATION
# -----------------------------

st.write("")
st.subheader("🏢 Company Information")

col1, col2 = st.columns(2)

with col1:
    st.write("**Company Name:**", info.get("longName", "N/A"))
    st.write("**Sector:**", info.get("sector", "N/A"))
    st.write("**Industry:**", info.get("industry", "N/A"))
    st.write("**Country:**", info.get("country", "N/A"))
    st.write("**Employees:**", info.get("fullTimeEmployees", "N/A"))

with col2:
    st.write("**Website:**", info.get("website", "N/A"))
    st.write("**Currency:**", info.get("currency", "N/A"))
    st.write("**Exchange:**", info.get("exchange", "N/A"))
    st.write("**P/E Ratio:**", info.get("trailingPE", "N/A"))
    st.write("**Dividend Yield:**", info.get("dividendYield", "N/A"))


# -----------------------------
# BUSINESS SUMMARY
# -----------------------------

summary = info.get("longBusinessSummary", "")

if summary:
    st.write("")
    st.subheader("📖 Business Summary")
    st.write(summary)


# -----------------------------
# LAST UPDATED
# -----------------------------

st.write("---")

st.caption(
    f"Last Updated: {datetime.now().strftime('%d %B %Y, %I:%M:%S %p')}"
)

st.caption("📊 Data Source: Yahoo Finance (yfinance)")
