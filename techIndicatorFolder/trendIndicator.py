# Iain Muir
# iam9ez

import matplotlib.pyplot as plt
from datetime import datetime
import mplfinance as fplt
import streamlit as st
import pandas as pd
import requests
import time


def run(data):
    """
    50 and 200 Day Exponential Moving Averages

    :return
    """

    st.markdown("<h3 style='text-align:center;'> Trend Indicator </h3>", unsafe_allow_html=True)
    st.write()  # Spacing

    token = data['token']
    ticker = data['ticker']
    start_date = data['startDate']
    end_date = data['endDate']
    candles = data['candles']

    fifty = requests.get(url='https://finnhub.io/api/v1/indicator?symbol=' + ticker + '&resolution=D&' +
                             'from=' + str(int(start_date.timestamp())) +
                             '&to=' + str(int(end_date.timestamp())) +
                             '&indicator=ema&timeperiod=50&token=' + token).json()

    two_hundo = requests.get(url='https://finnhub.io/api/v1/indicator?symbol=' + ticker + '&resolution=D&' +
                                 'from=' + str(int(start_date.timestamp())) +
                                 '&to=' + str(int(end_date.timestamp())) +
                                 '&indicator=ema&timeperiod=200&token=' + token).json()
    fig = fplt.plot(
        data=candles,
        type='candle',
        style='charles',
        title=ticker + " (" + str(start_date.date()) + " - " + str(end_date.date()) + ")",
        ylabel='Price ($)',
        volume=True,
        mav=(50, 200),
        ylabel_lower='Shares \n Traded',
        block=True
    )

    # plt.plot(fifty['c'], color='black')
    # plt.plot(two_hundo['c'], color='red')
    # plt.show()

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(fig)


if __name__ == '__main__':
    start = time.time()

    tick = input("Input Ticker: ")
    s = datetime(datetime.today().year - 1, 1, 1)
    e = datetime.today()
    api_key = 'bsm4nq7rh5rdb4arch50'

    df = pd.DataFrame(requests.get('https://finnhub.io/api/v1/stock/candle?symbol=' + tick + '&resolution=D&' +
                                   'from=' + str(int(s.timestamp())) +
                                   '&to=' + str(int(e.timestamp())) +
                                   '&token=' + api_key).json()).drop(axis=1, labels='s')
    df = pd.DataFrame({
        'Date': pd.to_datetime(df['t']),
        'Open': df['o'],
        'High': df['h'],
        'Low': df['l'],
        'Close': df['c'],
        'Volume': df['v'],
    })

    d = {'token': api_key,
         'ticker': tick,
         'startDate': s,
         'endDate': e,
         'candles': df.set_index('Date')}

    run(d)

    print("     --- Finished in %s seconds ---      " % round(time.time() - start, 2))
