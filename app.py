"""
Iain Muir, iam9ez

PROJECT DESCRIPTION

TO-DO:
    • Reformat Market News
    • Order Files with Functions
    • Insert Exceptions (everywhere)
    • Iron Condor
    • Remaining Technical Indicators
        • Descriptions of each
    • COVID Data
    • Documentation

streamlit run /Users/iainmuir/PycharmProjects/Desktop/stockMarket/app.py
"""

import streamlit as st

import home
import marketNews
import stockCharts
import optionChains
import portfolioDashboard
import technicalIndicators

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
