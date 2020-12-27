# Iain Muir
# iam9ez

import plotly.graph_objects as go
from bs4 import BeautifulSoup
import streamlit as st
from PIL import Image
import requests
import pickle
import time
import os
import io


def scale_image(image):
    """
    :argument image

    :return height
    """

    height, width = image.height, image.width
    ratio = height / width
    return '50' if ratio >= 1 else str(int(50 * ratio))


def run():
    """

    :return
    """

    st.markdown("<center> "
                "<img src='https://upload.wikimedia.org/wikipedia/en/d/da/Robinhood_%28company%29_logo.svg' "
                "height='50'/> "
                "</center>", unsafe_allow_html=True)
    st.write()
    st.markdown("<h1 style='text-align:center;'> Portfolio </h1>", unsafe_allow_html=True)
    st.write("------------------------------------------")

    if os.path.exists("/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles/portfolioB.pickle"):
        p = pickle.load(open(
            "/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles/portfolioB.pickle", 'rb'))

        # —————————— Investment Decisions ——————————
        investments = False
        # ——————————----------------------——————————

        if investments:
            pickle.dump(p, open(
                "/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles/portfolioB.pickle", 'wb'))

        stocks_col, graph_col = st.beta_columns(2)

        stocks_col.subheader("Current Portfolio")
        graph_col.subheader("Market Value: $" + str(p.market_value))
        graph_col.subheader("Remaining Cash: $" + str(p.cash))
        graph_col.subheader("Portfolio Composition: ")

        for stock in p.stocks.values():
            name = stock.company

            logo = stock.logo
            height = '50'

            if logo == "":
                try:
                    url = "https://en.wikipedia.org/wiki/" + stock.company.replace(" ", "_")
                    page = requests.get(url)
                    soup = BeautifulSoup(page.content, "html.parser")
                    logo = "https:" + soup.find("table", class_='infobox vcard').tbody.tr.td.a.img['src']
                    img = Image.open(io.BytesIO((requests.get(logo)).content))
                    height = scale_image(img)
                except (Exception, ValueError) as e:
                    logo = "https://media-exp1.licdn.com/dms/image/C4D0BAQGpUHuSqzqVkw/company-logo_200_200/0/1550857" \
                           "067943?e=1616630400&v=beta&t=xlDk7EW0NYiubh9SCYB18OUTn0RRdf7wyGXhXcyDmjA"
            else:
                img = Image.open(io.BytesIO((requests.get(logo)).content))
                height = scale_image(img)

            if len(name) > 15:
                name = ' '.join(map(str, name.split()[:name.count(" ") // 2]))

            stocks_col.markdown("<img src='" + logo + "' height='" + height + "' /> " + name + " (" +
                                stock.ticker + ")  -  $" + str(stock.current_price), unsafe_allow_html=True)

            graph_col.markdown("* " + stock.ticker + " - " + str(round(stock.volume, 2)) + " shares")

        fig = go.Figure(
            data=[
                go.Pie(labels=list(p.weight_dict.keys()),
                       values=list(p.weight_dict.values()))
            ]
        )
        fig.update_layout(
            title='Portfolio Composition'
        )
        st.plotly_chart(fig)

    else:
        st.write("Portfolio does not exist...")
        try:
            st.write("\nHere are the contents of the portfolioPickles folder:")
            for file in os.listdir("/Users/iainmuir/PycharmProjects/Desktop/stockMarket/portfolioPickles"):
                st.write("\t" + file)
        except (Exception, FileNotFoundError) as e:
            st.error(
                """
                Portfolio Pickles are either inaccessible or do not exist
                
                """
            )


if __name__ == '__main__':
    start = time.time()
    run()
    print("     --- Finished in %s seconds ---      " % round(time.time() - start, 2))
