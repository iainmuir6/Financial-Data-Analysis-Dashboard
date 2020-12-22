# Iain Muir
# iam9ez

from collections import deque
from datetime import datetime
import pandas as pd
import numpy as np
import requests
import os

api_key = os.environ['api_key']


class Portfolio:
    def __init__(self):
        """
        :argument self.creation – date the portfolio was created
        :argument self.cash – amount of funds remaining
        :argument self.market_value – current market value of the portfolio
        :argument self.portfolio_return – current nominal return (sum of profits - sum of costs)
        :argument self.realized_return – amount of nominal return cashed out
        :argument self.total_cost – amount of money invested
        :argument self.stocks – dictionary of stocks within portfolio
        :argument self.weight_dict – breakdown of the portfolio
        :argument self.record – DataFrame that tracks portfolio changes
        """
        self.creation = datetime.today().date()
        self.cash = 0.0
        self.market_value = 0.0
        self.portfolio_return = 0.0
        self.realized_return = 0.0
        self.total_cost = 0.0
        self.stocks = {}
        self.weight_dict = {}
        self.record = pd.DataFrame({'ticker': [],
                                    "buyDate": [],
                                    "sellDate": [],
                                    "buyPrice": [],
                                    "sellPrice": [],
                                    "shareVolume": [],
                                    "cost": [],
                                    "revenue": []})

    def deposit(self, amount):
        self.cash += float(amount)

    def withdraw(self, amount):
        if float(amount) > self.cash:
            print("NOT ENOUGH FUNDS")
        else:
            self.cash -= float(amount)

    def buy(self, ticker, volume=1.0, cost=None):
        if self.cash == 0.0:
            print("NO FUNDS")
            return

        if cost is not None:
            volume = cost / (requests.get('https://finnhub.io/api/v1/quote?symbol=' +
                                          ticker + '&token=' + api_key).json()['c'])

        s = Stock(ticker, volume)

        if s.historic_cost > self.cash:
            volume = self.cash / s.current_price
            del s
            s = Stock(ticker, volume)

        if ticker not in self.stocks.keys():
            self.stocks[ticker] = s
        else:
            self.stocks[ticker].add(s)

        self.cash -= (s.current_price * volume)
        self.update()

        self.record = self.record.append(pd.DataFrame({'ticker': [ticker],
                                                       "buyDate": [datetime.now().date()],
                                                       "sellDate": [np.NaN],
                                                       "buyPrice": [s.current_price],
                                                       "sellPrice": [np.NaN],
                                                       "shareVolume": [volume],
                                                       "cost": [s.historic_cost],
                                                       "revenue": [np.NaN]}))

        print("Bought:", s.company, "(" + s.ticker + ")")

    def sell(self, ticker, volume=1.0, cost=None):
        current = requests.get(
            'https://finnhub.io/api/v1/quote?symbol=' + ticker + '&token=' + api_key).json()['c']

        if cost is not None:
            volume = cost / current

        if float(volume) == float(self.stocks[ticker].volume):
            self.realized_return += (current * volume) - self.stocks[ticker].historic_cost
            self.stocks.pop(ticker)
            self.weight_dict.pop(ticker)
        elif float(volume) > float(self.stocks[ticker].volume):
            self.realized_return += self.stocks[ticker].subtract(self.stocks[ticker].volume)
        else:
            self.realized_return += self.stocks[ticker].subtract(volume)

        self.cash += (current * volume)
        self.update()

        self.record = self.record.append(pd.DataFrame({'ticker': [ticker],
                                                       "buyDate": [np.NaN],
                                                       "sellDate": [datetime.now().date()],
                                                       "buyPrice": [np.NaN],
                                                       "sellPrice": [current],
                                                       "shareVolume": [volume],
                                                       "cost": [np.NaN],
                                                       "revenue": [current * volume]}))
        print("Sold:", ticker)

    def update(self):
        for stock in self.stocks.values():
            stock.current_price = requests.get(
                'https://finnhub.io/api/v1/quote?symbol=' + stock.ticker + '&token=' + api_key).json()['c']
            stock.profit = round((stock.current_price * stock.volume) - stock.historic_cost, 2)

        self.market_value = round(sum(list(map(lambda s: s.current_price * s.volume, self.stocks.values()))), 2)
        self.portfolio_return = round(sum(list(map(lambda s: s.profit, self.stocks.values()))), 2)
        self.total_cost = round(sum(list(map(lambda s: s.historic_cost, self.stocks.values()))), 2)

        for stock in self.stocks.values():
            self.weight_dict[stock.ticker] = round((stock.current_price * stock.volume) / self.market_value, 2)


class Stock:
    def __init__(self, ticker, volume):
        self.ticker = ticker
        self.company = requests.get(
            'https://finnhub.io/api/v1/stock/profile2?symbol=' + ticker + '&token=' + api_key).json()['name']
        self.current_price = requests.get(
            'https://finnhub.io/api/v1/quote?symbol=' + ticker + '&token=' + api_key).json()['c']
        self.historic_cost = self.current_price * volume
        self.cost_queue = deque([(self.current_price, volume)])
        self.volume = volume
        self.profit = 0.0
        self.logo = requests.get(
            'https://finnhub.io/api/v1/stock/profile2?symbol=' + ticker + '&token=' + api_key).json()['logo']

    def add(self, new_stock):
        self.historic_cost += new_stock.current_price * new_stock.volume
        self.cost_queue.append((new_stock.current_price, new_stock.volume))
        self.volume += new_stock.volume

    def subtract(self, shares_sold):
        removed = 0.0
        ret = 0.0
        cost_sold = 0.0

        while removed != shares_sold:
            if self.cost_queue[0][1] <= (shares_sold - removed):
                item = self.cost_queue.popleft()
                cost, vol = item[0], item[1]
                
                removed += vol
                cost_sold += (cost * vol)
                ret += (self.current_price * vol) - cost_sold
            else:
                cost = self.cost_queue[0][0]
                cost_sold += (cost * (shares_sold - removed))
                ret += (self.current_price * (shares_sold - removed)) - cost_sold
                self.cost_queue[0] = (cost, self.cost_queue[0][1] - (shares_sold - removed))

                removed = shares_sold

        self.volume -= shares_sold
        self.historic_cost -= cost_sold

        return ret
