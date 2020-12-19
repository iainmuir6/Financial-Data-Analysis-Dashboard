# Iain Muir
# iam9ez

import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from locale import atof
import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import re


def graph_option(data, price):
    """
    :argument data
    :argument price
    :return visualization of option profitability – X: stock price, Y: profit

    """

    last_price = float(data[3])
    strike = float(data[2])
    break_even = last_price + strike
    x = range(int(price * 0.25), int(price * 4))
    y = []

    for dollar in x:
        if dollar < strike:
            y.append(last_price * -100)
        else:
            y.append((dollar * 100) - (break_even * 100))

    # profit = ['g' if p > 0 else 'r' for p in y]
    # profit = [(0, 1, 0) if p > 0 else (1, 0, 0) for p in y]
    # plt.plot(x, y, color=profit)

    plt.plot(x, y)
    plt.axvline(x=price, linestyle='dotted')
    plt.plot(x, [0 for _ in range(len(x))], color='black', linewidth=2)
    plt.show()


def highlight(df):
    return ['background-color: lightblue'] * len(df) if df.inTheMoney else ['background-color: white'] * len(df)


def run():
    """

    :return
    """

    st.markdown("<h1 style='text-align:center;'> Option Chains </h1>", unsafe_allow_html=True)
    st.write()  # Spacing

    api_key = 'bsm4nq7rh5rdb4arch50'

    ticker = st.text_input("Input Ticker: ")
    if ticker:
        url = "https://finance.yahoo.com/quote/" + ticker + "/options?p=" + ticker
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # dates = {}
        # choices = soup.find_all("select", class_='Fz(s) H(25px) Bd Bdc($seperatorColor)')[0].find_all('option')
        # i = 1
        # text = "Choose from the following expiration dates: \n"
        # for c in choices:
        #     dates[str(i)] = c['value']
        #     text += "\t " + str(i) + ") " + c.text + '\n'
        #     i += 1
        # date = dates[input(text)]

        options = soup.find_all("select", class_='Fz(s) H(25px) Bd Bdc($seperatorColor)')[0].find_all('option')
        string_choices = [option.text for option in options]
        timestamp_choices = [option['value'] for option in options]
        selection = st.selectbox("Expiration Date: ", string_choices)
        date = timestamp_choices[string_choices.index(selection)]

        url = "https://finance.yahoo.com/quote/" + ticker + "/options?p=" + ticker + "&date=" + str(date)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        calls, puts = soup.find_all('section', class_='Mt(20px)')

        regex = re.compile(r'>([A-Za-z0-9,.+:-]+)')
        current_price = requests.get('https://finnhub.io/api/v1/quote?symbol=' + ticker + '&token=' + api_key).json()['c']

        option_chain = calls.find('tbody').find_all('tr')
        call_data = [regex.findall(str(option)) for option in option_chain]
        call_df = pd.DataFrame(data=call_data,
                               columns=['contractName', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask', 'change',
                                        'pctChange', 'volume', 'openInterest', 'impliedVolatility'])
        call_df['inTheMoney'] = np.where(call_df['strike'].str.replace(",", "").astype(float) < current_price, True, False)

        option_chain = puts.find('tbody').find_all('tr')
        put_data = [regex.findall(str(option)) for option in option_chain]
        put_df = pd.DataFrame(data=put_data,
                              columns=['contractName', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask', 'change',
                                       'pctChange', 'volume', 'openInterest', 'impliedVolatility'])
        put_df['inTheMoney'] = np.where(put_df['strike'].str.replace(",", "").astype(float) < current_price, True, False)

        st.markdown("<center> <h3> Current Price (" + ticker + "): " + str(current_price) + "</h3> </center>",
                    unsafe_allow_html=True)

        c, p = st.beta_columns(2)
        c.title("Call Options")
        p.title('Put Options')

        c.dataframe(call_df[['strike', 'lastPrice', 'volume', 'inTheMoney']].style.apply(highlight, axis=1))
        p.dataframe(put_df[['strike', 'lastPrice', 'volume', 'inTheMoney']].style.apply(highlight, axis=1))
