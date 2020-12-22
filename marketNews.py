# Iain Muir
# iam9ez

from datetime import datetime, timedelta
import plotly.graph_objects as go
from experimentation.research import largestCap
from bs4 import BeautifulSoup
import streamlit as st
import requests
import time
import os

api_key = os.environ["api_key"]
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
            images += "<img src='" + news['image'] + "' height='75'/> --"
            text += "<li><b>" + news['headline'] + "</b> (<a href='" + \
                    news['url'] + "'>" + news['source'] + "</a>)</li>"

    st.markdown(images + "</p>", unsafe_allow_html=True)
    st.markdown(text + "</ul></p>", unsafe_allow_html=True)


def company_news(ticker):
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
        if news['headline'] in headlines or 'http' in news['source']:
            continue
        elif datetime.fromtimestamp(news['datetime']).date() == datetime.today().date():
            images += "<img src='" + news['image'] + "' height='50'/> --"
            text += "<li><b>" + news['headline'] + "</b> (<a href='" + \
                    news['url'] + "'>" + news['source'].title() + "</a>)</li>"
            headlines.append(news['headline'])

    if len(text) == 7 and len(images) == 42:
        st.markdown("<center> No Company News! </center>", unsafe_allow_html=True)
        return

    st.markdown(images + "</p>", unsafe_allow_html=True)
    st.markdown(text + "</ul></p>", unsafe_allow_html=True)


def analyst_sentiments(ticker):
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
                            ticker + '&token=' + api_key).json()
    length = len(analysts)
    if length < 4:
        if length == 0:
            st.markdown("<center> No Analyst Sentiments! </center>", unsafe_allow_html=True)
            return
        else:
            analysts = analysts[:length - 1]
    else:
        analysts = analysts[:2]

    dates, sb, b, h, s, ss = [], [], [], [], [], []
    for analyst in analysts:
        dates.insert(0, datetime.strptime(analyst['period'], '%Y-%m-%d').strftime('%b %d, %Y'))
        sb.insert(0, analyst['strongBuy'])
        b.insert(0, analyst['buy'])
        h.insert(0, analyst['hold'])
        s.insert(0, analyst['sell'])
        ss.insert(0, analyst['strongSell'])

    fig = go.Figure(data=[
        go.Bar(name='Strong Sell', x=dates, y=ss, marker_color='maroon'),
        go.Bar(name='Sell', x=dates, y=s, marker_color='salmon'),
        go.Bar(name='Hold', x=dates, y=h, marker_color='moccasin'),
        go.Bar(name='Buy', x=dates, y=b, marker_color='lightgreen'),
        go.Bar(name='Strong Buy', x=dates, y=sb, marker_color='darkgreen')
    ])
    fig.update_layout(barmode='stack',
                      title_text='Analyst Recommendations (' + ticker + ')',
                      xaxis={'title': 'Period'},
                      yaxis={'title': '# of Analysts'})

    st.plotly_chart(fig)


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
                st.markdown(
                    datetime.strptime(ipo['date'], '%Y-%m-%d').strftime('%b %d, %Y') + " – **" +
                    ipo['name'].title() + '** (' + ipo['symbol'] + ')'
                )
                bold = "**" if ipo['totalSharesValue'] > 1000000000 else ""
                st.markdown(
                    "|----- " + bold + " Valuation: " + money_string(ipo['totalSharesValue']) + " " + bold
                )
        except TypeError:
            # print(ipo['date'], ipo['name'].title())
            continue


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
                            str(date - timedelta(days=30)) + '&' +
                            str(date + timedelta(days=30)) + '&token=' + api_key).json()
    for event in earnings['earningsCalendar']:
        if event['symbol'] not in largestCap:
            continue

        st.markdown(
            "**" + event['symbol'] + "** (Q" + str(event['quarter']) + " " + str(event['year']) + ")"
        )
        st.markdown(
            "* EPS Actual vs. Expected: " + str(event['epsActual']) + " vs. " + str(round(event['epsEstimate'], 2))
        )
        st.markdown(
            "* Revenue Actual vs. Expected: " + money_string(event['revenueActual']) + " vs. " +
            money_string(event['revenueEstimate'])
        )


def run():
    """

    :return
    """

    # start = time.time()

    st.markdown("<h1 style='text-align:center;'> Market News </h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'> Today's Date: " + datetime.today().date().strftime("%B %d, %Y") +
                "</h3>", unsafe_allow_html=True)
    # st.write("------------------------------")  # Spacing

    running_tick = '<center><p class="small">'
    for ticker in ['FB', 'AAPL', 'AMZN', 'NFLX', 'GOOG']:
        quote = requests.get('https://finnhub.io/api/v1/quote?symbol=' + ticker + '&token=' + api_key).json()
        change = round(((quote['c'] - quote['pc']) / quote['pc']) * 100, 2)
        color = 'green' if change > 0 else 'red'

        running_tick += "<b><span style='font-size:7pt'>" + ticker + "</span></b><span style='font-size:8pt'> $" + \
                        str(round(quote['c'], 2)) + "</span> <span style='font-size:7pt;color:" + color + "'>" + \
                        str(round(quote['c'] - quote['pc'], 2)) + " (" + ('+' if change > 0 else "") + str(change) + \
                        "%)\n </span>"

    url = 'https://money.cnn.com/data/commodities/'
    page = requests.get(url=url)
    soup = BeautifulSoup(page.content, 'html.parser')

    for commodity in soup.find_all('tr', class_='commBotRow'):
        c = commodity.td.strong.text
        if c.strip() not in ['Oil  (Light Crude)', 'Gold', 'Silver', 'Corn', "Wheat"]:
            continue
        c = c.replace('  (Light Crude)', '')
        last = commodity.find('td', class_='cnncol3').text
        change = commodity.find('td', class_='cnncol5').text
        pct = commodity.find('td', class_='cnncol6').text
        color = 'green' if "+" in change else 'red'
        running_tick += "<b><span style='font-size:7pt'>" + c + "</span></b><span style='font-size:8pt'> $" + last + \
                        "</span><span style='font-size:7pt;color:" + color + "'> " + change + " (" + pct + ")\n </span>"
    st.markdown(running_tick + "</p></center>", unsafe_allow_html=True)

    for quote in ['BTC-USD?p=BTC-USD&.tsrc=fin-srch', '%5ETNX/']:
        url = 'https://finance.yahoo.com/quote/' + quote
        page = requests.get(url=url)
        soup = BeautifulSoup(page.content, 'html.parser')
        data = soup.find('div', class_='D(ib) Mend(20px)').find_all('span')

        last = data[0].text
        change = data[1].text.split()[0]
        pct = data[1].text.split()[1]
        color = 'green' if "+" in change else 'red'
        # print(last, change, pct)
        running_tick += "<b><span style='font-size:7pt'>" + c + "</span></b><span style='font-size:8pt'> $" + last + \
                        "</span><span style='font-size:7pt;color:" + color + "'> " + change + " (" + pct + ")\n </span>"

    forex = requests.get('https://finnhub.io/api/v1/forex/rates?base=USD&token=').json()['quote']
    eur, gbp, jpy = forex['EUR'], forex['GBP'], forex['JPY']
    print(eur, gbp, jpy)

    # Ticker Bar
    #   Indices, FAANG, Crypto, Commodities, 10 yr Yield, Currency

    st.markdown('------------------------------------------')
    st.subheader("Overall Market News")
    market_news()
    st.markdown('------------------------------------------')
    st.subheader("Company News and Analyst Sentiments")
    tick = st.text_input("Input Ticker:")
    if tick:
        company_news(tick)
        st.markdown('------------------------------------------')
        analyst_sentiments(tick)
    st.markdown('------------------------------------------')
    st.subheader("Earnings Calendar")
    earnings_calendar()
    st.markdown('------------------------------------------')
    st.subheader("IPO Calendar")
    ipo_calendar()


if __name__ == '__main__':
    start = time.time()
    run()
    print("     --- Finished in %s seconds ---      " % round(time.time() - start, 2))
