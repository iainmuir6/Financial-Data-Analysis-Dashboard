# Iain Muir
# iam9ez

from bs4 import BeautifulSoup
import streamlit as st
import requests
import pickle
import os

if os.path.exists("/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles/portfolioB.pickle"):
    p = pickle.load(open(
        "/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles/portfolioB.pickle", 'rb'))

    # Streamlit

    st.markdown("<center> <img src='https://upload.wikimedia.org/wikipedia/en/d/da/Robinhood_%28company%29_logo.svg' />"
                " </center>", unsafe_allow_html=True)
    st.write(" ")

    stocks_col, graph_col = st.beta_columns(2)

    stocks_col.subheader("Current Portfolio")
    for stock in p.stocks.values():
        logo = stock.logo
        height = '50'
        if logo == "":
            try:
                url = "https://en.wikipedia.org/wiki/" + stock.company.replace(" ", "_")
                page = requests.get(url)
                soup = BeautifulSoup(page.content, "html.parser")
                logo = "https://" + soup.find("table", class_='infobox vcard').tbody.tr.td.a.img['src']
                height = '20'
            except (Exception, ValueError) as e:
                print("Could not find logo...")

        stocks_col.markdown("<img src='" + logo + "' height='" + height + "' /> " + stock.company + " (" +
                            stock.ticker + ")  -  $" + str(stock.current_price), unsafe_allow_html=True)

    graph_col.subheader("Market Value: $" + str(p.market_value))

else:
    print("actualPortfolio does not exist...")
    print("\nHere are the contents of the portfolioPickles folder:")
    for file in os.listdir("/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles/"):
        print("\t" + file)
