# Iain Muir
# iam9ez

from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import requests

api_key = 'bsm4nq7rh5rdb4arch50'

resolution = 30
levels = requests.get('https://finnhub.io/api/v1/scan/support-resistance?symbol=AAPL&resolution=' + str(resolution) +
                      '&token=' + api_key).json()['levels']

s_date = datetime(2020, 9, 1)
e_date = datetime.today()

data = requests.get(
    'https://finnhub.io/api/v1/stock/candle?symbol=AAPL&resolution=D&from=' + str(int(s_date.timestamp())) + '&to=' +
    str(int(e_date.timestamp())) + '&token=' + api_key).json()

df = pd.DataFrame()
df['Date'] = data['t']
df['Open'] = data['o']
df['High'] = data['h']
df['Low'] = data['l']
df['Close'] = data['c']

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
              x0=list(df.Date)[-resolution], y0=levels[0],
              x1=list(df.Date)[-1], y1=levels[0],
              line=dict(
                  color='black',
                  width=1,
                  dash='dot'
              ))
fig.add_shape(type='line',
              x0=list(df.Date)[-resolution], y0=levels[1],
              x1=list(df.Date)[-1], y1=levels[1],
              line=dict(
                  color='black',
                  width=1,
                  dash='dot'
              ))
fig.add_shape(type='line',
              x0=list(df.Date)[-resolution], y0=levels[2],
              x1=list(df.Date)[-1], y1=levels[2],
              line=dict(
                  color='black',
                  width=1,
                  dash='dot'
              ))
fig.add_shape(type='line',
              x0=list(df.Date)[-resolution], y0=levels[3],
              x1=list(df.Date)[-1], y1=levels[3],
              line=dict(
                  color='black',
                  width=1,
                  dash='dot'
              ))
fig.add_shape(type='line',
              x0=list(df.Date)[-resolution], y0=levels[4],
              x1=list(df.Date)[-1], y1=levels[4],
              line=dict(
                  color='black',
                  width=1,
                  dash='dot'
              ))

fig.show()
