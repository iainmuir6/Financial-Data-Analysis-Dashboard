# Iain Muir
# iam9ez

import pandas as pd
import requests
from collections import deque

api_key = 'bsm4nq7rh5rdb4arch50'


class Portfolio:
    def __init__(self):
        self.cash = 0.0
        self.market_value = 0.0
        self.portfolio_return = 0.0
        self.realized_return = 0.0
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

    def buy(self, ticker, volume=1.0):
        if self.cash == 0.0:
            print("NO FUNDS")
            return

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

        # self.record["ticker"].append(ticker)
        # self.record["buyDate"].append(datetime.now().date())
        # self.record["sellDate"].append(np.NaN)
        # self.record["buyPrice"].append(s.current_price)
        # self.record["sellPrice"].append(np.NaN)
        # self.record["shareVolume"].append(volume)
        # self.record["cost"].append(s.historic_cost)
        # self.record["revenue"].append(np.NaN)

    def sell(self, ticker, volume=1.0):
        current = requests.get(
            'https://finnhub.io/api/v1/quote?symbol=' + ticker + '&token=' + api_key).json()['c']

        if float(volume) == float(self.stocks[ticker].volume):
            self.realized_return += (current * volume) - self.stocks[ticker].historic_cost
            self.stocks.pop(ticker)
            self.weight_dict.pop(ticker)

        else:
            self.realized_return += self.stocks[ticker].subtract(volume)

        self.cash += (current * volume)
        self.update()

        # self.record["ticker"].append(ticker)
        # self.record["buyDate"].append(np.NaN)
        # self.record["sellDate"].append(datetime.now().date())
        # self.record["buyPrice"].append(np.NaN)
        # self.record["sellPrice"].append(s.current_price)
        # self.record["shareVolume"].append(volume)
        # self.record["cost"].append(np.NaN)
        # self.record["revenue"].append(s.current_price * volume)

    def update(self):
        for stock in self.stocks.values():
            stock.current_price = requests.get(
                'https://finnhub.io/api/v1/quote?symbol=' + stock.ticker + '&token=' + api_key).json()['c']
            stock.profit = round((stock.current_price * stock.volume) - stock.historic_cost, 2)

        self.market_value = round(sum(list(map(lambda s: s.current_price * s.volume, self.stocks.values()))), 2)
        self.portfolio_return = round(sum(list(map(lambda s: s.profit, self.stocks.values()))), 2)

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
