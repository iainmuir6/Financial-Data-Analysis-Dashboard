# Iain Muir
# iam9ez

import streamlit as st
import time


def run():
    """

    :return
    """

    # Logos
    st.markdown("<p style='text-align:center;color:white' />"
                "<img src='https://upload.wikimedia.org/wikipedia/en/d/da/Robinhood_%28company%29_logo.svg' "
                "height='35'/>          -"
                "<img src='https://upload.wikimedia.org/wikipedia/commons/d/da/Yahoo_Finance_Logo_2019.svg'"
                "height='100'/>         -"
                "<img src='https://static.finnhub.io/img/finnhub_2020-05-09_20_51/logo/logo-gradient2.png'"
                "height='75'"
                "</p>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;'> Marketplace Information </h1>", unsafe_allow_html=True)
    st.write("\n\n")  # Spacing
    st.markdown(
        """
        
        Welcome to the **Marketplace Morning Scoop.** This dashboard is a one-stop shop for market information and 
        analysis, including the following:
        * **Daily News** - up-to-date news on the overall market, specific companies, and upcoming IPOs and Earnings 
        releases
        * **Portfolio Visualization** – display current portfolio and its historical movement
        * **Stock and Options Trading** – visualize company performance or pull option chain data
        * **Technical Indicators** – analyze a company or index using trend indicators, mean reversion, relative strength, 
        and volume and momentum metric 
        
        Market data is sourced from the [Finnhub.io API](https://finnhub.io/). See the [documentation]
        (https://finnhub.io/docs/api#introduction) for more details on the various endpoints. Endpoints used in this
        project include
        * **Company Profile** – Get general information of a company. You can query by symbol, ISIN or CUSIP.
        * **Market News** – Get latest market news.
        * **Company News** – List latest company news by symbol.
         This endpoint is only available for North American companies.
        * **IPO Calendar** – Get recent and coming IPO.
        * **Earnings Calendar** – Get historical and coming earnings release dating back to 2003.
         You can setup webhook to receive real-time earnings update.
        * **Quote** – Get real-time quote data for US stocks. Constant polling is not recommended.
         Use websocket if you need real-time update.
        * **Candles** – Get candlestick data for stocks going back 25 years for US stocks.
        * **Technical Indicators** – Return technical indicator with price data. List of supported indicators
         can be found 
         [here](https://docs.google.com/spreadsheets/d/1ylUvKHVYN2E87WdwIza8ROaCpd48ggEl1k5i5SgA29k/edit?usp=sharing).
        
        Generalized use:
        
        ```
        import requests
        api_key = "<TOKEN>"
        response = requests.get('https://finnhub.io/api/v1/<ENDPOINT>?
                                symbol=<TICKER>&
                                from=<TIMESTAMP>&
                                to=<TIMESTAMP>&
                                token=<API_KEY>
                   ).json()
        ```
        """
    )


if __name__ == '__main__':
    start = time.time()
    run()
    print("     --- Finished in %s seconds ---      " % round(time.time() - start, 2))
