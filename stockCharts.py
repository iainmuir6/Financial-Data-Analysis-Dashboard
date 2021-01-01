# Iain Muir
# iam9ez

from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import plotly.graph_objects as go
from bs4 import BeautifulSoup
from constants import API_KEY, S_AND_P
import streamlit as st
import pandas as pd
import requests
import time


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


def create_table(url):
    """
    :argument
    :return
    """

    # TODO Style/Reformat Statement Tables
    # TODO Footnotes

    footnote = ''
    html = """
    <!DOCTYPE html>
    <html>
        <table>
        """

    # <link rel="stylesheet" href="https://github.com/iainmuir6/stockMarket/blob/master/report.css" type="text/css"/>

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    for tr in soup.find('table').find_all('tr', recursive=False):
        html += '<tr>'
        try:
            c = tr['class'][0]
            color = 'lightblue' if 'e' in c else 'white' if 'o' in c else 'CornflowerBlue' if 'h' in c else 'lightgrey'
            underline = True if 'u' in c else False
            for td in tr.find_all('td'):
                # print(td.attrs.keys())
                text = td.text.lower().strip()
                try:
                    strong = td.a.strong
                    bold = True if strong is not None else False
                except (TypeError, AttributeError, KeyError):
                    bold = False

                html += '<td style="background-color:' + color + ';text-align:' +\
                        ('right' if 'num' in td['class'] else 'left') + ';' +\
                        ('border-bottom: 3px;' if underline else '') + '">' + ("<b>" if bold else "") + text.title() + \
                        ("</b>" if bold else "") + '</td>'
        except KeyError:
            if len(tr.find_all('th')) == 0:
                if 'colspan' in list(tr.td.attrs.keys()):
                    footnote += tr.td.text + '\n'
            for th in tr.find_all('th'):
                try:
                    colspan = str(th['colspan'])
                except KeyError:
                    colspan = "1"
                try:
                    rowspan = str(th['rowspan'])
                except KeyError:
                    rowspan = "1"

                text = th.text.strip().title() \
                    if len(th.find_all('div')) == 1 \
                    else ' '.join([div.text.strip().title() for div in th.find_all('div')])

                html += '<th style="background-color:CornflowerBlue;text-align:center;" colspan="' + colspan + \
                        '" rowspan="' + rowspan + '"><b>' + text + '</b></th>'

        html += '</tr>'

    return html + '</table></html>', footnote


def scrape_statements(base, xml):
    content = requests.get(xml).content
    soup = BeautifulSoup(content, 'lxml')
    reports = soup.find('myreports').find_all('report')
    master_reports = {}
    other = {}

    for report in reports[:-2]:
        link = base + report.htmlfilename.text
        name = report.shortname.text.lower()
        if report.menucategory.text == 'Statements':
            key = 'Comprehensive Income Statement' if 'comprehensive' in name \
                else 'Income Statement' if ('operations' in name or 'income' in name) and 'parenthetical' not in name \
                else 'Balance Sheet' if 'balance' in name and 'parenthetical' not in name \
                else "Statement of Shareholder's Equity" if 'shareholder' in name or 'stockholder' in name \
                else 'Statement of Cash Flows' if 'flow' in name \
                else None
            if key is not None:
                master_reports[key] = link
        else:
            other[name.title()] = link

    return master_reports, other


def get_reports(ticker):
    filings = requests.get("https://finnhub.io/api/v1/stock/filings?symbol=" + ticker + "&token=" + API_KEY).json()
    for f in filings:
        if f['form'] == '10-K':
            url = f['reportUrl']
            xml_summary = (url[:url.rfind("/")] + '/FilingSummary.xml').replace('ix?doc=/', '')
            base_url = xml_summary.replace('FilingSummary.xml', '')
            return scrape_statements(base_url, xml_summary)
    if True:
        st.warning('No 10-Ks on file, check below for other reports')


def run():
    """

    :return
    """

    st.markdown("<h1 style='text-align:center;'> Stock Information </h1>", unsafe_allow_html=True)
    st.write()
    ticker = st.selectbox("Input Company ('Other' for small caps):", S_AND_P, index=0)

    if ticker != '--- Select a Company ---':
        ticker = ticker[ticker.rfind('-') + 2:] if ticker != 'Other' else st.text_input("Input Ticker:")
        quote = requests.get('https://finnhub.io/api/v1/quote?symbol=' + ticker + '&token=' + API_KEY).json()
        change = round(((quote['c'] - quote['pc']) / quote['pc']) * 100, 2)
        color = 'green' if change > 0 else 'red'

        st.markdown("<center> <h3> Current Price: <span style='font-size:24pt'> $" +
                    str(round(quote['c'], 2)) + "</span> <span style='font-size:14pt;color: " + color + "'>" +
                    str(round(quote['c'] - quote['pc'], 2)) + " (" + ('+' if change > 0 else "") + str(change) +
                    "%) </span></h3> </center>", unsafe_allow_html=True)
        st.markdown("<center> Prev. Close: <b> $" + str(round(quote['pc'], 2)) + "</b>  |   Open: <b> $" +
                    str(round(quote['o'], 2)) + "</b>   |    High: <b> $" + str(round(quote['h'], 2)) +
                    "</b>  |   Low: <b> $" + str(round(quote['l'], 2)) + "</b></center>", unsafe_allow_html=True)
        st.write("----------------------------")

        s = datetime(datetime.today().year - 1, 1, 1)
        e = datetime.today()

        df = pd.DataFrame(requests.get('https://finnhub.io/api/v1/stock/candle?symbol=' + ticker + '&resolution=D&' +
                                       'from=' + str(int(s.timestamp())) +
                                       '&to=' + str(int(e.timestamp())) +
                                       '&token=' + API_KEY).json()).drop(axis=1, labels='s')
        df['t'] = [datetime.fromtimestamp(x) for x in df['t']]

        fig = make_subplots(
            specs=[[{"secondary_y": True}]]
        )
        fig.add_trace(
            go.Candlestick(
                x=df['t'].dt.date,
                open=df['o'],
                high=df['h'],
                low=df['l'],
                close=df['c'],
                name='Candlestick'
            ),
            secondary_y=True
        )
        fig.add_trace(
            go.Bar(
                x=df['t'].dt.date,
                y=df['v'],
                marker={'color': 'rgb(0,0,0)'},
                name='Volume'
            ),
            secondary_y=False
        )
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangebreaks=[
                dict(bounds=["sat", "sun"])
            ],
            ticklabelmode="period"
        )
        fig.update_layout(
            title='Historic Stock Data for ' + ticker
        )
        fig.layout.yaxis2.showgrid = False

        st.subheader("Candlestick Data")
        st.plotly_chart(fig)

        st.subheader("Financials Summary")

        basic_financials = requests.get('https://finnhub.io/api/v1/stock/metric?symbol=' + ticker +
                                        '&metric=all&token=' + API_KEY).json()
        if bool(basic_financials['series']):
            st.markdown('<u> Basic Financials </u>', unsafe_allow_html=True)

            date = list(basic_financials['series']['annual'].values())[0][0]['period']
            if datetime.today() - datetime.strptime(date, '%Y-%m-%d') < timedelta(days=200):
                st.write("Reported Date: " + date)
            else:
                st.warning("Reported Date: " + date)

            df1 = pd.DataFrame(
                {
                    'Metric': [k for k, v in basic_financials['series']['annual'].items() if len(v) != 0],
                    'Value': [round(v[0]['v'], 4) for v in basic_financials['series']['annual'].values() if len(v) != 0]
                }
            )
            df2 = pd.DataFrame(
                {
                    'Metric': [k for k in basic_financials['metric'].keys()],
                    'Value': [v for v in basic_financials['metric'].values()]
                }
            )

            df = df1.append(df2).reset_index().drop('index', axis=1)
            st.dataframe(df)
            selection = st.selectbox("Select Metric:", df['Metric'].values)
            val = df['Value'][list(df['Metric'].values).index(selection)]

            try:
                val = val.values[0]
            except AttributeError:
                val = val
            st.write(selection + ": " + str(val))

            if st.checkbox("Show Formulas"):
                st.markdown(
                    "* **Cash Ratio:** (Current Assets - Inventory) / Current Liabilities \n"
                    "* **Current Ratio:** Current Assets / Current Liabilities \n"
                    "* **EBIT Per Share:** EBIT / Average Number of Shares Outstanding \n"
                    "* **EPS:** Net Income / Average Number of Shares Outstanding \n"
                    "* **Gross Margin:** (Total Revenue - Cost of Goods Sold) / Total Revenue \n"
                    "* **LT Debt to Total Asset:** LT Debt / Total Assets \n"
                    "* **LT Debt to Total Capital:** LT Debt / (LT Debt + Total Equity) \n"
                    "* **LT Debt to Total Equity:** LT Debt / Total Equity \n"
                    "* **Net Debt to Total Capital:** (ST+LT Debt - Cash) / ((ST+LT Debt - Cash)"
                    " + Total Equity) \n"
                    "* **Net Debt to Total Equity:** (ST Debt + LT Debt - Cash) / Total Equity \n"
                    "* **Net Margin:** Net Income / Total Revenue \n"
                    "* **Operating Margin:** Operating Income (EBIT) / Total Revenue \n"
                    "* **Pretax Margin:** Pretax Income (EBT) / Total Revenue \n"
                    "* **Sales Per Share:** Total Revenue / Average Number of Shares Outstanding  \n"
                    "* **SGA to Sales:** SGA Expense / Total Revenue \n"
                    "* **Debt/Equity Ratio:** (ST Debt + LT Debt + Other Fixed Payments) / Total Equity \n"
                    "* **Total Debt to Total Asset:** (ST Debt + LT Debt + Other Fixed Payments) / Total Assets \n"
                    "* **Total Debt to Total Capital:** Total Debt / (Total Debt + Total Equity) \n"
                )

            st.write("----------------------------")

        st.markdown('<u> Financial Statements </u>', unsafe_allow_html=True)

        r, o = get_reports(ticker)

        statement = st.radio("",
                             ["Income Statement", "Balance Sheet", "Statement of Cash Flows",
                              "Statement of Shareholder's Equity", "Comprehensive Income Statement"])

        url = r[statement]
        st.markdown("<h3 style='text-align:center;color:black'><a href='" + url + "'>" + statement + "</a></h3>",
                    unsafe_allow_html=True)
        html, footnote = create_table(url)
        st.write(html, unsafe_allow_html=True)
        if footnote != '':
            st.markdown('*' + footnote.strip() + '*')
        st.write("----------------------------")

        # page = requests.get(url)
        # soup = BeautifulSoup(page.content, 'lxml')
        # for a in soup.findAll('a'):
        #     a.replaceWithChildren()
        # st.write(soup.find('table'), unsafe_allow_html=True)

        other_report = st.selectbox("Other Filed Reports:", list(o.keys()))
        st.write("Link: " + o[other_report])

        st.write("----------------------------")

        st.subheader("SEC Filings")
        s = datetime.today().date()
        e = s - timedelta(days=365)
        ten_k = ''
        ten_q = ''
        eight_k = ''

        filings = requests.get("https://finnhub.io/api/v1/stock/filings?symbol=" + ticker + "&token=" + API_KEY).json()

        for f in filings:
            if datetime.strptime(f['filedDate'], "%Y-%m-%d %H:%M:%S").date() < e:
                break
            if f['form'] == '10-K':
                ten_k += "* " + datetime.strptime(f['filedDate'], "%Y-%m-%d %H:%M:%S").strftime('%b %m, %Y') + \
                         " – [" + f['form'] + "](" + f['reportUrl'] + ") \n"
            elif f['form'] == '10-Q':
                ten_q += "* " + datetime.strptime(f['filedDate'], "%Y-%m-%d %H:%M:%S").strftime('%b %m, %Y') + \
                         " – [" + f['form'] + "](" + f['reportUrl'] + ") \n"
            elif f['form'] == '8-K':
                eight_k += "* " + datetime.strptime(f['filedDate'], "%Y-%m-%d %H:%M:%S").strftime('%b %m, %Y') + \
                           " – [" + f['form'] + "](" + f['reportUrl'] + ") \n"
            else:
                continue

        st.markdown('<u> Annual Reports </u>', unsafe_allow_html=True)
        st.write(ten_k)
        st.markdown('<u> Quarterly Reports </u>', unsafe_allow_html=True)
        st.write(ten_q)
        st.markdown('<u> Monthly Reports </u>', unsafe_allow_html=True)
        st.write(eight_k)


if __name__ == '__main__':
    start = time.time()
    run()
    print("     --- Finished in %s seconds ---      " % round(time.time() - start, 2))


"""
<html>
    <table>
    <tr>
        <th style="background-color:CornflowerBlue;text-align:center;" colspan="1" rowspan="1">
            <b>Stockholders' Equity Statements - Usd ($) $ In Millions</b></th>
        <th style="background-color:CornflowerBlue;text-align:center;" colspan="2" rowspan="1">
            <b>Total</b></th>
        <th style="background-color:CornflowerBlue;text-align:center;" colspan="1" rowspan="1">
            <b>Common Stock And Paid-In Capital</b></th>
        <th style="background-color:CornflowerBlue;text-align:center;" colspan="1" rowspan="1">
            <b>Retained Earnings</b></th>
        <th style="background-color:CornflowerBlue;text-align:center;" colspan="1" rowspan="1">
            <b>
"""