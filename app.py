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
    'RELIANCE.NS': 'Reliance Industries Limited',
    'HDFCBANK.NS': 'HDFC Bank Limited',
    'BHARTIARTL.NS': 'Bharti Airtel Limited',
    'TCS.NS': 'Tata Consultancy Services Limited',
    'ICICIBANK.NS': 'ICICI Bank Limited',
    'SBIN.NS': 'State Bank of India',
    'BAJFINANCE.NS': 'Bajaj Finance Limited',
    'INFY.NS': 'Infosys Limited',
    'HINDUNILVR.NS': 'Hindustan Unilever Limited',
    'ITC.NS': 'ITC Limited',
    'LT.NS': 'Larsen & Toubro Limited',
    'MARUTI.NS': 'Maruti Suzuki India Limited',
    'M&M.NS': 'Mahindra & Mahindra Limited',
    'HCLTECH.NS': 'HCL Technologies Limited',
    'KOTAKBANK.NS': 'Kotak Mahindra Bank Limited',
    'AXISBANK.NS': 'Axis Bank Limited',
    'TITAN.NS': 'Titan Company Limited',
    'NTPC.NS': 'NTPC Limited',
    'ULTRACEMCO.NS': 'UltraTech Cement Limited',
    'SUNPHARMA.NS': 'Sun Pharmaceutical Industries Limited',
    'TATAMOTORS.NS': 'Tata Motors Limited',
    'POWERGRID.NS': 'Power Grid Corporation of India Limited',
    'BAJAJ-AUTO.NS': 'Bajaj Auto Limited',
    'ASIANPAINT.NS': 'Asian Paints Limited',
    'INDUSINDBK.NS': 'IndusInd Bank Limited',
    'TATACONSUM.NS': 'Tata Consumer Products Limited',
    'DIVISLAB.NS': 'Divi\'s Laboratories Limited',
    'DRREDDY.NS': 'Dr. Reddy\'s Laboratories Limited',
    'WIPRO.NS': 'Wipro Limited',
    'COALINDIA.NS': 'Coal India Limited',
    'IOC.NS': 'Indian Oil Corporation Limited',
    'EICHERMOT.NS': 'Eicher Motors Limited',
    'HEROMOTOCO.NS': 'Hero MotoCorp Limited',
    'SHREECEM.NS': 'Shree Cement Limited',
    'BRITANNIA.NS': 'Britannia Industries Limited',
    'CIPLA.NS': 'Cipla Limited',
    'UPL.NS': 'UPL Limited',
    'GRASIM.NS': 'Grasim Industries Limited',
    'ADANIGREEN.NS': 'Adani Green Energy Limited',
    'ADANIPORTS.NS': 'Adani Ports and Special Economic Zone Limited',
    'ADANIPOWER.NS': 'Adani Power Limited',
    'ADANITRANS.NS': 'Adani Transmission Limited',
    'NTPCGREEN.NS': 'NTPC Green Energy Limited',
    'NCC.NS': 'NCC Limited',
    'WIPRO.NS': 'Wipro Limited',
    'INFIBEAM.NS': 'Infibeam Avenues Limited',
    'HAVELLS.NS': 'Havells India Limited',
    'MOTHERSUMI.NS': 'Motherson Sumi Systems Limited',
    'MUTHOOTFIN.NS': 'Muthoot Finance Limited',
    'RECLTD.NS': 'Rural Electrification Corporation Limited',
    'HINDALCO.NS': 'Hindalco Industries Limited',
    'TATAPOWER.NS': 'Tata Power Company Limited',
    'JSWSTEEL.NS': 'JSW Steel Limited',
    'VEDL.NS': 'Vedanta Limited',
    'TATACHEM.NS': 'Tata Chemicals Limited',
    'TATAMETALI.NS': 'Tata Metaliks Limited',
    'ZEELEARN.NS': 'Zee Learn Limited',
    'INDIACEM.NS': 'The India Cements Limited',
    'JUBLFOOD.NS': 'Jubilant FoodWorks Limited',
    'MCDOWELL-N.NS': 'McDowell Holdings Limited',
    'RELIANCE.NS': 'Reliance Industries Limited',
    'HDFCBANK.NS': 'HDFC Bank Limited',
    'BHARTIARTL.NS': 'Bharti Airtel Limited',
    'TCS.NS': 'Tata Consultancy Services Limited',
    'ICICIBANK.NS': 'ICICI Bank Limited',
    'SBIN.NS': 'State Bank of India',
    'BAJFINANCE.NS': 'Bajaj Finance Limited',
    'INFY.NS': 'Infosys Limited',
    'HINDUNILVR.NS': 'Hindustan Unilever Limited',
    'ITC.NS': 'ITC Limited',
    'LT.NS': 'Larsen & Toubro Limited',
    'MARUTI.NS': 'Maruti Suzuki India Limited',
    'M&M.NS': 'Mahindra & Mahindra Limited',
    'HCLTECH.NS': 'HCL Technologies Limited',
    'KOTAKBANK.NS': 'Kotak Mahindra Bank Limited',
    'AXISBANK.NS': 'Axis Bank Limited',
    'TITAN.NS': 'Titan Company Limited',
    'NTPC.NS': 'NTPC Limited',
    'ULTRACEMCO.NS': 'UltraTech Cement Limited',
    'SUNPHARMA.NS': 'Sun Pharmaceutical Industries Limited',
    'TATAMOTORS.NS': 'Tata Motors Limited',
    'POWERGRID.NS': 'Power Grid Corporation of India Limited',
    'BAJAJ-AUTO.NS': 'Bajaj Auto Limited',
    'ASIANPAINT.NS': 'Asian Paints Limited',
    'INDUSINDBK.NS': 'IndusInd Bank Limited',
    'TATACONSUM.NS': 'Tata Consumer Products Limited',
    'DIVISLAB.NS': 'Divi\'s Laboratories Limited',
    'DRREDDY.NS': 'Dr. Reddy\'s Laboratories Limited',
    'WIPRO.NS': 'Wipro Limited',
    'COALINDIA.NS': 'Coal India Limited',
    'IOC.NS': 'Indian Oil Corporation Limited',
    'EICHERMOT.NS': 'Eicher Motors Limited',
    'HEROMOTOCO.NS': 'Hero MotoCorp Limited',
    'SHREECEM.NS': 'Shree Cement Limited',
    'BRITANNIA.NS': 'Britannia Industries Limited',
    'CIPLA.NS': 'Cipla Limited',
    'UPL.NS': 'UPL Limited',
    'GRASIM.NS': 'Grasim Industries Limited',
    'ADANIGREEN.NS': 'Adani Green Energy Limited',
    'ADANIPORTS.NS': 'Adani Ports and Special Economic Zone Limited',
    'ADANIPOWER.NS': 'Adani Power Limited',
    'ADANITRANS.NS': 'Adani Transmission Limited',
    'NTPCGREEN.NS': 'NTPC Green Energy Limited',
    'NCC.NS': 'NCC Limited',
    'WIPRO.NS': 'Wipro Limited',
    'INFIBEAM.NS': 'Infibeam Avenues Limited',
    'HAVELLS.NS': 'Havells India Limited',
    'MOTHERSUMI.NS': 'Motherson Sumi Systems Limited',
    'MUTHOOTFIN.NS': 'Muthoot Finance Limited',
    'RECLTD.NS': 'Rural Electrification Corporation Limited',
    'HINDALCO.NS': 'Hindalco Industries Limited',
    'TATAPOWER.NS': 'Tata Power Company Limited',
    'JSWSTEEL.NS': 'JSW Steel Limited',
    'VEDL.NS': 'Vedanta Limited',
    'TATACHEM.NS': 'Tata Chemicals Limited',
    'TATAMETALI.NS': 'Tata Metaliks Limited',
    'ZEELEARN.NS': 'Zee Learn Limited',
    'INDIACEM.NS': 'The India Cements Limited',
    'JUBLFOOD.NS': 'Jubilant FoodWorks Limited',
    'MCDOWELL-N.NS': 'McDowell Holdings Limited',
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

