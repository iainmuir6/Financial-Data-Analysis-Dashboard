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
    "Market News": [marketNews, None],
    "Portfolio": [portfolioDashboard, None],
    "Stock Charts": [stockCharts, None],
    "Option Chains": [optionChains, None],
    "Technical Indicators": [technicalIndicators, None]
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
function = PAGES[selection]

