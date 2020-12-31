# Iain Muir
# iam9ez

from plotly.subplots import make_subplots
import plotly.graph_objects as go
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

    st.markdown("<h3 style='text-align:center;'> Relative Strength </h3>", unsafe_allow_html=True)
    st.subheader("Stochastic")
    st.markdown(
        """
        Market movement evolves through buy-and-sell cycles that can be identified through 
        [stochastics](https://www.investopedia.com/terms/s/stochasticoscillator.asp) (14,7,3) 
        and other relative strength indicators. These cycles often reach a peak at 
        [overbought](https://www.investopedia.com/terms/o/overbought.asp) or 
        [oversold](https://www.investopedia.com/terms/o/oversold.asp) levels and then shift in the opposite direction,
        with the two indicator lines crossing over. Cycle alternations don’t automatically translate into higher or
        lower security prices as you might expect. Rather, bullish or bearish turns signify periods in which buyers or
        sellers are in control of the [ticker tape](https://www.investopedia.com/terms/t/tickertape.asp).
        It still takes volume, momentum, and other market forces to generate price change.
        
        SPDR S&P Trust (SPY) oscillates through a series of buy-and-sell cycles over a 5-month period. Look for signals
        where:
        * A [crossover](https://www.investopedia.com/terms/c/crossover.asp) has occurred at or near an overbought or
         oversold level
        * Indicator lines then [thrust](https://www.investopedia.com/terms/t/thrusting-line.asp) toward the center of
         the panel.
         
        Example (Investopedia): 
        """
    )
    st.markdown('<center><img src="https://www.investopedia.com/thmb/lSafy9mbYVCFHLQliHn2_QC9Qh0=/4888x3964/filters:'
                'no_upscale():max_bytes(150000):strip_icc():format(webp)/dotdash_Final_Top_Technical_Indicators_for_'
                'Rookie_Traders_Sep_2020-02-9c5b800f6f424b778148a2c6717ea60a.jpg" height="250"/></center>',
                unsafe_allow_html=True)
    st.write("-------------------------")
    st.subheader("Relative Strength Index (RSI)")
    st.markdown(
        """
        The relative strength index (RSI) is a 
        [momentum indicator](https://www.investopedia.com/investing/momentum-and-relative-strength-index/)
        used in technical analysis that measures the magnitude of recent price changes to evaluate overbought or
        oversold conditions in the price of a stock or other asset. The RSI is displayed as an oscillator
        (a line graph that moves between two extremes) and can have a reading from 0 to 100. The indicator was
        originally developed by J. Welles Wilder Jr. and introduced in his seminal 1978 book, "New Concepts in
        Technical Trading Systems."

        Traditional interpretation and usage of the RSI are that values of 70 or above indicate that a security is
        becoming overbought or overvalued and may be primed for a trend reversal or corrective pullback in price.
        An RSI reading of 30 or below indicates an oversold or undervalued condition.
        """
    )

    ticker = data['ticker']
    start_date = data['startDate']
    end_date = data['endDate']
    candles = data['candles']

    stochastic = requests.get(url='https://finnhub.io/api/v1/indicator?symbol=' + ticker + '&resolution=D&' +
                                  'from=' + str(int(start_date.timestamp())) +
                                  '&to=' + str(int(end_date.timestamp())) +
                                  '&indicator=stochrsi&timeperiod=14&seriestype=c&fastkperiod=7&fastdperiod=3&'
                                  'token=' + API_KEY).json()
    fast_d, fast_k = stochastic["'fastd"][14:], stochastic['fastk'][14:]

    rsi = requests.get(url='https://finnhub.io/api/v1/indicator?symbol=' + ticker + '&resolution=D&' +
                           'from=' + str(int(start_date.timestamp())) +
                           '&to=' + str(int(end_date.timestamp())) +
                           '&indicator=rsi&seriestype=c&token=' + API_KEY).json()['rsi'][3:]

    fig = make_subplots(rows=3, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.05)

    fig.add_trace(
        go.Candlestick(
            x=candles.index,
            open=candles['Open'],
            high=candles['High'],
            low=candles['Low'],
            close=candles['Close'],
            name='Candlestick'
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=candles.index[14:],
            y=fast_d,
            mode='lines',
            line={'color': 'blue'},
            name='Fast D'
        ),
        row=2,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=candles.index[14:],
            y=fast_k,
            mode='lines',
            line={'color': 'orange'},
            name='Fast K'
        ),
        row=2,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=candles.index[3:],
            y=rsi,
            mode='lines',
            line={'color': 'black'},
            name='RSI'
        ),
        row=3,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=candles.index[3:],
            y=[30 for _ in range(len(candles.index[3:]))],
            mode='lines',
            line={'color': 'green'},
            name='Oversold (30%)'
        ),
        row=3,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=candles.index[3:],
            y=[70 for _ in range(len(candles.index[3:]))],
            mode='lines',
            line={'color': 'red'},
            name='Overbought (70%)'
        ),
        row=3,
        col=1
    )

    fig.update_xaxes(
        rangeslider_visible=False,
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

    st.plotly_chart(fig)


if __name__ == '__main__':
    start = time.time()

    tick = input("Input Ticker: ")
    s = datetime(datetime.today().year - 1, 1, 1)
    e = datetime.today()

    df = pd.DataFrame(requests.get('https://finnhub.io/api/v1/stock/candle?symbol=' + tick + '&resolution=D&' +
                                   'from=' + str(int(s.timestamp())) +
                                   '&to=' + str(int(e.timestamp())) +
                                   '&token=' + API_KEY).json()).drop(axis=1, labels='s')
    df = pd.DataFrame({
        'Date': pd.to_datetime(df['t']),
        'Open': df['o'],
        'High': df['h'],
        'Low': df['l'],
        'Close': df['c'],
        'Volume': df['v'],
    })

    d = {'token': API_KEY,
         'ticker': tick,
         'startDate': s,
         'endDate': e,
         'candles': df.set_index('Date')}

    run(d)
    print("     --- Finished in %s seconds ---      " % round(time.time() - start, 2))
