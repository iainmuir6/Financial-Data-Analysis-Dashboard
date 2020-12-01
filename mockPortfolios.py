# Iain Muir
# iam9ez

try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

from datetime import datetime, timedelta
from portfolio import Portfolio
from research import largestCap
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
        str(int((datetime.today() - timedelta(days=30)).timestamp())) +
        '&to=' + str(int((datetime.today()).timestamp())) + '&token=' + api_key).json()

    high = max(candle['h'])
    low = min(candle['l'])
    close = candle['c'][0]
    pivot_point = (high + low + close) / 3
    resistance1 = 2 * pivot_point - low
    support1 = 2 * pivot_point - high
    resistance2 = (pivot_point - support1) + resistance1
    support2 = pivot_point - (resistance1 - support1)
    resistance3 = (pivot_point - support2) + resistance2
    support3 = pivot_point - (resistance2 - support2)
    return [support3, support2, support1, pivot_point, resistance1, resistance2, resistance3]


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
        s3, s2, s1, pp, r1, r2, r3 = support_resistance(tick)

        current = requests.get(
            'https://finnhub.io/api/v1/quote?symbol=' + tick + '&token=' + api_key).json()['c']
        # print(tick, "---", current, s1)
        
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
