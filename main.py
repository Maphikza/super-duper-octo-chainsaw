import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd

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


@st.cache
def stock_symbols():
    symbols = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    symbols.set_index("Symbol", inplace=True)
    return symbols


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


tab1, tab2 = st.tabs(["S&P 500", "Information"])

col1, col2 = st.columns(spec=2, gap="small")
col3, col4 = st.columns(spec=2, gap="small")

s_and_p_500_symbols = stock_symbols()
# ticker_stock = s_and_p_500_symbols.loc[st.session_state.ticker]

with st.sidebar:
    st.session_state["ticker"] = st.selectbox("Stock Tickers".upper(), tuple(ticker_names))
    ticker_stock = s_and_p_500_symbols.loc[st.session_state.ticker]
    timeframe = st.selectbox("Analysis Timeframe".upper(), (
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

    st.subheader("Stock Symbol Information")
    st.write(f"SECURITY :  {ticker_stock['Security']}")
    st.write(f"SECTOR :  {ticker_stock['GICS Sector']}")
    st.write(f"HEADQUARTERS :  {ticker_stock['Headquarters Location']}")
    st.write(f"FOUNDED : {ticker_stock['Founded']}")


@st.cache
def full_data():
    ticker_ = yf.Ticker(st.session_state.ticker)
    ticker_history = ticker_.history(period=st.session_state.period)
    ticker_actions = ticker_.actions
    institution_share_holders = ticker_.institutional_holders

    return ticker_history, ticker_actions, institution_share_holders


history, actions, institutional_holders = full_data()

with tab1:
    with st.container():
        with col1:
            fig_history = go.Figure(data=[go.Ohlc(x=history.index,
                                                  open=history['Open'], high=history['High'],
                                                  low=history['Low'], close=history['Close'])
                                          ])

            fig_history.update_layout(xaxis_rangeslider_visible=False, height=500, template="plotly_white",
                                      title=f"{ticker_stock['Security']} Stock Price Movement")
            st.plotly_chart(fig_history, theme="streamlit", use_container_width=True)
            with st.expander("Chart Information"):
                st.write("This chart displays the price movement of a financial security over a given time period. "
                         "The market open, close, high, and low for each trading day are plotted. This chart can be "
                         "used to visualize the price trends and patterns of the security being tracked.")

        with col2:
            fig_volumes = px.bar(history, x=history.index, y="Volume", height=500,
                                 title=f"{ticker_stock['Security']} Stock Volume",
                                 labels={"value": "Volume"},
                                 template="plotly_white", color="Volume")
            st.plotly_chart(fig_volumes, use_container_width=True)
            with st.expander("Chart Information"):
                st.write("This chart displays the trading volume for a financial security over a given time period. "
                         "The volume is plotted on the y-axis (vertical axis), while the time period is plotted on "
                         "the x-axis (horizontal axis). This chart visualizes the level of activity in the security "
                         "being tracked and can provide insight into the demand for the security.")

        with col3:
            fig_dividends = px.line(actions, x=actions.index, y="Dividends",
                                    title=f"{ticker_stock['Security']} Dividends")
            st.plotly_chart(fig_dividends, theme="streamlit", use_container_width=True)
            with st.expander("Dividends Chart Information"):
                st.write("This chart displays the dividends paid out by a company over a given time period. The "
                         "amount of dividends is plotted on the y-axis (vertical axis), while the time period is "
                         "plotted on the x-axis (horizontal axis). This chart visualizes the company's dividend "
                         "history and can provide insight into its financial health and payout policies.")

        with col4:
            fig_stock_splits = px.bar(actions, x=actions.index, y="Stock Splits",
                                      title=f"{ticker_stock['Security']} Stock Splits")
            st.plotly_chart(fig_stock_splits, theme="streamlit", use_container_width=True)
            with st.expander("Stock Splits Chart Information"):
                st.write("This chart displays the stock split history of a company over a given time period. A stock "
                         "split is a corporate action in which a company increases the number of its outstanding "
                         "shares by issuing more shares to its shareholders. The stock split is typically done in a "
                         "ratio, such as 2-for-1, which means that for every 1 share owned, the shareholder receives "
                         "an additional 2 shares. Stock splits are often done to make the stock more affordable for "
                         "individual investors and to increase the liquidity of the stock. On the chart, "
                         "the stock split ratio is plotted on the y-axis (vertical axis), while the time period is "
                         "plotted on the x-axis (horizontal axis). This chart visualizes the company's stock split "
                         "history and can provide insight into its financial and strategic decision-making.")

        with st.expander(f"{ticker_stock['Security']} Institutional Stock Ownership"):
            institute_data = institutional_holders
            st.dataframe(institute_data[["Holder", "Shares", "Date Reported", "% Out", "Value"]], width=1400)

        with st.expander(f"{ticker_stock['Security']} Daily Stock Performance"):
            data = history.reset_index().sort_values(by="Date", ascending=False)
            st.dataframe(data[["Date", "Open", "High", "Low", "Close", "Volume"]], width=1400)

with tab2:
    with st.container():
        st.write("The S&P 500 (Standard & Poor's 500) index is a market-capitalization-weighted index of 500 leading "
                 "publicly traded companies in the U.S. The index is widely considered to be a gauge of the overall "
                 "U.S. stock market, as it includes a broad range of industries and sectors. The S&P 500 is "
                 "calculated by Standard & Poor's, a division of S&P Global, which is a financial services company "
                 "that provides information and analytics to investors. The companies included in the index are "
                 "chosen based on a number of criteria, such as market capitalization, financial strength, "
                 "and liquidity. The index is weighted by market capitalization, which means that the larger the "
                 "company, the more influence it has on the index. The S&P 500 is often used as a benchmark for the "
                 "performance of the U.S. stock market, and it is one of the most widely followed indexes in the "
                 "world.")
