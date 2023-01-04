import datetime

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf

st.set_page_config(page_title="Stock Charts Test", layout="wide", initial_sidebar_state="auto")
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


def my_figure(data):
    my_fig = make_subplots(
        rows=5, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "scatter"}],
               [{"type": "scatter"}],
               [{"type": "scatter"}],
               [{"type": "scatter"}],
               [{"type": "scatter"}]]
    )

    my_fig.add_trace(
        go.Scatter(
            x=data.Date,
            y=data.Volume,
            mode="lines",
            name="Volume",
        ),
        row=5, col=1
    )

    my_fig.add_trace(
        go.Scatter(
            x=data.Date,
            y=data.Open,
            mode="lines",
            name="Opening Price",
        ),
        row=4, col=1
    )

    my_fig.add_trace(
        go.Scatter(
            x=data.Date,
            y=data.High,
            mode="lines",
            name="Opening Price",
        ),
        row=3, col=1
    )

    my_fig.add_trace(
        go.Scatter(
            x=data.Date,
            y=data.Low,
            mode="lines",
            name="Opening Price",
        ),
        row=2, col=1
    )

    my_fig.add_trace(
        go.Scatter(
            x=data.Date,
            y=data.Close,
            mode="lines",
            name="Closing Price",
        ),
        row=1, col=1
    )
    print(f"{st.session_state.ticker} b4 fig")
    my_fig.update_layout(
        height=900,
        showlegend=True,
        title_text=f"{st.session_state.ticker} Opening and Closing", template="plotly_dark",
    )
    return my_fig


st.header('S&P 500 Stocks')

with st.sidebar:
    st.session_state["ticker"] = st.selectbox("Stocks", tuple(ticker_names))
    st.button("Maximum Dates", on_click=all_time)
    st.button("10 years to date", on_click=ten_years_to_date)
    st.button("5 years to date", on_click=five_years_to_date)
    st.button("2 Years to date", on_click=two_years_to_date)
    st.button("1 year to date", on_click=one_year_to_date)
    st.button("6 Months to date", on_click=six_months_to_date)
    st.button("3 Months to date", on_click=three_months_to_date)
    st.button("1 Month to date", on_click=month_to_date)
    st.button("5 days to date", on_click=five_days_to_date)
    st.button("1 day to date", on_click=one_day_to_date)

with st.container():
    change_ticker()
    current_data = st.session_state.data
    fig = my_figure(current_data)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with st.container():
    st.dataframe(current_data[["Date", "Open", "High", "Low", "Close", "Volume"]], width=1400)
