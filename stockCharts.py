# Iain Muir
# iam9ez

from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import plotly.graph_objects as go
from constants import API_KEY
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


def run():
    """

    :return
    """

    st.markdown("<h1 style='text-align:center;'> Stock Information </h1>", unsafe_allow_html=True)
    st.write()  # Spacing

    ticker = st.text_input("Enter Ticker: ")

    if ticker:
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
        st.markdown('<u> Basic Financials </u>', unsafe_allow_html=True)
        basic_financials = requests.get('https://finnhub.io/api/v1/stock/metric?symbol=' + ticker +
                                        '&metric=all&token=' + API_KEY).json()
        st.write("Reported Date: " + str(list(basic_financials['series']['annual'].values())[0][0]['period']))

        df1 = pd.DataFrame(
            {
                'Metric': [k for k in basic_financials['series']['annual'].keys()],
                'Value': [round(v[0]['v'], 4) for v in basic_financials['series']['annual'].values()]
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
        financial_statements = requests.get('https://finnhub.io/api/v1/stock/financials-reported?symbol=' + ticker +
                                            '&token=' + API_KEY).json()['data'][0]['report']
        bs, cf, ic = financial_statements['bs'], financial_statements['cf'], financial_statements['ic']

        if st.checkbox("Show Balance Sheet"):
            st.markdown("<h3 style='text-align:center;'> Balance Sheet </h3>", unsafe_allow_html=True)
            assets, liability_se = st.beta_columns(2)
            assets.subheader("Assets")
            liability_se.subheader("Liabilities and Sharholders Equity")

            a = True
            total_assets = 0
            total_liabilities = 0

            for item in bs:
                bold = False
                if item['value'] == 'N/A':
                    continue
                elif a:
                    if item['label'] == 'ASSETS:':
                        assets.markdown('<center><u> Total Assets: ' + money_string(total_assets) + '</u></center>',
                                        unsafe_allow_html=True)
                        a = False
                        continue
                    elif item['label'] == 'Current assets:' or item['label'] == 'Total non-current assets':
                        total_assets += item['value']
                        bold = True
                    assets.markdown("<p style='font-size:" + ('8' if len(item['label']) > 40 else '10') + "pt;'>  " +
                                    ("<b>" if bold else "") + item['label'].title() + "<span style='float:right'> " +
                                    money_string(item['value']) + "</span>" + ("</b>" if bold else "") + "</p>",
                                    unsafe_allow_html=True)
                else:
                    if 'LIABILITIES AND SHAREHOLDERS' in item['label']:
                        if item['concept'] == 'Liabilities':
                            liability_se.markdown('<center><u> Total Liabilities: ' + money_string(total_liabilities) +
                                                  '</u></center>', unsafe_allow_html=True)
                            continue
                        else:
                            liability_se.markdown('<center><u> Total Sharholders Equity: ' +
                                                  money_string(item['value'] - total_liabilities) + '</u></center>',
                                                  unsafe_allow_html=True)
                            break
                    elif item['label'] == 'Total current liabilities' or item['label'] == 'Total non-current liabilities':
                        total_liabilities += item['value']
                        bold = True
                    elif item['label'] == 'Retained earnings':
                        bold = True
                    elif 'Common stock and additional paid-in capital' in item['label']:
                        item['label'] = 'Common stock and additional paid-in capital'
                        bold = True

                    liability_se.markdown("<p style='font-size:" + ('8' if len(item['label']) > 40 else '10') +
                                          "pt;'>  " + ("<b>" if bold else "") + item['label'].title() +
                                          "<span style='float:right'> " + money_string(item['value']) + "</span>" +
                                          ("</b>" if bold else "") + "</p>", unsafe_allow_html=True)

        if st.checkbox("Show Statement of Cash Flows"):
            st.write("CASH FLOWS")

        if st.checkbox("Show Income Statement"):
            st.write("INCOME STATEMENT")

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
