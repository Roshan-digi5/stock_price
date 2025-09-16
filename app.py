import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# --- Page Config ---
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- Stock Data ---
stock_data = {
    '^NSEI': 'Nifty 50 Index', '20MICRONS.NS': '20 Microns Limited', 
    '21STCENMGM.NS': '21st Century Management Services Limited',
    '3IINFOTECH.NS': '3i Infotech Limited', '3MINDIA.NS': '3M India Limited',
    # Add rest of your stocks...
}

# --- Sidebar ---
st.sidebar.title("Stock Analysis Dashboard")
st.sidebar.markdown("Select time period for analysis:")

period_options = {
    "1 Year": 365,
    "2 Years": 730,
    "3 Years": 1095,
    "5 Years": 1825
}
selected_period = st.sidebar.selectbox(
    "Select time period:",
    options=list(period_options.keys()),
    index=2  # Default to 3 Years
)

# --- Date Calculation ---
end_date = datetime.today()
start_date = end_date - timedelta(days=period_options[selected_period])

# --- Fetch Stock Data ---
@st.cache_data(ttl=3600)
def get_stock_data(symbols, start_date, end_date):
    summary_data = []

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(start=start_date, end=end_date)

            if df.empty:
                continue

            # Resample monthly
            monthly_close = df['Close'].resample('ME').last().dropna()
            monthly_pct_change = monthly_close.pct_change() * 100
            monthly_pct_change = monthly_pct_change.fillna(0)

            company = stock_data.get(symbol, "N/A")

            if len(monthly_pct_change) > 1:
                valid_returns = monthly_pct_change.iloc[1:]
                summary_data.append({
                    'Company': company,
                    'Avg Monthly Change (%)': round(valid_returns.mean(), 2),
                    'Volatility (Std Dev)': round(valid_returns.std(), 2),
                    'Highest Monthly Change (%)': round(valid_returns.max(), 2),
                    'Lowest Monthly Change (%)': round(valid_returns.min(), 2),
                    'Months of Data': len(monthly_pct_change)
                })
            else:
                summary_data.append({
                    'Company': company,
                    'Avg Monthly Change (%)': 0,
                    'Volatility (Std Dev)': 0,
                    'Highest Monthly Change (%)': 0,
                    'Lowest Monthly Change (%)': 0,
                    'Months of Data': len(monthly_pct_change)
                })

        except Exception as e:
            st.error(f"Error fetching data for {stock_data.get(symbol)}: {str(e)}")

    summary_df = pd.DataFrame(summary_data) if summary_data else pd.DataFrame()
    return summary_df

# --- Main ---
st.title("Stock Monthly Performance Analysis")
st.markdown(f"Analysis from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

with st.spinner("Downloading stock data..."):
    summary_df = get_stock_data(list(stock_data.keys()), start_date, end_date)

if summary_df.empty:
    st.error("Failed to fetch data for the selected companies.")
else:
    # Display only summary table
    st.subheader("Summary Statistics of All Stocks")
    st.dataframe(summary_df.sort_values(by='Avg Monthly Change (%)', ascending=False), use_container_width=True)
