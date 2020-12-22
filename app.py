"""
Iain Muir, iam9ez

PROJECT DESCRIPTION

TO-DO:
    • Reformat Market News
    • Translate Tickers to Company Names
    • Order Files with Delineated Functions
    • Order IPO Calendar by date
    • Insert Exceptions (everywhere)
    • Financial Statements
    • Iron Condor
    • Remaining Technical Indicators
        • Descriptions of each
    • COVID Data
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
