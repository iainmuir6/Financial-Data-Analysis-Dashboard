# Iain Muir
# iam9ez

import matplotlib.pyplot as plt
from datetime import datetime
import requests

api_key = 'bsm4nq7rh5rdb4arch50'

delta = 20
d1 = datetime(2020, 1, 1)
d2 = datetime.today()

url = 'https://finnhub.io/api/v1/indicator?symbol=PLTR&resolution=D&from=' + str(int(d1.timestamp())) + \
      '&to=' + str(int(d2.timestamp())) + '&indicator=bbands&timeperiod=' + str(delta) + '&token=' + api_key

r = requests.get(url=url).json()

plt.plot(r['c'][delta-1:], color='black')
plt.plot(r['lowerband'][delta-1:], color='green')
plt.plot(r['middleband'][delta-1:], color='black', alpha=0.5)
plt.plot(r['upperband'][delta-1:], color='red')
plt.show()
