import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
from numerize import numerize

st.set_page_config(page_title="S&P 500 Stocks", layout="wide", initial_sidebar_state="auto", page_icon=":chart:")
st.header('S&P 500')


@st.cache
def stock_symbols():
    symbols = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    symbols.set_index("Symbol", inplace=True)
    symbol_names = sorted(list(symbols.index))
    return symbols, symbol_names


def outstanding_shares():
    shares = pd.read_csv("Shares_Outstanding.csv").set_index("Unnamed: 0")
    index = shares["Symbols"]
    shares.set_index(index, inplace=True)
    return shares


shares_outstanding = outstanding_shares()

s_and_p_500_symbols, ticker_names = stock_symbols()

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


tab1, tab2, tab3 = st.tabs(["S&P 500", "Information", "Analysis"])

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
    try:
        outstanding_share_number = shares_outstanding.loc[st.session_state['ticker']]['Raw_outstanding_share_vals']
    except KeyError:
        outstanding_share_number = "Value Missing"
    st.subheader("Stock Symbol Information")
    st.write(f"SECURITY :  {ticker_stock['Security']}")
    st.write(f"SECTOR :  {ticker_stock['GICS Sector']}")
    st.write(f"SUB-INDUSTRY :  {ticker_stock['GICS Sub-Industry']}")
    st.write(f"HEADQUARTERS :  {ticker_stock['Headquarters Location']}")
    st.write(f"FOUNDED : {ticker_stock['Founded']}")
    st.write(f"DATE FIRST ADDED : {ticker_stock['Date added']}")
    st.write(f"CIK : {ticker_stock['CIK']}")
    st.write(f"Outstanding Shares: {outstanding_share_number}")


@st.cache
def full_data():
    if st.session_state.ticker == "BRK.B":
        ticker_ = yf.Ticker("BRK-B")
    else:
        ticker_ = yf.Ticker(st.session_state.ticker)
    ticker_history = ticker_.history(period=st.session_state.period)
    ticker_actions = ticker_.actions
    institution_share_holders = ticker_.institutional_holders

    return ticker_history, ticker_actions, institution_share_holders


history, actions, institutional_holders = full_data()
latest_close = history['Close'].tail().values[0]


@st.cache
def google_tick():
    goog = yf.Ticker("GOOG").history(period="max")["Close"].tail(1).values[0]
    googl = yf.Ticker("GOOGL").history(period="max")["Close"].tail(1).values[0]
    closing_price = goog + googl
    return closing_price


google_close = google_tick()

with tab1:
    try:
        if st.session_state['ticker'] == "GOOGL":
            market_cap = numerize.numerize(outstanding_share_number * google_close)
            st.write(f"{ticker_stock['Security']}'s Markets cap at closing was {market_cap}.")
        else:
            market_cap = numerize.numerize(outstanding_share_number * latest_close)
            st.write(f"{ticker_stock['Security']}'s Markets cap at closing was {market_cap}.")
    except TypeError:
        pass

    with st.expander(f"{ticker_stock['Security']} Institutional Stock Ownership"):
        institute_data = institutional_holders
        st.dataframe(institute_data[["Holder", "Shares", "Date Reported", "% Out", "Value"]], width=1400)

    with st.expander(f"{ticker_stock['Security']} Daily Stock Performance"):
        data = history.reset_index().sort_values(by="Date", ascending=False)
        st.dataframe(data[["Date", "Open", "High", "Low", "Close", "Volume"]], width=1400)

    col1, col2 = st.columns(spec=2, gap="small")
    col3, col4 = st.columns(spec=2, gap="small")
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
                         "The market open, close, high, and low for each trading day are plotted. This chart"
                         " visualizes the price trends and patterns of the security being tracked.")

        with col2:
            fig_volumes = px.bar(history, x=history.index, y="Volume", height=500,
                                 title=f"{ticker_stock['Security']} Stock Volume",
                                 labels={"value": "Volume"})
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
                         "shares by issuing more shares to its shareholders.\n\n The stock split is typically done in a"
                         "ratio, such as 2-for-1, which means that for every 1 share owned, the shareholder receives "
                         "an additional 2 shares. Stock splits are often done to make the stock more affordable for "
                         "individual investors and to increase the liquidity of the stock.\n\n On the chart, "
                         "the stock split ratio is plotted on the y-axis (vertical axis), while the time period is "
                         "plotted on the x-axis (horizontal axis). This chart visualizes the company's stock split "
                         "history and can provide insight into its financial and strategic decision-making.")

with tab2:
    with st.container():
        st.write("Welcome to the information section!\n\n This "
                 "section is designed to provide background understanding for those interested in learning about "
                 "these concepts. It is not intended to be financial or investment advice, but rather a resource "
                 "for gaining a better understanding of the S&P 500 Index and the terms used in the world of stock "
                 "investing.")
        with st.expander("What is the S&P 500 Index"):
            st.write("The S&P 500 (Standard & Poor's 500) index is a market-capitalization-weighted index of 500 "
                     "leading publicly traded companies in the U.S. The index is widely considered to be a gauge of "
                     "the overall U.S. stock market, as it includes a broad range of industries and sectors.\n\n"
                     "The S&P 500 is calculated by Standard & Poor's, a division of S&P Global, which is a financial "
                     "services company"
                     "that provides information and analytics to investors. The companies included in the index are "
                     "chosen based on a number of criteria, such as market capitalization, financial strength, "
                     "and liquidity. \n\nThe index is weighted by market capitalization, which means that the larger "
                     "the"
                     "company, the more influence it has on the index. The S&P 500 is often used as a benchmark for the"
                     "performance of the U.S. stock market, and it is one of the most widely followed indexes in the "
                     "world.")

        with st.expander("What is a Market-Capitalization-Weighted index"):
            st.write("A market-capitalization-weighted index is an index where the weight of each component security "
                     "is proportional to its market capitalization.\n\n Market capitalization is the value of a "
                     "company's"
                     "outstanding shares of stock, and it is calculated by multiplying the number of shares by the "
                     "current market price of one share. For example, if a company has 1 million shares of stock "
                     "outstanding and the market price of each share is 50 Dollars, the company's market capitalization"
                     "would be 50 million dollars. \n\n In a market-capitalization-weighted index, the companies with "
                     "the"
                     "highest"
                     "market capitalization have the greatest influence on the index. For example, in the S&P 500 "
                     "index, the largest companies by market capitalization, such as Apple and Microsoft, "
                     "have a greater impact on the index than smaller companies. This is because the index is "
                     "calculated based on the market capitalizations of the component companies, so the companies "
                     "with the largest market caps make up a larger portion of the index. \n\nTo calculate the value "
                     "of a"
                     "market-capitalization-weighted index, you would take the market capitalization of each "
                     "component company and multiply it by the index's weighting factor for that company. The "
                     "weighting factors are typically based on the market capitalization of each company relative to "
                     "the total market capitalization of all the companies in the index. The resulting values are "
                     "then summed to give the overall value of the index.")

        with st.expander("What is Day Trading"):
            st.write("Day trading is a trading strategy where an investor buys and sells financial instruments within "
                     "the same trading day. The goal of day traders is to make profits by taking advantage of small "
                     "price movements in highly liquid stocks or other financial instruments.\n\n Day traders "
                     "typically hold their positions for a few hours to a few days at most, and they close out all "
                     "positions before the market close to avoid any overnight risk. Because they hold their "
                     "positions for such a short time, day traders typically look for liquid instruments that they "
                     "can buy and sell quickly to take advantage of the price movements.")

        with st.expander("What are liquid instruments"):
            st.write("Liquid instruments are financial instruments that can be easily bought or sold on the market "
                     "without affecting the asset's price. In other words, there is a high level of liquidity for "
                     "these instruments, which means that there are many buyers and sellers available at any given "
                     "time, and the spread between the bid and ask prices is usually small. \n\nSome examples of "
                     "liquid instruments include major currency pairs in the forex market, large cap stocks listed on "
                     "major stock exchanges, and government bonds. These instruments are considered liquid because "
                     "there are many market participants trading them, which creates a deep and liquid market.")

        with st.expander("Thoughts on Day Trading"):
            st.write("Day trading can be an exciting and potentially lucrative activity, but it is important to keep "
                     "in mind that it is not without its risks. According to a study of Brazilian day traders, "
                     "97% of those who were in the market for more than 300 days lost money, with only 1.1% ending up "
                     "profitable. These statistics highlight the inherent challenges and risks of day trading, "
                     "and suggest that success in the market is not guaranteed.\n\n Many amateur day traders may not "
                     "fully understand the complexities of the market or have a solid investment strategy, "
                     "leading to poor decision making and potential financial losses. It is essential for day "
                     "traders, particularly those who are just starting out, to thoroughly educate themselves and "
                     "have a clear plan in place to minimize risks and maximize profits. Even professional traders "
                     "with decades of experience can be caught off guard by the unpredictable nature of the market, "
                     "so it is important for all day traders to be aware of the potential for 'pain trades' - market "
                     "movements that cause the most financial hardship to the most people. Overall, it is crucial for "
                     "day traders to approach the market with caution and a solid understanding of the risks and "
                     "potential rewards.\n\n I am a firm believer in the benefits of long term value investing. While "
                     "day trading and other short term strategies may offer the potential for quick profits, "
                     "they also come with a higher level of risk. In contrast, long term value investing allows for a "
                     "slower and steadier approach, and requires a deeper understanding of a company's fundamentals. "
                     "While it may not offer the same thrill as day trading, I believe it is a safer and ultimately "
                     "more successful strategy for building wealth over time. It is important to recognize that there "
                     "is no 'low risk, get rich quick' scheme in the world of investing. Good things take time, "
                     "and a measured and well-informed approach is the key to long term success.")

with tab3:
    top_mkt_cap_list = ['AAPL', 'MSFT', 'AMZN', 'UNH', 'XOM', 'JNJ', 'JPM', 'WMT', 'NVDA', 'TSLA', 'MA', 'PG', 'LLY',
                        'CVX', 'HD', 'MRK', 'ABBV', 'BAC', 'KO', 'PFE', 'BRK-A', 'BRK-B', 'BF-A', 'BF-B', 'GOOGL',
                        'GOOG']
    sectors = pd.DataFrame(s_and_p_500_symbols["GICS Sector"].value_counts()).sort_values(by="GICS Sector",
                                                                                          ascending=False)
    st.write("Making stock analysis accessible to the general public is a complex task that poses several challenges. "
             "One of the main obstacles is obtaining accurate and up-to-date data. Currently, the data used for "
             "analysis is often scraped from the internet, which can lead to inconsistencies and inaccuracies. To "
             "overcome this challenge, I am constantly refining my methods and exploring new ways to obtain accurate "
             "and timely data. Additionally, I am working to expand the scope of my analysis by incorporating a wider "
             "range of data sources to provide a more comprehensive picture of the market.")
    fig_sector = px.bar(sectors,
                        y=sectors.index,
                        x="GICS Sector",
                        color=sectors.index,
                        height=600,
                        labels={"index": "Sectors"},
                        title="S&P 500 Company Sectors",
                        text_auto='.2s', template="plotly_dark")
    st.plotly_chart(fig_sector, theme="streamlit", use_container_width=True)


    @st.cache
    def closing_prices():
        closing_price_list = []

        for symbol in top_mkt_cap_list:
            try:
                closing_price_list.append(yf.Ticker(symbol).history(period="max")["Close"].tail(1).values[0])
            except IndexError:
                closing_price_list.append(symbol)
        return closing_price_list


    prices_at_close = closing_prices()
    closing_tickers_data = {"Symbols": top_mkt_cap_list, "Closing_price": prices_at_close}
    df_symbol_close = pd.DataFrame(data=closing_tickers_data)
    df_symbol_close.loc[21, "Symbols"] = "BRK.B"
    df_symbol_close.set_index("Symbols", inplace=True)
    df_symbol_close.loc["GOOGL", "Closing_price"] = df_symbol_close.loc["GOOGL", "Closing_price"] + df_symbol_close.loc[
        "GOOG", "Closing_price"]
    df_symbol_close.index.names = ["index"]
    shares_outstanding.index.names = ["index"]

    merged_price_and_outstanding_shares = df_symbol_close.merge(shares_outstanding, how="inner", on="index").drop(
        columns=["Oustanding_Shares", "Source_urls"])
    merged_price_and_outstanding_shares["Market_cap"] = merged_price_and_outstanding_shares["Closing_price"] * \
                                                        merged_price_and_outstanding_shares[
                                                            "Raw_outstanding_share_vals"]
    merged_price_and_outstanding_shares.sort_values(by="Market_cap", ascending=False, inplace=True)


    def format_market_cap(market_caps):
        units = ['', 'K', 'M', 'B', 'T']
        i = 0
        while market_caps >= 1000:
            market_caps /= 1000
            i += 1
        return f"{market_caps:.2f}{units[i]}"


    merged_price_and_outstanding_shares["Formatted_Cap"] = merged_price_and_outstanding_shares["Market_cap"].apply(
        format_market_cap)
    merged_price_and_outstanding_shares.set_index("Symbols", inplace=True)
    top_10_mkt_caps = merged_price_and_outstanding_shares.head(10)

    fig_index_weight = px.bar(top_10_mkt_caps,
                              x="Market_cap",
                              y=top_10_mkt_caps.index,
                              orientation="h",
                              color=top_10_mkt_caps.index,
                              height=600,
                              text='Formatted_Cap',
                              template="plotly_dark",
                              title="Top 10 S&P 500 companies by Index Weight.",
                              labels={"Market_cap": "Market Cap", "Symbols": "Companies"})
    st.plotly_chart(fig_index_weight, theme="streamlit", use_container_width=True)