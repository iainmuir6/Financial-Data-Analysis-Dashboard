"""
Iain Muir, iam9ez

PROJECT DESCRIPTION

TODO:
    • Order Files with Functions
    • Insert Exceptions (everywhere)
        • Custom Error Message on Streamlit
    • Documentation
    • Display Progress for Loading
    • Caching

streamlit run /Users/iainmuir/PycharmProjects/Desktop/stockMarket/app.py
https://share.streamlit.io/iainmuir6/stockMarket/master/app.py
"""

import streamlit as st

from stockMarket import home, marketNews, stockCharts, optionChains, portfolioDashboard, technicalIndicators


def launch():
    PAGES = {
        "Home": home,
        "Market News": marketNews,
        "Portfolio": portfolioDashboard,
        "Stock Charts": stockCharts,
        "Option Chains": optionChains,
        "Technical Indicators": technicalIndicators
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.run()
