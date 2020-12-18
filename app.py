# Iain Muir
# iam9ez

import streamlit as st

import home
import marketNews
import stockCharts
import optionChains
import portfolioDashboard
import technicalIndicators

PAGES = {
    "Home": home.welcome(),
    "Market News": marketNews.news(),
    "Portfolio": portfolioDashboard.portfolio(),
    "Stock Charts": stockCharts.charts(),
    "Option Chains": optionChains.chain(),
    "Technical Indicators": technicalIndicators
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
function = PAGES[selection]
