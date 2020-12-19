# Iain Muir
# iam9ez

import streamlit as st


def data():
    st.write("Data...")


def run():
    """

    :return
    """

    st.markdown("<h1 style='text-align:center;'> Stock Information </h1>", unsafe_allow_html=True)
    st.write()  # Spacing

    st.text_input("Enter Ticker: ")
    data()
