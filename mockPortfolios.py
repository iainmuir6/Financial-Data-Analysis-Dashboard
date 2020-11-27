# Iain Muir
# iam9ez

try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

from portfolio import Portfolio
from research import largestCap
from datetime import datetime
import requests
import os

"""
PORTFOLIO DIVERSIFICATION
25 Stocks
    US Stock        (48%)
        Large-Cap       (7 – 28%)
        Small-Cap       (5 – 20%)
    Foreign         (5 – 20%)
    Indices/ETFs    (5 – 20%)
    Options         (3 – 12%)
"""

api_key = 'bsm4nq7rh5rdb4arch50'


def annualized_return(portfolio):
    days = datetime.today().date() - portfolio.creation
    if days == 0 or portfolio.total_cost == 0:
        return None
    nominal_return = portfolio.portfolio_return / portfolio.total_cost
    return (1 + nominal_return) ** (365 / days) - 1


'''
PORTFOLIO A
    Crossover Trading Strategy
    Notes:
        ...
'''
if not os.path.exists("/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles/portfolioA.pickle"):
    p = Portfolio()
    pickle.dump(p, open(
        "/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles/portfolioA.pickle", 'wb'))
    print('Successfully created a mock portfolio!')

else:
    p = pickle.load(open(
        "/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles/portfolioA.pickle", 'rb'))

    # —————————— Investment Decisions ——————————

    # ——————————----------------------——————————

    p.update()
    print("Market Value: $", p.market_value)
    print("Portfolio Return: $", p.portfolio_return)
    print("Annualized Return:", annualized_return(p), "%")
    print("Remaining Cash: $", p.cash)
    print()

    for each in p.stocks.values():
        print(each.company)
        print('\t Ticker: ' + str(each.ticker) + '\n',
              '\t  Price: $' + str(each.current_price) + '\n',
              '\t   Cost: $' + str(each.historic_cost) + '\n',
              '\t Shares: ' + str(each.volume) + '\n',
              '\t Profit: $' + str(each.profit) + '\n')

    pickle.dump(p, open(
        "/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles/portfolioA.pickle", 'wb'))


'''
PORTFOLIO B
    Resistance Levels Strategy
    Notes:
        ...
'''
if not os.path.exists("/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles/portfolioB.pickle"):
    p = Portfolio()
    pickle.dump(p, open(
        "/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles/portfolioB.pickle", 'wb'))
    print('Successfully created a mock portfolio!')

else:
    p = pickle.load(open(
        "/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles/portfolioB.pickle", 'rb'))

    # —————————— Investment Decisions ——————————

    # resolution = 30
    stocks = p.stocks.keys()

    for tick in largestCap:
        levels = requests.get('https://finnhub.io/api/v1/scan/support-resistance?symbol=' + tick +
                              '&resolution=D&token=' + api_key).json()['levels']
        length = len(levels)
        if length == 4:
            s2, s1, r1, r2 = levels
        if length == 5:
            s2, s1, pp, r1, r2 = levels
        if length == 6:
            s3, s2, s1, r1, r2, r3 = levels
        if length == 7:
            s3, s2, s1, pp, r1, r2, r3 = levels
        if length == 8:
            s4, s3, s2, s1, r1, r2, r3, r4 = levels
        if length < 4 or length > 8:
            print(len(levels))
            exit(0)

        current = requests.get(
            'https://finnhub.io/api/v1/quote?symbol=' + tick + '&token=' + api_key).json()['c']
        if tick in stocks:
            if current > r1:
                p.sell(tick)
            else:
                continue
        else:
            if current < s1:
                p.buy(tick)
            else:
                continue

    # ——————————----------------------——————————

    p.update()
    print("Market Value: $", p.market_value)
    print("Portfolio Return: $", p.portfolio_return)
    print("Annualized Return:", annualized_return(p), "%")
    print("Remaining Cash: $", p.cash)
    print()

    for each in p.stocks.values():
        print(each.company)
        print('\t Ticker: ' + str(each.ticker) + '\n',
              '\t  Price: $' + str(each.current_price) + '\n',
              '\t   Cost: $' + str(each.historic_cost) + '\n',
              '\t Shares: ' + str(each.volume) + '\n',
              '\t Profit: $' + str(each.profit) + '\n')

    pickle.dump(p, open(
        "/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles/portfolioB.pickle", 'wb'))
