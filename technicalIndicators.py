"""
Iain Muir, iam9ez

Five Categories of Technical Indicators:
      Trend
      Mean Reversion
      Relative Strength
      Volume
      Momentum
"""

import matplotlib.pyplot as plt
from datetime import datetime
import mplfinance as fplt
import requests


class TechnicalIndicators:
    def __init__(self, ticker):
        self.token = 'bsm4nq7rh5rdb4arch50'
        self.ticker = ticker
        self.start_date = datetime(datetime.today().year - 2, 1, 1)
        self.end_date = datetime.today()
        self.candles = requests.get('https://finnhub.io/api/v1/stock/candle?symbol=' + ticker + '&resolution=D&' +
                                    'from=' + str(int(self.start_date.timestamp())) +
                                    '&to=' + str(int(self.end_date.timestamp())) + '&token=' + self.token).json()

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
        plt.plot()

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






