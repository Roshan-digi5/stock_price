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
    "ABB.NS": "ABB",
    "ABCAPITAL.NS": "Aditya Birla Capital",
    "ADANIENSOL.NS": "Adani Energy Solutions",
    "ADANIENT.NS": "Adani Enterprises",
    "ADANIGREEN.NS": "Adani Green Energy",
    "ADANIPORTS.NS": "Adani Ports & SEZ",
    "ALKEM.NS": "Alkem Laboratories",
    "AMBER.NS": "Amber Enterprises",
    "AMBUJACEM.NS": "Ambuja Cements",
    "ANGELONE.NS": "Angel One",
    "APLAPOLLO.NS": "APL Apollo Tubes",
    "APOLLOHOSP.NS": "Apollo Hospitals",
    "ASHOKLEY.NS": "Ashok Leyland",
    "ASIANPAINT.NS": "Asian Paints",
    "ASTRAL.NS": "Astral",
    "AUBANK.NS": "AU Small Finance Bank",
    "AUROPHARMA.NS": "Aurobindo Pharma",
    "AXISBANK.NS": "Axis Bank",
    "BAJAJ-AUTO.NS": "Bajaj Auto",
    "BAJAJFINSV.NS": "Bajaj Finserv",
    "BAJFINANCE.NS": "Bajaj Finance",
    "BANDHANBNK.NS": "Bandhan Bank",
    "BANKBARODA.NS": "Bank of Baroda",
    "BANKINDIA.NS": "Bank of India",
    "BDL.NS": "Bharat Dynamics",
    "BEL.NS": "Bharat Electronics",
    "BHARATFORG.NS": "Bharat Forge",
    "BHARTIARTL.NS": "Bharti Airtel",
    "BHEL.NS": "Bharat Heavy Electricals",
    "BIOCON.NS": "Biocon",
    "BLUESTARCO.NS": "Blue Star",
    "BOSCHLTD.NS": "Bosch",
    "BPCL.NS": "Bharat Petroleum",
    "BRITANNIA.NS": "Britannia Industries",
    "BSE.NS": "BSE",
    "CAMS.NS": "Computer Age Management Services",
    "CANBK.NS": "Canara Bank",
    "CDSL.NS": "CDSL",
    "CGPOWER.NS": "CG Power & Industrial Solutions",
    "CHOLAFIN.NS": "Cholamandalam Investment",
    "CIPLA.NS": "Cipla",
    "COALINDIA.NS": "Coal India",
    "COFORGE.NS": "Coforge",
    "COLPAL.NS": "Colgate Palmolive",
    "CONCOR.NS": "Container Corporation of India",
    "CROMPTON.NS": "Crompton Greaves",
    "CUMMINSIND.NS": "Cummins",
    "CYIENT.NS": "Cyient",
    "DABUR.NS": "Dabur India",
    "DALBHARAT.NS": "Dalmia Bharat",
    "DELHIVERY.NS": "Delhivery",
    "DIVISLAB.NS": "Divis Laboratories",
    "DIXON.NS": "Dixon Technologies",
    "DLF.NS": "DLF",
    "DMART.NS": "Avenue Supermarts (DMart)",
    "DRREDDY.NS": "Dr Reddys Laboratories",
    "EICHERMOT.NS": "Eicher Motors",
    "ETERNAL.NS": "Eternal",
    "EXIDEIND.NS": "Exide Industries",
    "FEDERALBNK.NS": "Federal Bank",
    "FORTIS.NS": "Fortis Healthcare",
    "GAIL.NS": "GAIL (India)",
    "GLENMARK.NS": "Glenmark Pharmaceuticals",
    "GMRAIRPORT.NS": "GMR Airports",
    "GODREJCP.NS": "Godrej Consumer Products",
    "GODREJPROP.NS": "Godrej Properties",
    "GRASIM.NS": "Grasim Industries",
    "HAL.NS": "Hindustan Aeronautics",
    "HAVELLS.NS": "Havells",
    "HCLTECH.NS": "HCL Technologies",
    "HDFCAMC.NS": "HDFC AMC",
    "HDFCBANK.NS": "HDFC Bank",
    "HDFCLIFE.NS": "HDFC Life Insurance",
    "HEROMOTOCO.NS": "Hero MotoCorp",
    "HFCL.NS": "HFCL",
    "HINDALCO.NS": "Hindalco Industries",
    "HINDPETRO.NS": "Hindustan Petroleum",
    "HINDUNILVR.NS": "Hindustan Unilever",
    "HINDZINC.NS": "Hindustan Zinc",
    "HUDCO.NS": "HUDCO",
    "ICICIBANK.NS": "ICICI Bank",
    "ICICIGI.NS": "ICICI Lombard General Insurance",
    "ICICIPRULI.NS": "ICICI Prudential Life Insurance",
    "IDEA.NS": "Vodafone Idea (IDEA)",
    "IDFCFIRSTB.NS": "IDFC First Bank",
    "IEX.NS": "Indian Energy Exchange",
    "IGL.NS": "Indraprastha Gas",
    "IIFL.NS": "IIFL Finance",
    "INDHOTEL.NS": "Indian Hotels Company",
    "INDIANB.NS": "Indian Bank",
    "INDIGO.NS": "InterGlobe Aviation (IndiGo)",
    "INDUSINDBK.NS": "IndusInd Bank",
    "INDUSTOWER.NS": "Indus Towers",
    "INFY.NS": "Infosys",
    "INOXWIND.NS": "Inox Wind",
    "IOC.NS": "Indian Oil Corporation",
    "IRCTC.NS": "IRCTC",
    "IREDA.NS": "IREDA",
    "IRFC.NS": "IRFC",
    "ITC.NS": "ITC",
    "JINDALSTEL.NS": "Jindal Steel",
    "JIOFIN.NS": "Jio Financial Services",
    "JSWENERGY.NS": "JSW Energy",
    "JSWSTEEL.NS": "JSW Steel",
    "JUBLFOOD.NS": "Jubilant FoodWorks",
    "KALYANKJIL.NS": "Kalyan Jewellers (KalyanJIL)",
    "KAYNES.NS": "Kaynes Technology India",
    "KEI.NS": "KEI Industries",
    "KFINTECH.NS": "KFin Technologies",
    "KOTAKBANK.NS": "Kotak Mahindra Bank",
    "KPITTECH.NS": "KPIT Technologies",
    "LAURUSLABS.NS": "Laurus Labs",
    "LICHSGFIN.NS": "LIC Housing Finance",
    "LICI.NS": "LIC of India",
    "LODHA.NS": "Lodha Developers",
    "LT.NS": "Larsen & Toubro (L&T)",
    "LTF.NS": "L&T Finance",
    "LTIM.NS": "LTI Mindtree",
    "LUPIN.NS": "Lupin",
    "M&M.NS": "Mahindra & Mahindra",
    "MANAPPURAM.NS": "Manappuram Finance",
    "MANKIND.NS": "Mankind Pharma",
    "MARICO.NS": "Marico",
    "MARUTI.NS": "Maruti Suzuki",
    "MAXHEALTH.NS": "Max Healthcare Institute",
    "MAZDOCK.NS": "Mazagon Dock Shipbuilders",
    "MCX.NS": "MCX",
    "MFSL.NS": "Max Financial Services",
    "MOTHERSON.NS": "Samvardhana Motherson International (Motherson)",
    "MPHASIS.NS": "Mphasis",
    "MUTHOOTFIN.NS": "Muthoot Finance",
    "NATIONALUM.NS": "NALCO (National Aluminium Co.)",
    "NAUKRI.NS": "Info Edge (Naukri)",
    "NBCC.NS": "NBCC",
    "NCC.NS": "NCC",
    "NESTLEIND.NS": "Nestle India",
    "NHPC.NS": "NHPC",
    "NMDC.NS": "NMDC",
    "NTPC.NS": "NTPC",
    "NUVAMA.NS": "Nuvama Wealth Management",
    "NYKAA.NS": "Nykaa",
    "OBEROIRLTY.NS": "Oberoi Realty",
    "OFSS.NS": "Oracle Financial Services Software (OFSS)",
    "OIL.NS": "Oil India",
    "ONGC.NS": "Oil & Natural Gas Corporation (ONGC)",
    "PAGEIND.NS": "Page Industries",
    "PATANJALI.NS": "Patanjali Foods",
    "PAYTM.NS": "One97 Communications (Paytm)",
    "PERSISTENT.NS": "Persistent Systems",
    "PETRONET.NS": "Petronet LNG",
    "PFC.NS": "Power Finance Corporation (PFC)",
    "PGEL.NS": "PG Electroplast",
    "PHOENIXLTD.NS": "Phoenix Mills",
    "PIDILITIND.NS": "Pidilite Industries",
    "PIIND.NS": "PI Industries",
    "PNB.NS": "Punjab National Bank (PNB)",
    "PNBHOUSING.NS": "PNB Housing Finance",
    "POLICYBZR.NS": "PB FinTech (Policybazaar)",
    "POLYCAB.NS": "Polycab India",
    "POWERGRID.NS": "Power Grid Corporation of India",
    "PPLPHARMA.NS": "Piramal Pharma (PPLPHARMA)",
    "PRESTIGE.NS": "Prestige Estates Projects",
    "RBLBANK.NS": "RBL Bank",
    "RECLTD.NS": "REC (Rural Electrification Corporation)",
    "RELIANCE.NS": "Reliance Industries",
    "RVNL.NS": "Rail Vikas Nigam (RVNL)",
    "SAIL.NS": "Steel Authority of India (SAIL)",
    "SAMMAANCAP.NS": "Sammaan Capital",
    "SBICARD.NS": "SBI Cards & Payment Services",
    "SBILIFE.NS": "SBI Life Insurance",
    "SBIN.NS": "State Bank of India (SBI)",
    "SHREECEM.NS": "Shree Cement",
    "SHRIRAMFIN.NS": "Shriram Finance",
    "SIEMENS.NS": "Siemens",
    "SOLARINDS.NS": "Solar Industries",
    "SONACOMS.NS": "Sona BLW Precision Forgings (Sonacoms)",
    "SRF.NS": "SRF",
    "SUNPHARMA.NS": "Sun Pharmaceutical",
    "SUPREMEIND.NS": "Supreme Industries",
    "SUZLON.NS": "Suzlon Energy",
    "SYNGENE.NS": "Syngene International",
    "TATACHEM.NS": "Tata Chemicals",
    "TATACONSUM.NS": "Tata Consumer Products",
    "TATAELXSI.NS": "Tata Elxsi",
    "TATAMOTORS.NS": "Tata Motors",
    "TATAPOWER.NS": "Tata Power",
    "TATASTEEL.NS": "Tata Steel",
    "TATATECH.NS": "Tata Technologies",
    "TCS.NS": "Tata Consultancy Services (TCS)",
    "TECHM.NS": "Tech Mahindra",
    "TIINDIA.NS": "Tube Investments of India (TI India)",
    "TITAGARH.NS": "Titagarh Rail Systems",
    "TITAN.NS": "Titan",
    "TORNTPHARM.NS": "Torrent Pharmaceuticals",
    "TORNTPOWER.NS": "Torrent Power",
    "TRENT.NS": "Trent",
    "TVSMOTOR.NS": "TVS Motor Company",
    "ULTRACEMCO.NS": "UltraTech Cement",
    "UNIONBANK.NS": "Union Bank of India",
    "UNITDSPR.NS": "United Spirits",
    "UNOMINDA.NS": "UNO Minda",
    "UPL.NS": "UPL",
    "VBL.NS": "Varun Beverages",
    "VEDL.NS": "Vedanta",
    "VOLTAS.NS": "Voltas",
    "WIPRO.NS": "Wipro",
    "YESBANK.NS": "Yes Bank",
    "ZYDUSLIFE.NS": "Zydus Life Science"
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



