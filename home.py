# Iain Muir
# iam9ez

import streamlit as st


def run():
    """

    :return
    """
    st.markdown("<center> <img src='https://img.shields.io/badge/python-100%25-brightgreen' "
                "height='20'/> <img src='https://img.shields.io/badge/implementation-streamlit-orange' "
                "height='20'/> </center>", unsafe_allow_html=True)
    # Logos
    st.markdown("<center>"
                "<img src='https://upload.wikimedia.org/wikipedia/en/d/da/Robinhood_%28company%29_logo.svg' "
                "height='50'/>"
                "<img src='https://upload.wikimedia.org/wikipedia/commons/d/da/Yahoo_Finance_Logo_2019.svg'"
                "height='125'/> "
                "</center>", unsafe_allow_html=True)
    st.write()  # Spacing
    st.markdown("<h1 style='text-align:center;'> Marketplace Information </h1>", unsafe_allow_html=True)
    st.write()  # Spacing


if __name__ == '__main__':
    run()
