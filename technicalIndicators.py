"""
Iain Muir, iam9ez

Five Categories of Technical Indicators:
      Trend
      Mean Reversion
      Relative Strength
      Volume
      Momentum
"""

from techIndicatorFolder import trendIndicator, meanReversion, relativeStrength, volume, momentum
import matplotlib.pyplot as plt
from datetime import datetime
import mplfinance as fplt
import streamlit as st
import pandas as pd
import requests
import time
import os


class TechnicalIndicators:
    def __init__(self, ticker):
        self.token = os.environ['API_KEY']
        self.ticker = ticker
        self.start_date = datetime(datetime.today().year - 1, 1, 1)
        self.end_date = datetime.today()
        df = pd.DataFrame(requests.get('https://finnhub.io/api/v1/stock/candle?symbol=' + ticker + '&resolution=D&' +
                                       'from=' + str(int(self.start_date.timestamp())) +
                                       '&to=' + str(int(self.end_date.timestamp())) +
                                       '&token=' + self.token).json()).drop(axis=1, labels='s')
        df = pd.DataFrame({
            'Date': pd.to_datetime(df['t']),
            'Open': df['o'],
            'High': df['h'],
            'Low': df['l'],
            'Close': df['c'],
            'Volume': df['v'],
        })
        self.candles = df.set_index('Date')

    def trend_indicator(self):
        """
        50 and 200 Day Exponential Moving Averages

        :return
        """

        fifty = requests.get(url='https://finnhub.io/api/v1/indicator?symbol=' + self.ticker + '&resolution=D&' +
                                 'from=' + str(int(self.start_date.timestamp())) +
                                 '&to=' + str(int(self.end_date.timestamp())) +
                                 '&indicator=ema&timeperiod=50&token=' + self.token).json()

        two_hundo = requests.get(url='https://finnhub.io/api/v1/indicator?symbol=' + self.ticker + '&resolution=D&' +
                                     'from=' + str(int(self.start_date.timestamp())) +
                                     '&to=' + str(int(self.end_date.timestamp())) +
                                     '&indicator=ema&timeperiod=200&token=' + self.token).json()
        fig = fplt.plot(
            data=self.candles,
            type='candle',
            style='charles',
            title=self.ticker + " (" + str(self.start_date.date()) + " - " + str(self.end_date.date()) + ")",
            ylabel='Price ($)',
            volume=True,
            mav=(50, 200),
            ylabel_lower='Shares \n Traded',
            block=False
        )

        # plt.plot(fifty['c'], color='black')
        # plt.plot(two_hundo['c'], color='red')
        # plt.show()

        return fig

    def mean_reversion(self):
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
        bands = requests.get(url='https://finnhub.io/api/v1/indicator?symbol=' + self.ticker + '&resolution=D&' +
                                 'from=' + str(int(self.start_date.timestamp())) +
                                 '&to=' + str(int(self.end_date.timestamp())) +
                                 '&indicator=bbands&timeperiod=20&token=' + self.token).json()

        plt.plot(bands['c'][19:], color='black')
        plt.plot(bands['lowerband'][19:], color='green')
        plt.plot(bands['middleband'][19:], color='black', alpha=0.5)
        plt.plot(bands['upperband'][19:], color='red')
        plt.show()


def run():
    """

    :return
    """
    global ticker

    # # Markdown Tags
    # st.markdown("<center> <img src='https://img.shields.io/badge/python-100%25-brightgreen' "
    #             "height='20'/> <img src='https://img.shields.io/badge/implementation-streamlit-orange' "
    #             "height='20'/> </center>", unsafe_allow_html=True)
    # # Logos
    # st.markdown("<center> "
    #             "<img src='https://upload.wikimedia.org/wikipedia/en/d/da/Robinhood_%28company%29_logo.svg' "
    #             "height='50'/> "
    #             "<img src='https://upload.wikimedia.org/wikipedia/commons/d/da/Yahoo_Finance_Logo_2019.svg' "
    #             "height='125'/> </center>", unsafe_allow_html=True)
    # st.write()      # Spacing

    st.markdown("<h1 style='text-align:center;'> Technical Indicators </h1>", unsafe_allow_html=True)
    st.write()      # Spacing

    # Navigation
    st.sidebar.title("Techincal Indicators")

    pages = {
        "Trend Indicators": trendIndicator,
        "Mean Reversion": meanReversion,
        "Relative Strength": relativeStrength,
        "Volume": volume,
        "Momentum": momentum,
    }

    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]

    ticker = st.text_input("Input Ticker: ")

    # Inputs

    if ticker:
        s = datetime(datetime.today().year - 1, 1, 1)
        e = datetime.today()
        API_KEY = os.environ['api_key']

        df = pd.DataFrame(requests.get('https://finnhub.io/api/v1/stock/candle?symbol=' + ticker + '&resolution=D&' +
                                       'from=' + str(int(s.timestamp())) +
                                       '&to=' + str(int(e.timestamp())) +
                                       '&token=' + API_KEY).json()).drop(axis=1, labels='s')
        df['t'] = [datetime.fromtimestamp(x) for x in df['t']]

        df = pd.DataFrame({
            'Date': df['t'].dt.date,
            'Open': df['o'],
            'High': df['h'],
            'Low': df['l'],
            'Close': df['c'],
            'Volume': df['v'],
        })

        data = {'token': API_KEY,
                'ticker': ticker,
                'startDate': s,
                'endDate': e,
                'candles': df.set_index('Date')}

        page.run(data)


if __name__ == '__main__':
    start = time.time()

    ticker = input("Input Ticker: ")
    run()

    # t = TechnicalIndicators(tick)
    # st.set_option('deprecation.showPyplotGlobalUse', False)
    # st.pyplot(t.trend_indicator())
    # t.mean_reversion()

    print("     --- Finished in %s seconds ---      " % round(time.time() - start, 2))
