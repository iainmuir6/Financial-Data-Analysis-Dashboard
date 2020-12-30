# Iain Muir
# iam9ez

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from constants import API_KEY
import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import re


class Option:
    def __init__(self, values):
        self.expiration = str(expiration.date())
        self.contractName = values[0]
        self.strike = float(values[2].replace(",", ""))
        self.initial_price = float(values[3].replace(",", ""))


class LongCall(Option):
    def __init__(self, values, current):
        Option.__init__(self, values)
        self.initial_cf = self.initial_price * -100
        self.break_even = self.strike + self.initial_price
        self.market_value = max(current - self.strike, 0) - self.initial_price


class LongPut(Option):
    def __init__(self, values, current):
        Option.__init__(self, values)
        self.initial_cf = self.initial_price * -100
        self.break_even = self.strike - self.initial_price
        self.market_value = max(self.strike - current, 0) - self.initial_price


class ShortCall(Option):
    def __init__(self, values, current):
        Option.__init__(self, values)
        self.initial_cf = self.initial_price * 100
        self.break_even = self.strike + self.initial_price
        self.market_value = self.initial_price - max(current - self.strike, 0)


class ShortPut(Option):
    def __init__(self, values, current):
        Option.__init__(self, values)
        self.initial_cf = self.initial_price * 100
        self.break_even = self.strike - self.initial_price
        self.market_value = self.initial_price - max(self.strike - current, 0)


def graph_iron_condor(orders_df, price):
    """
    :argument orders_df
    :argument price
    :return visualization of option profitability – X: stock price, Y: profit

    """

    long_call, short_call, short_put, long_put = orders_df.values

    scale = 1 + (100 / price)
    x = range(int(price * (1 / scale)), int(price * scale))
    y = []

    for dollar in x:
        lc = LongCall(long_call, dollar).market_value
        sc = ShortCall(short_call, dollar).market_value
        sp = ShortPut(short_put, dollar).market_value
        lp = LongPut(long_put, dollar).market_value

        y.append(lc + sc + sp + lp)

    plt.plot(x, y)
    plt.axvline(x=price, linestyle='dotted')
    plt.plot(x, [0 for _ in range(len(x))], color='black', linewidth=2)
    fig = plt.gcf()

    st.pyplot(fig)


def highlight(df):
    return ['background-color: lightblue'] * len(df) if df.inTheMoney else ['background-color: white'] * len(df)


def iron_condor(ticker):
    # Explanation
    # Days to expiration
    # 4 Orders
        # Suggested
        # Choice
    # graph
    # Max Profit
    # Max Loss

    global expiration

    st.markdown("<center> <h3> Iron Condor Options Strategy </h3> </center>", unsafe_allow_html=True)
    st.markdown(
        "The Iron Condor Options Trading Strategy involves **four options orders** that aim to *minimize risk* "
        "and *generate profit from limited volatility.* These four orders will be: \n"
        "* Short Put at Strike Price A \n"
        "* Short Call at Strike Price B \n"
        "* Long Call above Strike Price B \n"
        "* Long Put below Strike Price A \n"
    )
    st.markdown(
        "<center>"
        "<img src='https://www.optionsbro.com/wp-content/uploads/2017/07/Iron-Condor-Options-Trading-Example.jpg' "
        "height='400' /></center", unsafe_allow_html=True
    )

    st.subheader("Application")
    if st.checkbox("Custom Settings"):
        st.write("Custom...")   # Inputs
    else:
        st.write("Inputs:")
        date = datetime.today().timestamp()
        expiration = datetime.today().date()

        for i, timestamp in enumerate(timestamp_choices):
            if int(timestamp) > (datetime.today() + timedelta(days=35)).timestamp():
                date = timestamp_choices[i-1]
                expiration = datetime.fromtimestamp(int(date)) + timedelta(days=1)
                break

        call_df, put_df = scrape(ticker, date)

        current_price = requests.get('https://finnhub.io/api/v1/quote?symbol=' + ticker +
                                     '&token=' + API_KEY).json()['c']
        remainder = round(current_price, 0) % 10
        rounded = round(current_price, 0) + (-remainder if remainder < 2.5
                                             else 5 - remainder if remainder < 7.5
                                             else 10 - remainder if remainder < 10
                                             else 0)
        maxi = float(list(call_df['strike'])[-1].replace(",", ""))
        mini = float(list(put_df['strike'])[0].replace(",", ""))
        upper = 30 if maxi - rounded > 30 else maxi - rounded
        lower = 40 if rounded - mini > 40 else rounded - mini

        long_call = call_df.loc[
            call_df['strike'].str.replace(",", "").astype(float) == rounded + upper].values[0]
        short_call = call_df.loc[
            call_df['strike'].str.replace(",", "").astype(float) == rounded + (upper - 5)].values[0]
        short_put = put_df.loc[put_df['strike'].str.replace(",", "").astype(float) == rounded - (lower - 5)].values[0]
        long_put = put_df.loc[put_df['strike'].str.replace(",", "").astype(float) == rounded - lower].values[0]

        orders = pd.DataFrame(data=[long_call, short_call, short_put, long_put],
                              columns=['contractName', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask', 'change',
                                       'pctChange', 'volume', 'openInterest', 'impliedVolatility', 'inTheMoney'])

        st.markdown(
            "Expiration Date: **" + str(expiration.date()) + "**\n" +
            "* Days til Expiration: " + str((expiration.date() - datetime.today().date()).days)
        )
        st.dataframe(orders[['contractName', 'strike', 'lastPrice', 'volume', 'impliedVolatility']])
        st.write("Total Price: $" + str(100 * orders['lastPrice'].astype(float).sum()))
        graph_iron_condor(orders, current_price)


def scrape(ticker, date):
    """
    :argument

    :return
    """

    url = "https://finance.yahoo.com/quote/" + ticker + "/options?p=" + ticker + "&date=" + str(date)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    calls, puts = soup.find_all('section', class_='Mt(20px)')

    regex = re.compile(r'>([A-Za-z0-9,.+:-]+)')
    current_price = requests.get('https://finnhub.io/api/v1/quote?symbol=' + ticker +
                                 '&token=' + API_KEY).json()['c']
    st.markdown("<center> <h3> Current Price (" + ticker + "): " + str(current_price) + "</h3> </center>",
                unsafe_allow_html=True)

    option_chain = calls.find('tbody').find_all('tr')
    call_data = [regex.findall(str(option)) for option in option_chain]
    call_df = pd.DataFrame(data=call_data,
                           columns=['contractName', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask', 'change',
                                    'pctChange', 'volume', 'openInterest', 'impliedVolatility'])
    call_df['inTheMoney'] = np.where(call_df['strike'].str.replace(",", "").astype(float) < current_price,
                                     True, False)

    option_chain = puts.find('tbody').find_all('tr')
    put_data = [regex.findall(str(option)) for option in option_chain]
    put_df = pd.DataFrame(data=put_data,
                          columns=['contractName', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask', 'change',
                                   'pctChange', 'volume', 'openInterest', 'impliedVolatility'])
    put_df['inTheMoney'] = np.where(put_df['strike'].str.replace(",", "").astype(float) > current_price,
                                    True, False)

    return call_df, put_df


def run():
    """

    :return
    """
    global timestamp_choices

    # TODO Finish Iron Condor
    # TODO Ability to Create Option "Legs"
    #         • Payoff Summary
    #         • Generalize Options Graphs

    st.markdown("<h1 style='text-align:center;'> Option Chains </h1>", unsafe_allow_html=True)
    st.write()  # Spacing

    ticker = st.text_input("Input Ticker: ")
    if ticker:
        url = "https://finance.yahoo.com/quote/" + ticker + "/options?p=" + ticker
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        options = soup.find_all("select", class_='Fz(s) H(25px) Bd Bdc($seperatorColor)')[0].find_all('option')
        string_choices = [option.text for option in options]
        timestamp_choices = [option['value'] for option in options]
        selection = st.selectbox("Expiration Date: ", string_choices)
        date = timestamp_choices[string_choices.index(selection)]

        if date:
            call_df, put_df = scrape(ticker, date)

            c, p = st.beta_columns(2)
            c.title("Call Options")
            p.title('Put Options')

            c.dataframe(call_df[['strike', 'lastPrice', 'volume', 'inTheMoney']].style.apply(highlight, axis=1))
            p.dataframe(put_df[['strike', 'lastPrice', 'volume', 'inTheMoney']].style.apply(highlight, axis=1))

            st.markdown('------------------------------------------')
        if st.checkbox("Show Iron Condor"):
            iron_condor(ticker)


if __name__ == '__main__':
    start = time.time()
    run()
    print("     --- Finished in %s seconds ---      " % round(time.time() - start, 2))
