import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

# NSE tickers with company names
stock_data = {
    '^NSEI': 'Nifty 50 Index',
    'BEL.NS': 'Bharat Electronics Ltd',
    'BAJFINANCE.NS': 'Bajaj Finance Ltd',
    'HINDALCO.NS': 'Hindalco Industries Ltd',
    'SHRIRAMFIN.NS': 'Shriram Finance Ltd',
    'BAJAJFINSV.NS': 'Bajaj Finserv Ltd',
    'AXISBANK.NS': 'Axis Bank Ltd',
    'EICHERMOT.NS': 'Eicher Motors Ltd',
    'MARUTI.NS': 'Maruti Suzuki India Ltd',
    'TATAMOTORS.NS': 'Tata Motors Ltd',
    'INFY.NS': 'Infosys Ltd',
    'DRREDDY.NS': "Dr. Reddy's Laboratories Ltd",
    'LT.NS': 'Larsen & Toubro Ltd',
    'ICICIBANK.NS': 'ICICI Bank Ltd',
    'RELIANCE.NS': 'Reliance Industries Ltd',
    'SBILIFE.NS': 'SBI Life Insurance Company Ltd',
    'CIPLA.NS': 'Cipla Ltd',
    'HDFCLIFE.NS': 'HDFC Life Insurance Company Ltd',
    'SUNPHARMA.NS': 'Sun Pharmaceutical Industries Ltd',
    'COALINDIA.NS': 'Coal India Ltd',
    'TCS.NS': 'Tata Consultancy Services Ltd',
    'TATASTEEL.NS': 'Tata Steel Ltd',
    'TECHM.NS': 'Tech Mahindra Ltd',
    'GRASIM.NS': 'Grasim Industries Ltd',
    'ADANIPORTS.NS': 'Adani Ports and Special Economic Zone Ltd',
    'POWERGRID.NS': 'Power Grid Corporation of India Ltd',
    'NTPC.NS': 'NTPC Ltd',
    'SBIN.NS': 'State Bank of India',
    'JSWSTEEL.NS': 'JSW Steel Ltd',
    'ONGC.NS': 'Oil and Natural Gas Corporation Ltd',
    'APOLLOHOSP.NS': 'Apollo Hospitals Enterprise Ltd',
    'HCLTECH.NS': 'HCL Technologies Ltd',
    'HEROMOTOCO.NS': 'Hero MotoCorp Ltd',
    'ITC.NS': 'ITC Ltd',
    'ADANIENT.NS': 'Adani Enterprises Ltd',
    'M&M.NS': 'Mahindra & Mahindra Ltd',
    'HDFCBANK.NS': 'HDFC Bank Ltd',
    'BHARTIARTL.NS': 'Bharti Airtel Ltd',
    'KOTAKBANK.NS': 'Kotak Mahindra Bank Ltd',
    'ASIANPAINT.NS': 'Asian Paints Ltd',
    'TITAN.NS': 'Titan Company Ltd',
    'ULTRACEMCO.NS': 'UltraTech Cement Ltd',
    'NESTLEIND.NS': 'Nestle India Ltd',
    'TRENT.NS': 'Trent Ltd',
    'INDUSINDBK.NS': 'IndusInd Bank Ltd',
    'TATACONSUM.NS': 'Tata Consumer Products Ltd',
    'WIPRO.NS': 'Wipro Ltd',
    'BAJAJ-AUTO.NS': 'Bajaj Auto Ltd',
    'HINDUNILVR.NS': 'Hindustan Unilever Ltd'
}

# Sidebar
st.sidebar.title("Stock Analysis Dashboard")
st.sidebar.markdown("Select stocks to analyze monthly performance")

# Multi-select (only company names shown)
selected_companies = st.sidebar.multiselect(
    "Select companies:",
    options=list(stock_data.values())  # Only names
)

# Map back to tickers
selected_symbols = [k for k, v in stock_data.items() if v in selected_companies]

# Time period selection
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

# Date calculation
end_date = datetime.today()
start_date = end_date - timedelta(days=period_options[selected_period])

# Download and process data
@st.cache_data(ttl=3600)
def get_stock_data(symbols, start_date, end_date):
    all_monthly_data = []
    summary_data = []

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(start=start_date, end=end_date)

            if df.empty:
                st.warning(f"No data available for {stock_data.get(symbol)}")
                continue

            # Resample to monthly Open & Close
            monthly_open = df['Open'].resample('ME').first().dropna()
            monthly_close = df['Close'].resample('ME').last().dropna()
            monthly_pct_change = monthly_close.pct_change() * 100
            monthly_pct_change = monthly_pct_change.fillna(0)

            company = stock_data.get(symbol, "N/A")

            monthly_data = pd.DataFrame({
                'Date': monthly_close.index,
                'Company': company,
                'Open': monthly_open.values,
                'Close': monthly_close.values,
                'Monthly Change (%)': monthly_pct_change.values
            })
            all_monthly_data.append(monthly_data)

            # Summary stats
            if len(monthly_pct_change) > 1:
                valid_returns = monthly_pct_change.iloc[1:]
                avg_return = valid_returns.mean()
                volatility = valid_returns.std()
                months_count = len(monthly_pct_change)

                summary_data.append({
                    'Company': company,
                    'Avg Monthly Change (%)': avg_return,
                    'Volatility (Std Dev)': volatility,
                    'Months of Data': months_count
                })
            else:
                summary_data.append({
                    'Company': company,
                    'Avg Monthly Change (%)': 0,
                    'Volatility (Std Dev)': 0,
                    'Months of Data': len(monthly_pct_change)
                })

        except Exception as e:
            st.error(f"Error fetching data for {stock_data.get(symbol)}: {str(e)}")

    monthly_df = pd.concat(all_monthly_data, ignore_index=True) if all_monthly_data else pd.DataFrame()
    summary_df = pd.DataFrame(summary_data) if summary_data else pd.DataFrame()

    return monthly_df, summary_df

# Main content
st.title("Stock Monthly Performance Analysis")

if not selected_symbols:
    st.warning("Please select at least one company from the sidebar.")
else:
    st.markdown(f"Analysis from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

    with st.spinner("Downloading stock data..."):
        monthly_df, summary_df = get_stock_data(selected_symbols, start_date, end_date)

    if monthly_df.empty:
        st.error("Failed to fetch data for the selected companies. Please try different ones.")
    else:
        # Summary table
        st.subheader("Summary Statistics")
        if not summary_df.empty:
            summary_display = summary_df.copy()
            summary_display['Avg Monthly Change (%)'] = summary_display['Avg Monthly Change (%)'].round(2)
            summary_display['Volatility (Std Dev)'] = summary_display['Volatility (Std Dev)'].round(2)
            st.dataframe(summary_display, use_container_width=True)
        else:
            st.info("No summary data available.")

        # Monthly table
        st.subheader("Monthly Performance Data")
        monthly_display = monthly_df.copy()
        monthly_display['Open'] = monthly_display['Open'].round(2)
        monthly_display['Close'] = monthly_display['Close'].round(2)
        monthly_display['Monthly Change (%)'] = monthly_display['Monthly Change (%)'].round(2)
        monthly_display['Date'] = monthly_display['Date'].dt.strftime('%Y-%m-%d')
        st.dataframe(monthly_display[['Date', 'Company', 'Open', 'Close', 'Monthly Change (%)']],
                     use_container_width=True)

        # Quick insights
        st.subheader("Quick Insights")
        if not summary_df.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                best_stock = summary_df.loc[summary_df['Avg Monthly Change (%)'].idxmax()]
                st.metric("Best Avg Return",
                          f"{best_stock['Avg Monthly Change (%)']:.2f}%",
                          best_stock['Company'])
            with col2:
                worst_stock = summary_df.loc[summary_df['Avg Monthly Change (%)'].idxmin()]
                st.metric("Worst Avg Return",
                          f"{worst_stock['Avg Monthly Change (%)']:.2f}%",
                          worst_stock['Company'])
            with col3:
                total_months = monthly_df['Company'].value_counts().max()
                st.metric("Months Analyzed", total_months)
