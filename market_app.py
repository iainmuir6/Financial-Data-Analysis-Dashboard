"""
Iain Muir, iam9ez

PROJECT DESCRIPTION

TODO:
    • Insert Exceptions (everywhere)
        • Custom Error Message on Streamlit
    • Documentation
    • Display Progress for Loading
    • Symbol Lookup

streamlit run /Users/iainmuir/PycharmProjects/Desktop/streamlitApp/stockMarket/market_app.py
/Users/iainmuir/PycharmProjects/Desktop/streamlitApp/stockMarket/market_app.py
"""

import streamlit as st

try:
    from stockMarket import marketNews, stockCharts, optionChains, portfolioDashboard, technicalIndicators, market_home
except ModuleNotFoundError:
    import market_home
    import marketNews
    import stockCharts
    import optionChains
    import portfolioDashboard
    import technicalIndicators


def launch():
    pages = {
        "Home": market_home,
        "Market News": marketNews,
        "Portfolio": portfolioDashboard,
        "Stock Charts": stockCharts,
        "Option Chains": optionChains,
        "Technical Indicators": technicalIndicators
    }

    st.sidebar.title("Market Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    page.run()


if __name__ == '__main__':
    launch()
