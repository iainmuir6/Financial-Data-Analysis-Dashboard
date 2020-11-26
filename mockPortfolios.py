# Iain Muir
# iam9ez

try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

from portfolio import Portfolio
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
    Investor Signals Strategy
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

    # ——————————----------------------——————————

    p.update()
    print("Market Value: $", p.market_value)
    print("Portfolio Return: $", p.portfolio_return)
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
