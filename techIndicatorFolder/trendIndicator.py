# Iain Muir
# iam9ez

from plotly.subplots import make_subplots
import plotly.graph_objects as go
# import matplotlib.pyplot as plt
from datetime import datetime
import plotly.express as px
# import mplfinance as fplt
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

    fig = make_subplots(
        specs=[[{"secondary_y": True}]]
    )
    fig.add_trace(
        go.Candlestick(
            x=candles.index,
            open=candles['Open'],
            high=candles['High'],
            low=candles['Low'],
            close=candles['Close'],
        ),
        secondary_y=True
    )
    fig.add_trace(
        go.Scatter(
            x=candles.index[-len(fifty['ema']):],
            y=fifty['ema'],
            mode='lines',
            line={'color': 'rgb(0,0,0,0.5)'}
        ),
        secondary_y=True
    )
    fig.add_trace(
        go.Scatter(
            x=candles.index[-len(two_hundo['ema']):],
            y=two_hundo['ema'],
            mode='lines',
            line={'color': 'rgb(0,0,0,0.5)'}
        ),
        secondary_y=True
    )
    fig.add_trace(
        go.Bar(
            x=candles.index,
            y=candles['Volume'],
            marker={'color': 'rgb(0,0,0)'}
        ),
        secondary_y=False
    )
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangebreaks=[
            dict(bounds=["sat", "sun"])
        ],
        ticklabelmode="period"
    )
    fig.layout.yaxis2.showgrid = False

    st.plotly_chart(fig)


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
    df['t'] = [datetime.fromtimestamp(x) for x in df['t']]

    df = pd.DataFrame({
        'Date': df['t'].dt.date,
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
