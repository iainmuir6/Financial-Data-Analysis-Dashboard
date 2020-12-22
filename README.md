# Marketplace Information

This dashboard is a one-stop shop for market information and 
analysis, including the following:
* **Daily News** - up-to-date news on the overall market, specific companies, and upcoming IPOs and Earnings 
releases
* **Portfolio Visualization** – display current portfolio and its historical movement
* **Stock and Options Trading** – visualize company performance or pull option chain data
* **Technical Indicators** – analyze a company or index using trend indicators, mean reversion, relative strength, 
and volume and momentum metric 
        
        
Powered by [Streamlit](https://docs.streamlit.io/en/stable/index.html). See the 
[documentation](https://docs.streamlit.io/en/stable/api.html) for more details on its application. Installation:

```
$ pip install streamlit
>>> import streamlit as st
```

Market data is sourced from the [Finnhub.io API](https://finnhub.io/). See the [documentation](https://finnhub.io/docs/api#introduction)
for more details on the various endpoints. Endpoints used in this
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
 
Dashboard is solely programmed and maintained by **Iain A. Muir**; he is currently a third-year student at the 
University of Virginia studying Finance and Information Technology.
* LinkedIn: [Iain Muir](https://www.linkedin.com/in/iain-muir-b37718164/)
* Email: iam9ez@virginia.edu 
