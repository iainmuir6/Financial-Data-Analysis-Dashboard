# Iain Muir
# iam9ez

from plotly.subplots import make_subplots
import plotly.graph_objects as go
from datetime import datetime
import streamlit as st
import pandas as pd
import requests
import time


def run():
    """

    :return
    """
    api_key = 'bsm4nq7rh5rdb4arch50'

    st.markdown("<h1 style='text-align:center;'> Stock Information </h1>", unsafe_allow_html=True)
    st.write()  # Spacing

    ticker = st.text_input("Enter Ticker: ")

    if ticker:
        quote = requests.get('https://finnhub.io/api/v1/quote?symbol=' + ticker + '&token=' + api_key).json()
        change = round(((quote['c'] - quote['pc']) / quote['pc']) * 100, 2)

        st.markdown("<center> <h3> Current Price: <span style='color: " + ('green' if change > 0 else 'red') + "'> $" +
                    str(round(quote['c'], 2)) + " (" + ('+' if change > 0 else "") + str(change) +
                    "%) </span></h3> </center>", unsafe_allow_html=True)
        st.markdown("<center> Prev. Close: <b> $" + str(round(quote['pc'], 2)) + "</b>  |   Open: <b> $" +
                    str(round(quote['o'], 2)) + "</b>   |    High: <b> $" + str(round(quote['h'], 2)) +
                    "</b>  |   Low: <b> $" + str(round(quote['l'], 2)) + "</b></center>", unsafe_allow_html=True)
        st.write("----------------------------")

        s = datetime(datetime.today().year - 1, 1, 1)
        e = datetime.today()
        api_key = 'bsm4nq7rh5rdb4arch50'

        df = pd.DataFrame(requests.get('https://finnhub.io/api/v1/stock/candle?symbol=' + ticker + '&resolution=D&' +
                                       'from=' + str(int(s.timestamp())) +
                                       '&to=' + str(int(e.timestamp())) +
                                       '&token=' + api_key).json()).drop(axis=1, labels='s')
        df['t'] = [datetime.fromtimestamp(x) for x in df['t']]

        fig = make_subplots(
            specs=[[{"secondary_y": True}]]
        )
        fig.add_trace(
            go.Candlestick(
                x=df['t'].dt.date,
                open=df['o'],
                high=df['h'],
                low=df['l'],
                close=df['c'],
                name='Candlestick'
            ),
            secondary_y=True
        )
        fig.add_trace(
            go.Bar(
                x=df['t'].dt.date,
                y=df['v'],
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
        fig.update_layout(
            title='Historic Stock Data for ' + ticker
        )
        fig.layout.yaxis2.showgrid = False

        st.subheader("Candlestick Data")
        st.plotly_chart(fig)


if __name__ == '__main__':
    start = time.time()
    run()
    print("     --- Finished in %s seconds ---      " % round(time.time() - start, 2))
