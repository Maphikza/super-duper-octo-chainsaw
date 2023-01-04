import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf

st.set_page_config(page_title="Stock Charts Test", layout="wide", initial_sidebar_state="auto")
st.header('S&P 500')
ticker_names = ['A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACGL', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP',
                'ADSK', 'AEE', 'AEP', 'AES', 'AFL', 'AIG', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE',
                'AMAT', 'AMCR', 'AMD', 'AME', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 'ANSS', 'AON', 'AOS', 'APA', 'APD',
                'APH', 'APTV', 'ARE', 'ATO', 'ATVI', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXP', 'AZO', 'BA', 'BAC', 'BALL',
                'BAX', 'BBWI', 'BBY', 'BDX', 'BEN', 'BF.B', 'BIIB', 'BIO', 'BK', 'BKNG', 'BKR', 'BLK', 'BMY', 'BR',
                'BRK.B', 'BRO', 'BSX', 'BWA', 'BXP', 'C', 'CAG', 'CAH', 'CARR', 'CAT', 'CB', 'CBOE', 'CBRE', 'CCI',
                'CCL', 'CDAY', 'CDNS', 'CDW', 'CE', 'CEG', 'CF', 'CFG', 'CHD', 'CHRW', 'CHTR', 'CI', 'CINF', 'CL',
                'CLX', 'CMA', 'CMCSA', 'CME', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COO', 'COP', 'COST', 'CPB',
                'CPRT', 'CPT', 'CRL', 'CRM', 'CSCO', 'CSGP', 'CSX', 'CTAS', 'CTLT', 'CTRA', 'CTSH', 'CTVA', 'CVS',
                'CVX', 'CZR', 'D', 'DAL', 'DD', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DISH', 'DLR', 'DLTR',
                'DOV', 'DOW', 'DPZ', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN', 'DXC', 'DXCM', 'EA', 'EBAY', 'ECL', 'ED', 'EFX',
                'EIX', 'EL', 'ELV', 'EMN', 'EMR', 'ENPH', 'EOG', 'EPAM', 'EQIX', 'EQR', 'EQT', 'ES', 'ESS', 'ETN',
                'ETR', 'ETSY', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FANG', 'FAST', 'FBHS', 'FCX', 'FDS',
                'FDX', 'FE', 'FFIV', 'FIS', 'FISV', 'FITB', 'FLT', 'FMC', 'FOX', 'FOXA', 'FRC', 'FRT', 'FTNT', 'FTV',
                'GD', 'GE', 'GEN', 'GILD', 'GIS', 'GL', 'GLW', 'GM', 'GNRC', 'GOOG', 'GOOGL', 'GPC', 'GPN', 'GRMN',
                'GS', 'GWW', 'HAL', 'HAS', 'HBAN', 'HCA', 'HD', 'HES', 'HIG', 'HII', 'HLT', 'HOLX', 'HON', 'HPE', 'HPQ',
                'HRL', 'HSIC', 'HST', 'HSY', 'HUM', 'HWM', 'IBM', 'ICE', 'IDXX', 'IEX', 'IFF', 'ILMN', 'INCY', 'INTC',
                'INTU', 'INVH', 'IP', 'IPG', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW', 'IVZ', 'J', 'JBHT', 'JCI', 'JKHY',
                'JNJ', 'JNPR', 'JPM', 'K', 'KDP', 'KEY', 'KEYS', 'KHC', 'KIM', 'KLAC', 'KMB', 'KMI', 'KMX', 'KO', 'KR',
                'L', 'LDOS', 'LEN', 'LH', 'LHX', 'LIN', 'LKQ', 'LLY', 'LMT', 'LNC', 'LNT', 'LOW', 'LRCX', 'LUMN', 'LUV',
                'LVS', 'LW', 'LYB', 'LYV', 'MA', 'MAA', 'MAR', 'MAS', 'MCD', 'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET',
                'META', 'MGM', 'MHK', 'MKC', 'MKTX', 'MLM', 'MMC', 'MMM', 'MNST', 'MO', 'MOH', 'MOS', 'MPC', 'MPWR',
                'MRNA', 'MRO', 'MS', 'MSCI', 'MSFT', 'MSI', 'MTB', 'MTCH', 'MTD', 'MU', 'NCLH', 'NDAQ', 'NDSN', 'NEE',
                'NEM', 'NFLX', 'NI', 'NKE', 'NOC', 'NOW', 'NRG', 'NSC', 'NTAP', 'NTRS', 'NUE', 'NVDA', 'NVR', 'NWL',
                'NWS', 'NWSA', 'NXPI', 'O', 'ODFL', 'OGN', 'OKE', 'OMC', 'ON', 'ORCL', 'ORLY', 'OTIS', 'OXY', 'PARA',
                'PAYC', 'PAYX', 'PCAR', 'PCG', 'PEAK', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKG',
                'PKI', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'POOL', 'PPG', 'PPL', 'PRU', 'PSA', 'PSX', 'PTC', 'PWR', 'PXD',
                'PYPL', 'QCOM', 'QRVO', 'RCL', 'RE', 'REG', 'REGN', 'RF', 'RHI', 'RJF', 'RL', 'RMD', 'ROK', 'ROL',
                'ROP', 'ROST', 'RSG', 'RTX', 'SBAC', 'SBNY', 'SBUX', 'SCHW', 'SEDG', 'SEE', 'SHW', 'SIVB', 'SJM', 'SLB',
                'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SRE', 'STE', 'STT', 'STX', 'STZ', 'SWK', 'SWKS', 'SYF', 'SYK',
                'SYY', 'T', 'TAP', 'TDG', 'TDY', 'TECH', 'TEL', 'TER', 'TFC', 'TFX', 'TGT', 'TJX', 'TMO', 'TMUS', 'TPR',
                'TRGP', 'TRMB', 'TROW', 'TRV', 'TSCO', 'TSLA', 'TSN', 'TT', 'TTWO', 'TXN', 'TXT', 'TYL', 'UAL', 'UDR',
                'UHS', 'ULTA', 'UNH', 'UNP', 'UPS', 'URI', 'USB', 'V', 'VFC', 'VICI', 'VLO', 'VMC', 'VNO', 'VRSK',
                'VRSN', 'VRTX', 'VTR', 'VTRS', 'VZ', 'WAB', 'WAT', 'WBA', 'WBD', 'WDC', 'WEC', 'WELL', 'WFC', 'WHR',
                'WM', 'WMB', 'WMT', 'WRB', 'WRK', 'WST', 'WTW', 'WY', 'WYNN', 'XEL', 'XOM', 'XRAY', 'XYL', 'YUM', 'ZBH',
                'ZBRA', 'ZION', 'ZTS']

set_ticker_names = " ".join(ticker_names)
tickers = yf.Tickers(set_ticker_names)


def change_ticker():
    st.session_state["data"] = current_ticker(st.session_state.period)


def current_ticker(entry):
    return yf.Ticker(st.session_state.ticker).history(period=entry).reset_index().sort_values(by="Date",
                                                                                              ascending=False)


if "ticker" not in st.session_state:
    st.session_state["ticker"] = 'A'

if "period" not in st.session_state:
    st.session_state["period"] = "max"

if "data" not in st.session_state:
    st.session_state["data"] = current_ticker(st.session_state.period)


def all_time():
    st.session_state["period"] = "max"
    st.session_state["data"] = current_ticker(st.session_state.period)


def ten_years_to_date():
    st.session_state["period"] = "10y"
    st.session_state["data"] = current_ticker(st.session_state.period)


def five_years_to_date():
    st.session_state["period"] = "5y"
    st.session_state["data"] = current_ticker(st.session_state.period)


def two_years_to_date():
    st.session_state["period"] = "2y"
    st.session_state["data"] = current_ticker(st.session_state.period)


def one_year_to_date():
    st.session_state["period"] = "1y"
    st.session_state["data"] = current_ticker(st.session_state.period)


def six_months_to_date():
    st.session_state["period"] = "6mo"
    st.session_state["data"] = current_ticker(st.session_state.period)


def three_months_to_date():
    st.session_state["period"] = "3mo"
    st.session_state["data"] = current_ticker(st.session_state.period)


def month_to_date():
    st.session_state["period"] = "1mo"
    st.session_state["data"] = current_ticker(st.session_state.period)


def five_days_to_date():
    st.session_state["period"] = "5d"
    st.session_state["data"] = current_ticker(st.session_state.period)


def one_day_to_date():
    st.session_state["period"] = "1d"
    st.session_state["data"] = current_ticker(st.session_state.period)


@st.cache
def latest_news():
    return st.session_state["news"]


col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with st.sidebar:
    st.session_state["ticker"] = st.selectbox("Stock Tickers", tuple(ticker_names))
    timeframe = st.selectbox("Analysis Timeframe", (
        "Maximum Dates", "10 years to date", "5 years to date", "2 Years to date", "1 year to date", "6 Months to date",
        "3 Months to date", "1 Month to date", "5 days to date", "1 day to date"))
    if timeframe == "Maximum Dates":
        all_time()
    elif timeframe == "10 years to date":
        ten_years_to_date()
    elif timeframe == "5 years to date":
        five_years_to_date()
    elif timeframe == "2 Years to date":
        two_years_to_date()
    elif timeframe == "1 year to date":
        one_year_to_date()
    elif timeframe == "6 Months to date":
        six_months_to_date()
    elif timeframe == "3 Months to date":
        three_months_to_date()
    elif timeframe == "1 Month to date":
        month_to_date()
    elif timeframe == "5 days to date":
        five_days_to_date()
    elif timeframe == "1 day to date":
        one_day_to_date()
    else:
        all_time()
    if "news" in st.session_state:
        news_list = latest_news()
        with st.expander("News".upper()):
            for story in news_list:
                st.markdown(f"<br>{story.get('title')}", unsafe_allow_html=True)
                st.markdown(f"{story.get('publisher')}")
                st.markdown(f"<a href='{story.get('link')}'>{story.get('title')[:20]}</a>", unsafe_allow_html=True)


@st.cache
def full_data():
    ticker_ = yf.Ticker(st.session_state.ticker)
    ticker_history = ticker_.history(period=st.session_state.period)
    ticker_actions = ticker_.actions
    institution_share_holders = ticker_.institutional_holders
    news = ticker_.news
    if "news" not in st.session_state:
        st.session_state["news"] = news

    return ticker_history, ticker_actions, institution_share_holders, news


history, actions, institutional_holders, current_news = full_data()

with col1:
    fig_history = go.Figure(data=[go.Ohlc(x=history.index,
                                          open=history['Open'], high=history['High'],
                                          low=history['Low'], close=history['Close'])
                                  ])

    fig_history.update_layout(xaxis_rangeslider_visible=False, height=500, template="plotly_white",
                              title=f"({st.session_state.ticker}) Stock Price Movement")
    st.plotly_chart(fig_history, theme="streamlit", use_container_width=True)

with col2:
    fig_volumes = px.line(history, x=history.index, y=["Volume"], height=500,
                          title=f"({st.session_state.ticker}) Volume",
                          labels={"value": "Volume"},
                          template="plotly_white")
    st.plotly_chart(fig_volumes, use_container_width=True)

with col3:
    fig_dividends = px.line(actions, x=actions.index, y="Dividends", title=f"({st.session_state.ticker}) Dividends")
    st.plotly_chart(fig_dividends, theme="streamlit", use_container_width=True)

with col4:
    fig_stock_splits = px.line(actions, x=actions.index, y="Stock Splits",
                               title=f"({st.session_state.ticker}) Stock Splits")
    st.plotly_chart(fig_stock_splits, theme="streamlit", use_container_width=True)

with st.expander("Institutional Holders"):
    institute_data = institutional_holders
    st.dataframe(institute_data[["Holder", "Shares", "Date Reported", "% Out", "Value"]], width=1400)

with st.expander("Numbers Table"):
    data = history.reset_index().sort_values(by="Date", ascending=False)
    st.dataframe(data[["Date", "Open", "High", "Low", "Close", "Volume"]], width=1400)
