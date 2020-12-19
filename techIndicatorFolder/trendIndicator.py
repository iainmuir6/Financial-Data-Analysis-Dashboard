# Iain Muir
# iam9ez

import matplotlib.pyplot as plt
from datetime import datetime
import mplfinance as fplt
import streamlit as st
import pandas as pd
import requests


def run(self):
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