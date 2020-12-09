# Iain Muir
# iam9ez

import streamlit as st
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
        print(stock.logo)
        stocks_col.markdown("<img src='" + stock.logo + "' height='40' /> " + stock.company + " (" + stock.ticker +
                            ")  -  $" + str(stock.current_price), unsafe_allow_html=True)

    graph_col.subheader("Market Value: $" + str(p.market_value))

else:
    print("actualPortfolio does not exist...")
    print("\nHere are the contents of the portfolioPickles folder:")
    for file in os.listdir("/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles/"):
        print("\t" + file)
