# Iain Muir
# iam9ez

from technicalIndicators import t
import streamlit as st
import time


def run(data):
    """

    :return
    """

    st.markdown("<h3 style='text-align:center;'> Volume </h3>", unsafe_allow_html=True)
    st.write()  # Spacing


if __name__ == '__main__':
    start = time.time()
    d = {'token': t.token,
         'ticker': t.ticker,
         'startDate': t.start_date,
         'endDate': t.end_date,
         'candles': t.candles}

    run(d)
    print("     --- Finished in %s seconds ---      " % round(time.time() - start, 2))
