# Iain Muir
# iam9ez

from statsmodels import regression
import matplotlib.pyplot as plt
from datetime import datetime
import statsmodels.api as sm
import pandas as pd
import requests
import time
import os


API_KEY = os.environ['api_key']

industries = {'Industrial Conglomerates': [('3M', 'MMM')],
              'Financial Services': [('American Express', 'AXP'), ('Goldman Sachs', 'GS')],
              'Technology': [('Apple', 'AAPL'), ('IBM', 'IBM'), ('Microsoft', 'MSFT'), ('Visa', 'V')],
              'Aerospace & Defense': [('Boeing', 'BA')],
              'Machinery': [('Caterpillar', 'CAT')],
              'Energy ': [('Chevy', 'CVX')],
              'Communications': [('Cisco', 'CSCO')],
              'Beverages': [('Coke', 'KO')],
              'Media': [('Disney', 'DIS')],
              'Chemicals': [('Dow Chemical', 'DOW')],
              'Pharmaceuticals': [('Exxon', 'ZOM'), ('Johnson & Johnson', 'JNJ'), ('Merck', 'MRK'), ('Pfizer', 'PFE')],
              'Retail': [('Home Depot', 'HD'), ('Wal-Mart', 'WMT'), ('Walgreen', 'WBA')],
              'Semiconductors': [('Intel', 'INTC')],
              'Banking': [('JP Morgan', 'JPM')],
              'Hotels, Restaurants & Leisure': [("McDonald's", 'MCD')],
              'Textiles, Apparel & Luxury Goods': [('Nike', 'NKE')],
              'Consumer products': [('P&G', 'PG')],
              'Insurance': [('Travelers Companies Inc', 'TRV')],
              'Health Care': [('UnitedHealth', 'UNH')],
              'Telecommunication': [('Verizon', 'VZ')]}

betas = {}


def linear_regression(x, y):
    x = sm.add_constant(x)
    model = regression.linear_model.OLS(y, x).fit()
    return model.params[0], model.params[1]


start = time.time()

sdate = datetime(2020, 1, 1)
edate = datetime.today()

spy = requests.get('https://finnhub.io/api/v1/stock/candle?symbol=SPY&resolution=D&from=' +
                   str(int(sdate.timestamp())) + '&to=' + str(int(edate.timestamp())) + '&token=' + API_KEY).json()
return_spy = pd.Series(spy['c']).pct_change()[1:]
X = return_spy.values


for industry, companies in industries.items():
    beta_list = []
    for company in companies:
        name = company[0]
        ticker = company[1]
        df = requests.get('https://finnhub.io/api/v1/stock/candle?symbol=' + ticker +
                          '&resolution=D&from=' + str(int(sdate.timestamp())) +
                          '&to=' + str(int(edate.timestamp())) + '&token=' + API_KEY).json()
        return_val = pd.Series(df['c']).pct_change()[1:]
        Y = return_val.values

        try:
            alpha, beta = linear_regression(X, Y)
            print(name, beta)
        except ValueError:
            alpha, beta = linear_regression(X, Y[:len(X)])
            print(name, beta)

        beta_list.append(beta)
        plt.scatter(X, Y)
        plt.show()
        exit(0)

    betas[industry] = [sum(beta_list)/len(beta_list), beta_list]

print(betas)
