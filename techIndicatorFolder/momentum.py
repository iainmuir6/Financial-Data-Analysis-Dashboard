# Iain Muir
# iam9ez

from datetime import datetime
import streamlit as st
import pandas as pd
import requests
import time


def run(data):
    """

    :return
    """

    st.markdown("<h3 style='text-align:center;'> Momentum </h3>", unsafe_allow_html=True)
    st.write()  # Spacing


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
