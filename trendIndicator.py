# Iain Muir
# iam9ez

from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime
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
    st.write(
        """
        Trend indicators analyze whether a market is moving up, down, or sideways over time; this is a lagging measure
        as it looks at how historical data led to the current security price.
        
        Specifically, this indicator looks at the 50- and 200-day Exponential Moving Average of a security; in general,
        the 50-day EMA is used to measure the average intermediate price of a security, while the 200-day EMA measures
        the average long term price. 
        
        *SIGNALS*
        * **SELL:** Shorter-term EMA crossing over the longer-term average signifies a bearish change in trend
        * **BUY:** Longer-term EMA crossing over the shorter-term average signifies a bullish change in trend
        
        Example (Investopedia):
        """
    )
    st.markdown('<center><img src="https://www.investopedia.com/thmb/W53XvEGTcsv5QywLWP4gkvAdWLE=/4888x3964/filters:no_'
                'upscale():max_bytes(150000):strip_icc():format(webp)/dotdash_Final_Top_Technical_Indicators_for_'
                'Rookie_Traders_Sep_2020-01-65454aefbc9042ef98df266def257fa3.jpg" height="250"/></center>',
                unsafe_allow_html=True)
    st.write()
    st.subheader('Stock Data')

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
            name='Candlestick'
        ),
        secondary_y=True
    )
    fig.add_trace(
        go.Scatter(
            x=candles.index[50:],
            y=fifty['ema'][50:],
            mode='lines',
            line={'color': 'rgb(203,213,232)'},
            name='50-Day EMA'
        ),
        secondary_y=True
    )
    fig.add_trace(
        go.Scatter(
            x=candles.index[200:],
            y=two_hundo['ema'][200:],
            mode='lines',
            line={'color': 'rgb(253,205,172)'},
            name='200-Day EMA'
        ),
        secondary_y=True
    )
    fig.add_trace(
        go.Bar(
            x=candles.index,
            y=candles['Volume'],
            marker={'color': 'rgb(0,0,0)'},
            name='Volume'
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
    fig.layout.title = 'Trend Indicator Graph'

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
