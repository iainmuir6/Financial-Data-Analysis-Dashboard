# Iain Muir
# iam9ez

from datetime import datetime, timedelta
import streamlit as st
import requests
import time

api_key = 'bsm4nq7rh5rdb4arch50'
ticker = 'AAPL'
date = datetime.today().date()


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


def market_news():
    """
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
    """

    m_news = requests.get('https://finnhub.io/api/v1/news?category=general&token=' + api_key).json()
    text = "<p><ul>"
    images = "<p style='text-align:center;color:white'/>"
    for news in m_news:
        if datetime.fromtimestamp(news['datetime']).date() == datetime.today().date():
            images += "<img src='" + news['image'] + "' height='120'/> --"
            text += "<li><b>" + news['headline'] + "</b> (<a href='" + \
                    news['url'] + "'>" + news['source'] + "</a>)</li>"

    st.markdown(images + "</p>", unsafe_allow_html=True)
    st.markdown(text + "</ul></p>", unsafe_allow_html=True)


def company_news():
    """
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
    """
    c_news = requests.get('https://finnhub.io/api/v1/company-news?symbol=' + ticker +
                          '&from=' + str((date - timedelta(days=7))) + '&to=' + str(date) +
                          '&token=' + api_key).json()
    text = "<p><ul>"
    images = "<p style='text-align:center;color:white'/>"
    headlines = []
    for news in c_news:
        if news['headline'] in headlines:
            continue
        elif datetime.fromtimestamp(news['datetime']).date() == datetime.today().date():
            images += "<img src='" + news['image'] + "' height='50'/> --"
            text += "<li><b>" + news['headline'] + "</b> (<a href='" + \
                    news['url'] + "'>" + news['source'] + "</a>)</li>"
            headlines.append(news['headline'])

    st.markdown(images + "</p>", unsafe_allow_html=True)
    st.markdown(text + "</ul></p>", unsafe_allow_html=True)


def ipo_calendar():
    """
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
    """
    ipos = requests.get('https://finnhub.io/api/v1/calendar/ipo?from=' + str(date - timedelta(days=7)) +
                        '&to=' + str(date + timedelta(days=30)) + '&token=' + api_key).json()
    for ipo in ipos['ipoCalendar']:
        try:
            if ipo['totalSharesValue'] > 50000000:
                print(ipo['date'], ipo['name'].title(), '(' + ipo['symbol'] +
                      ')  ---  Valuation:', money_string(ipo['totalSharesValue']))
        except TypeError:
            print(ipo['date'], ipo['name'].title())
    print()


def earnings_calendar():
    """
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
    """
    earnings = requests.get('https://finnhub.io/api/v1/calendar/earnings?from=' +
                             str(date) + '&' + str(date + timedelta(days=30)) + '&token=' + api_key).json()
    for event in earnings['earningsCalendar']:
        print(event['symbol'] + " (Q" + str(event['quarter']) + " " + str(event['year']) + ")" +
              "\n\t EPS Actual vs. Expected: ", event['epsActual'], "vs.", str(round(event['epsEstimate'], 2)) +
              "\n\t Revenue Actual vs. Expected: ",
              money_string(event['revenueActual']), "vs.", money_string(event['revenueEstimate']))
    print()


def analyst_sentiments():
    """
        RESPONSE FORMAT:
        [
          {
            "buy": int,
            "hold": int,
            "period": str (date – first of month),
            "sell": int,
            "strongBuy": int,
            "strongSell": int,
            "symbol": str
          },
          ...
        ]
    """
    analysts = requests.get('https://finnhub.io/api/v1/stock/recommendation?symbol=' +
                            ticker + '&token=' + api_key).json()[:2]


def run():
    """

    :return
    """

    # start = time.time()

    st.markdown("<h1 style='text-align:center;'> Market News </h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'> Today's Date: " + datetime.today().date().strftime("%B %d, %Y") +
                "</h3>", unsafe_allow_html=True)
    st.write()  # Spacing
    st.markdown('---------------------')

    # Ticker Bar
    #   Indices, FAANG, Crypto, Commodities

    st.subheader("Overall Market News")
    market_news()
    st.subheader("Company News")
    tick = st.text_input("Input Ticker:")
    if tick:
        company_news()
    # earnings_calendar()
    # ipo_calendar()
    # analyst_sentiments()

    # print('\n   --- Finished in %s seconds ---' % round(time.time() - start, 4))


if __name__ == '__main__':
    start = time.time()
    run()
    print("     --- Finished in %s seconds ---      " % round(time.time() - start, 2))
