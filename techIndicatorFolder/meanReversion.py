# Iain Muir
# iam9ez

import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime
from constants import API_KEY
import streamlit as st
import pandas as pd
import requests
import time


def run(data):
    """

    :return
    """

    st.markdown("<h3 style='text-align:center;'> Mean Reversion </h3>", unsafe_allow_html=True)
    st.write(
        """
        Mean Reversion indicators measure  how far a price swing will stretch before a counter impulse triggers
        a [retracement](https://www.investopedia.com/terms/r/retracement.asp); this is a lagging measure as it looks
        at how historical data led to the current security price.

        Specifically, this indicator uses [Bollinger Bands](https://www.investopedia.com/terms/b/bollingerbands.asp)
        to attempt to identify turning points by measuring how far price can travel from a central tendency pivot; 
        for (20, 2) bands, this pivot point is the *20*-day Simple Moving Average, and the bands are trendlines plotted
        two [standard deviations](https://www.investopedia.com/terms/s/standarddeviation.asp) away from the SMA

        *SIGNALS*
        * **SELL:** Security price reaches the upper Bollinger Band, i.e. is 2 standard deviations above SMA
        * **BUY:** Security price reaches the lower Bollinger Band, i.e. is 2 standard deviations below SMA
        """
    )
    st.write()

    ticker = data['ticker']
    start_date = data['startDate']
    end_date = data['endDate']

    """
    Bollinger Bands
    (20, 2): 20 days, 2 standard deviations

    API
    :return {
              'c': [$, ...],
              'h': [$, ...],
              'l': [$, ...],
              'lowerband': [$, ...],
              'middleband': [$, ...],
              'upperband': [$, ...]
             }

    """
    bands = requests.get(url='https://finnhub.io/api/v1/indicator?symbol=' + ticker + '&resolution=D&' +
                             'from=' + str(int(start_date.timestamp())) +
                             '&to=' + str(int(end_date.timestamp())) +
                             '&indicator=bbands&timeperiod=20&token=' + API_KEY).json()

    df = pd.DataFrame({
        'Date': pd.to_datetime(bands['t'][19:]),
        'Close': bands['c'][19:],
        'Lower Band': bands['lowerband'][19:],
        'Middle Band': bands['middleband'][19:],
        'Upper Band': bands['upperband'][19:],
    })
    df = df.set_index('Date')

    fig = px.line(df, color_discrete_map={
        'Close': 'black',
        'Lower Band': 'blue',
        'Middle Band': 'grey',
        'Upper Band': 'orange',
    })

    # plt.plot(bands['c'][19:], color='black')
    # plt.plot(bands['lowerband'][19:], color='green')
    # plt.plot(bands['middleband'][19:], color='black', alpha=0.5)
    # plt.plot(bands['upperband'][19:], color='red')
    # plt.title('Bollinger Bands (20, 2)')
    # fig = plt.gcf()
    # st.pyplot(fig)

    st.plotly_chart(fig)


if __name__ == '__main__':
    start = time.time()

    tick = input("Input Ticker: ")
    s = datetime(datetime.today().year - 1, 1, 1)
    e = datetime.today()

    d = {'token': API_KEY,
         'ticker': tick,
         'startDate': s,
         'endDate': e}

    run(d)

    print("     --- Finished in %s seconds ---      " % round(time.time() - start, 2))
