# Iain Muir
# iam9ez

import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import requests
import os

API_KEY = os.environ['api_key']
# s_date = datetime(2020, 9, 1)

resolution = 30
e_date = datetime.today()
s_date = e_date - timedelta(days=resolution)


def support_resistance(tick):
    """
    Pivot Point = (High + Low + Close) / 3
    Resistance Level 1 = 2 * Pivot Point – Low
    Support Level 1 = 2 * Pivot Point – High
    Resistance Level 2 = (Pivot Point – Support Level 1) + Resistance Level 1
    Support Level 2 = Pivot Point – (Resistance Level 1 – Support Level 1)
    Resistance Level 3 = (Pivot Point – Support Level 2) + Resistance Level 2
    Support Level 3 = Pivot Point – (Resistance Level 2 – Support Level 2)
    """
    candle = requests.get(
        'https://finnhub.io/api/v1/stock/candle?symbol=' + tick + '&resolution=D&from=' +
        str(int(s_date.timestamp())) + '&to=' + str(int(e_date.timestamp())) + '&token=' + API_KEY).json()
    high = max(candle['h'])
    low = min(candle['l'])
    close = candle['c'][0]
    pp = (high + low + close) / 3
    r1 = 2 * pp - low
    s1 = 2 * pp - high
    r2 = (pp - s1) + r1
    s2 = pp - (r1 - s1)
    r3 = (pp - s2) + r2
    s3 = pp - (r2 - s2)
    return candle, [s3, s2, s1, pp, r1, r2, r3]


data, levels = support_resistance('BABA')

df = pd.DataFrame()
df['Date'] = data['t']
df['Open'] = data['o']
df['High'] = data['h']
df['Low'] = data['l']
df['Close'] = data['c']

days = len(df['Date'])

fig = go.Figure(
    data=[go.Candlestick(x=df['Date'],
                         open=df['Open'],
                         high=df['High'],
                         low=df['Low'],
                         close=df['Close']
                         )
          ])


# print(list(df.Date)[-30], levels[0])
fig.add_shape(type='line',
              x0=list(df.Date)[-days], y0=levels[0],
              x1=list(df.Date)[-1], y1=levels[0],
              line=dict(
                  color='black',
                  width=1,
                  dash='dot'
              ))
fig.add_shape(type='line',
              x0=list(df.Date)[-days], y0=levels[1],
              x1=list(df.Date)[-1], y1=levels[1],
              line=dict(
                  color='black',
                  width=1,
                  dash='dot'
              ))
fig.add_shape(type='line',
              x0=list(df.Date)[-days], y0=levels[2],
              x1=list(df.Date)[-1], y1=levels[2],
              line=dict(
                  color='black',
                  width=1,
                  dash='dot'
              ))
fig.add_shape(type='line',
              x0=list(df.Date)[-days], y0=levels[3],
              x1=list(df.Date)[-1], y1=levels[3],
              line=dict(
                  color='black',
                  width=3,
              ))
fig.add_shape(type='line',
              x0=list(df.Date)[-days], y0=levels[4],
              x1=list(df.Date)[-1], y1=levels[4],
              line=dict(
                  color='black',
                  width=1,
                  dash='dot'
              ))

fig.add_shape(type='line',
              x0=list(df.Date)[-days], y0=levels[5],
              x1=list(df.Date)[-1], y1=levels[5],
              line=dict(
                  color='black',
                  width=1,
                  dash='dot'
              ))

fig.add_shape(type='line',
              x0=list(df.Date)[-days], y0=levels[6],
              x1=list(df.Date)[-1], y1=levels[6],
              line=dict(
                  color='black',
                  width=1,
                  dash='dot'
              ))

fig.show()
