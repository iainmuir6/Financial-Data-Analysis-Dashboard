# Iain Muir
# iam9ez

from constants import API_KEY, STATE_CODES, S_AND_P, DOW_JONES, NEWS_LOGOS
from datetime import datetime, timedelta
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import plotly.express as px
import streamlit as st
import pandas as pd
import requests
import time

try:
    from stockMarket import compiler
except ModuleNotFoundError:
    import compiler

# TODO Reformat Market and Company News
# TODO Combine News Compiler

date = datetime.today().date()


def money_string(value: int):
    value = str(value)[::-1]
    v = value[value.find(".") + 1:] if value.find(".") != -1 else value
    s = (''.join(["," + v[i] if i != 0 and i % 3 == 0 else v[i] for i in range(len(v))]) + "$")[::-1]
    return s


def yahoo_finance(endpoint):
    """
    :argument

    :return
    """
    url = 'https://finance.yahoo.com/quote/' + endpoint
    page = requests.get(url=url)
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find('div', class_='D(ib) Mend(20px)').find_all('span')

    last = data[0].text
    change = data[1].text.split()[0]
    pct = data[1].text.split()[1]
    color = 'green' if "+" in change else 'red'

    return last, change, pct, color


def display_news(stories):
    try:
        logo = NEWS_LOGOS[list(stories[0])[0]]
    except KeyError:
        logo = NEWS_LOGOS[list(stories[0])[1]]
    st.markdown("<center><img src='" + logo + "' height='65'/></center>", unsafe_allow_html=True)
    st.write('--------------')

    left, right = st.beta_columns(2)
    for i, story in enumerate(stories):
        try:
            _, _, headline, _, image, link = story
        except ValueError:
            _, _, _, headline, _, image, link = story
        image = str(image)

        col = left if i % 2 == 0 else right
        if image != 'nan':
            col.markdown("<center><img src='" + image + "' height='150'/></center>",
                         unsafe_allow_html=True)
        col.markdown("<center>" + headline + " (<a href='" + link + "'>link</a>)</center>",
                     unsafe_allow_html=True)


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

    m_news = requests.get('https://finnhub.io/api/v1/news?category=general&token=' + API_KEY).json()
    text = "<p><ul>"
    images = "<p style='text-align:center;color:white'/>"
    for news in m_news:
        if datetime.fromtimestamp(news['datetime']).date() == datetime.today().date():
            images += "<img src='" + news['image'] + "' height='75'/> --"
            text += "<li><b>" + news['headline'] + "</b> (<a href='" + \
                    news['url'] + "'>" + news['source'] + "</a>)</li>"

    st.markdown(images + "</p>", unsafe_allow_html=True)
    st.markdown(text + "</ul></p>", unsafe_allow_html=True)


def market_news2():
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

    m_news = requests.get('https://finnhub.io/api/v1/news?category=general&token=' + API_KEY).json()
    left, right = st.beta_columns(2)
    for i, news in enumerate(m_news):
        if datetime.fromtimestamp(news['datetime']).date() == datetime.today().date():
            col = left if i % 2 == 0 else right
            col.markdown("<center><img src='" + news['image'] + "' height='150'/></center>",
                         unsafe_allow_html=True)
            col.markdown(news['headline'] + " (<a href='" + news['url'] + "'>" + news['source'] + "</a>)",
                         unsafe_allow_html=True)


def market_news3():
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

    m_news = requests.get('https://finnhub.io/api/v1/news?category=general&token=' + API_KEY).json()
    for i, news in enumerate(m_news):
        if datetime.fromtimestamp(news['datetime']).date() == datetime.today().date():
            st.markdown("<p><img src='" + news['image'] + "' height='75' align='left'/>" + news['headline'] + "</p>",
                        unsafe_allow_html=True)


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
                          '&token=' + API_KEY).json()
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
                            ticker + '&token=' + API_KEY).json()
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
                        '&to=' + str(date + timedelta(days=30)) + '&token=' + API_KEY).json()
    d = {}
    for ipo in ipos['ipoCalendar']:
        try:
            if ipo['totalSharesValue'] > 50000000:
                ipo_date = datetime.strptime(ipo['date'], '%Y-%m-%d').strftime('%b %d, %Y')
                if ipo_date not in d.keys():
                    d[ipo_date] = [[ipo['name'], ipo['symbol'], ipo['totalSharesValue']]]
                else:
                    d[ipo_date].append([ipo['name'], ipo['symbol'], ipo['totalSharesValue']])
        except TypeError:
            continue

    for d, values in d.items():
        st.markdown("<u>" + d.strip() + '</u>', unsafe_allow_html=True)
        for val in values:
            bold = "**" if val[2] > 1000000000 else ""
            st.markdown(
                "* **" + val[0].title() + '** (' + val[1] + ')  --  ' + bold + money_string(val[2]) + " " + bold
            )


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

    # TODO Link to Earnings Report for Calendar

    earnings = requests.get('https://finnhub.io/api/v1/calendar/earnings?from=' +
                            str(date - timedelta(days=7)) + '&' +
                            str(date + timedelta(days=30)) + '&token=' + API_KEY).json()
    if not any(map(lambda e: e['symbol'] in DOW_JONES, earnings['earningsCalendar'])):
        st.write('No Earnings to Report!')
        return

    for event in earnings['earningsCalendar']:
        if event['symbol'] not in DOW_JONES:
            continue
        company = requests.get('https://finnhub.io/api/v1/stock/profile2?symbol=' + event['symbol'] + '&token=' +
                               API_KEY).json()['name']

        st.markdown(
            "**" + company + "** (Q" + str(event['quarter']) + " " + str(event['year']) + ")"
        )
        st.markdown(
            "* EPS Actual vs. Expected: " + str(event['epsActual']) + " vs. " + str(round(event['epsEstimate'], 2))
        )
        st.markdown(
            "* Revenue Actual vs. Expected: " + money_string(event['revenueActual']) + " vs. " +
            money_string(event['revenueEstimate'])
        )


def covid19():
    """:argument

    """

    # TODO Enhance COVID Data Display
    #         • State data

    states = requests.get('https://finnhub.io/api/v1/covid19/us?token=' + API_KEY).json()
    data = [[s['state'], STATE_CODES[s['state']], s['case'], s['death']]
            for s in states if s['state'] in STATE_CODES.keys()]
    df = pd.DataFrame(data, columns=['State', 'Code', 'Cases', 'Deaths']).set_index('State')

    st.markdown('<center><h2> Total Cases: ' + money_string(df['Cases'].sum())[1:] + '</center></h2>',
                unsafe_allow_html=True)
    st.markdown('<center><h3> Total Deaths: ' + money_string(df['Deaths'].sum())[1:] + '</center></h3>',
                unsafe_allow_html=True)

    st.write("------------------------------")
    selection = st.checkbox("Cases")
    if selection:
        fig = px.choropleth(df['Cases'],
                            locations=df['Code'],
                            locationmode='USA-states',
                            color='Cases',
                            color_continuous_scale='inferno',
                            scope='usa')

        st.plotly_chart(fig)
    selection2 = st.checkbox("Deaths")
    if selection2:
        fig = px.choropleth(df['Deaths'],
                            locations=df['Code'],
                            locationmode='USA-states',
                            color='Deaths',
                            color_continuous_scale='inferno',
                            scope='usa')

        st.plotly_chart(fig)


def run():
    """

    :return
    """

    # start = time.time()
    st.markdown("<h1 style='text-align:center;'> Market News </h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'> Today's Date: " + datetime.today().date().strftime("%B %d, %Y") +
                "</h3>", unsafe_allow_html=True)

    indices = '<center>'
    for item in [('%5EGSPC', 'S&P 500'), ('%5EDJI', "Dow Jones"), ('%5EIXIC', 'Nasdaq'), ('%5ERUT', 'Russell 2000')]:
        endpoint, i = item
        last, change, pct, color = yahoo_finance(endpoint)
        indices += "<b><span style='font-size:6.5pt'>" + i + "</span></b><span style='font-size:7.5pt'> $" + last + \
                   "</span><span style='font-size:6.5pt;color:" + color + "'> " + change + " " + pct + " </span>"
    st.markdown(indices + '</center>', unsafe_allow_html=True)

    faang = '<center>'
    for ticker in ['FB', 'AAPL', 'AMZN', 'NFLX', 'GOOG']:
        quote = requests.get('https://finnhub.io/api/v1/quote?symbol=' + ticker + '&token=' + API_KEY).json()
        change = round(((quote['c'] - quote['pc']) / quote['pc']) * 100, 2)
        color = 'green' if change > 0 else 'red'

        faang += "<b><span style='font-size:7pt'>" + ticker + "</span></b><span style='font-size:8pt'> $" + \
                 str(round(quote['c'], 2)) + "</span> <span style='font-size:7pt;color:" + color + "'>" + \
                 str(round(quote['c'] - quote['pc'], 2)) + " (" + ('+' if change > 0 else "") + str(change) + \
                 "%) </span>"
    st.markdown(faang + '</center>', unsafe_allow_html=True)

    url = 'https://money.cnn.com/data/commodities/'
    page = requests.get(url=url)
    soup = BeautifulSoup(page.content, 'html.parser')

    commodities = '<center>'

    for commodity in soup.find_all('tr', class_='commBotRow'):
        c = commodity.td.strong.text
        if c.strip() not in ['Oil  (Light Crude)', 'Gold', 'Silver', 'Corn', "Wheat"]:
            continue
        c = c.replace('  (Light Crude)', '')
        last = commodity.find('td', class_='cnncol3').text
        change = commodity.find('td', class_='cnncol5').text
        pct = commodity.find('td', class_='cnncol6').text
        color = 'green' if "+" in change else 'red'
        commodities += "<b><span style='font-size:7pt'>" + c + "</span></b><span style='font-size:8pt'> $" + last + \
                       "</span><span style='font-size:7pt;color:" + color + "'> " + change + " (" + pct + ")\n </span>"
    st.markdown(commodities + '</center>', unsafe_allow_html=True)

    other = '<center>'
    for item in [('%5ETNX/', '10yr Yield'), ('BTC-USD?p=BTC-USD', 'Bitcoin')]:
        endpoint, i = item
        last, change, pct, color = yahoo_finance(endpoint)
        other += "<b><span style='font-size:7pt'>" + i + "</span></b><span style='font-size:8pt'> $" + last + \
                 "</span><span style='font-size:7pt;color:" + color + "'> " + change + " " + pct + "\n </span>"

    forex = requests.get('https://finnhub.io/api/v1/forex/rates?base=USD&token=' + API_KEY).json()['quote']
    eur, gbp, jpy, chf, cad = str(round(forex['EUR'], 2)), str(round(forex['GBP'], 2)), str(round(forex['JPY'], 2)), \
                              str(round(forex['CHF'], 2)), str(round(forex['CAD'], 2))
    other += "<b><span style='font-size:7pt'> Euro </span></b><span style='font-size:8pt'>" + eur + " </span>" \
             "<b><span style='font-size:7pt'> Pound " + "</span></b><span style='font-size:8pt'>" + gbp + "</span>" \
             "<b><span style='font-size:7pt'> Yen " + "</span></b><span style='font-size:8pt'>" + jpy + "</span>" \
             "<b><span style='font-size:7pt'> Franc " + "</span></b><span style='font-size:8pt'>" + chf + "</span>" \
             "<b><span style='font-size:7pt'> Loonie " + "</span></b><span style='font-size:8pt'>" + cad + "</span>"
    st.markdown(other + "</center>", unsafe_allow_html=True)

    st.markdown('------------------------------------------')

    st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>',
             unsafe_allow_html=True)

    st.subheader("Market News")
    source = st.radio('News Source', ['Home', 'Associated Press', 'ESPN', 'Financial Times', 'Economist'])
    # news_data = pd.read_csv('stockMarket/news.csv')
    news_data = {
        'Home': compiler.home(),
        'Associated Press': compiler.ap(),
        'ESPN': compiler.espn(),
        'Financial Times': compiler.ft(),
        'Economist': compiler.economist()
    }.get(source, pd.DataFrame.empty)

    if not news_data.empty:
        stories = news_data.query('source == "' + source + '"')
        display_news(stories.values)
    else:
        st.write('Problem collecting and displaying news...')
    st.markdown('------------------------------------------')

    with st.beta_expander('Company News', expanded=False):
        st.subheader("Company News and Analyst Sentiments")
        tick = st.selectbox("Input Company ('Other' for small caps):", S_AND_P, index=0)
        st.markdown('------------------------------------------')
        if tick != '--- Select a Company ---':
            tick = tick[tick.rfind('-') + 2:] if tick != '-- Other --' else st.text_input("Input Ticker:")
            if tick:
                company_news(tick)
                st.markdown('------------------------------------------')
                analyst_sentiments(tick)
    with st.beta_expander('Earnings Calendar', expanded=False):
        st.subheader("Earnings Calendar")
        earnings_calendar()
        st.markdown('------------------------------------------')
    with st.beta_expander('IPO Calendar', expanded=False):
        st.subheader("IPO Calendar")
        ipo_calendar()
        st.markdown('------------------------------------------')
    with st.beta_expander('Coronavirus Data', expanded=False):
        st.subheader("Coronarvirus Data")
        covid19()


if __name__ == '__main__':
    start = time.time()
    run()
    print("     --- Finished in %s seconds ---      " % round(time.time() - start, 2))
