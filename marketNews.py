# Iain Muir
# iam9ez

from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import requests
import time

api_key = 'bsm4nq7rh5rdb4arch50'
ticker = 'AAPL'
date = datetime.today().date()
start = time.time()


def money_string(value: int):
    string = ""
    value = str(value)[::-1]
    if value.find(".") != -1:
        value = value[value.find(".") + 1:]
    for i in range(len(value)):
        if i != 0 and i % 3 == 0:
            string += "," + value[i]
        else:
            string += value[i]
    return (string + "$")[::-1]


'''
RESPONSE FORMAT:
{
    "category": str,
    "datetime": timestamp,
    "headline": str,
    "id": int,
    "image": str (link),
    "related": str (ticker or blank),
    "source": str (news company),
    "summary": str,
    "url": str (link)
  },

'''
market_news = requests.get('https://finnhub.io/api/v1/news?category=general&token=' + api_key).json()
company_news = requests.get('https://finnhub.io/api/v1/company-news?symbol=' + ticker +
                            '&from=' + str((date - timedelta(days=7))) + '&to=' + str(date) +
                            '&token=' + api_key).json()

'''
RESPONSE FORMAT:
{
  "ipoCalendar": [
    {
      "date": str (date),
      "exchange": str,
      "name": str,
      "numberOfShares": int,
      "price": str (range or exact),
      "status": str,
      "symbol": str,
      "totalSharesValue": int
    },
    ...]
}
'''
ipo_calendar = requests.get('https://finnhub.io/api/v1/calendar/ipo?from=' + str(date - timedelta(days=7)) +
                            '&to=' + str(date + timedelta(days=30)) + '&token=' + api_key).json()

'''
RESPONSE FORMAT:
{
  "earningsCalendar": [
    {
      "date": str (date),
      "epsActual": float,
      "epsEstimate": float,
      "hour": str (bmo, amc, dmh),
      "quarter": int,
      "revenueActual": int,
      "revenueEstimate": int,
      "symbol": str,
      "year": int
    },
    ...]
}
'''
earnings_calendar = requests.get('https://finnhub.io/api/v1/calendar/earnings?from=' +
                                 str(date) + '&' + str(date + timedelta(days=30)) + '&token=' + api_key).json()
for event in earnings_calendar['earningsCalendar']:
    print(event['symbol'] + " (Q" + str(event['quarter']) + " " + str(event['year']) + ")" +
          "\n\t EPS Actual vs. Expected: ", event['epsActual'], "vs.", str(round(event['epsEstimate'], 2)) +
          "\n\t Revenue Actual vs. Expected: ",
          money_string(event['revenueActual']), "vs.", money_string(event['revenueEstimate']))
print()

for ipo in ipo_calendar['ipoCalendar']:
    try:
        if ipo['totalSharesValue'] > 50000000:
            print(ipo['date'], ipo['name'].title(), '(' + ipo['symbol'] +
                  ')  ---  Valuation:', money_string(ipo['totalSharesValue']))
    except TypeError:
        print(ipo['date'], ipo['name'].title())
print()

for news in market_news:
    if datetime.fromtimestamp(news['datetime']).date() == datetime.today().date():
        if news['source'] is None:
            news['source'] = "n/a"

        print(datetime.fromtimestamp(news['datetime']).date(), news['headline'],
              "(" + news['source'] + ") \n\t url: " + news['url'])
print()

for news in company_news:
    if datetime.fromtimestamp(news['datetime']).date() == datetime.today().date():
        if news['source'] is None:
            news['source'] = "n/a"

        print(datetime.fromtimestamp(news['datetime']).date(), news['headline'],
              "(" + news['source'] + ") \n\t url: " + news['url'])
print()

print('\n   --- Finished in %s seconds ---' % round(time.time() - start, 4))
