# Iain Muir
# iam9ez

from selenium import webdriver
from bs4 import BeautifulSoup
from constants import API_KEY
import streamlit as st
from datetime import datetime
import requests
import time


def overall():
    print('home')
    st.write('***')
    m_news = requests.get('https://finnhub.io/api/v1/news?category=general&token=' + API_KEY).json()
    left, right = st.beta_columns(2)
    for i, news in enumerate(m_news):
        if datetime.fromtimestamp(news['datetime']).date() == datetime.today().date():
            col = left if i % 2 == 0 else right
            col.markdown("<center><img src='" + news['image'] + "' height='150'/></center>",
                         unsafe_allow_html=True)
            col.markdown(news['headline'] + " (<a href='" + news['url'] + "'>" + news['source'] + "</a>)",
                         unsafe_allow_html=True)


def wp():
    print('wp')
    st.write(__name__)


def espn():
    print('espn')
    st.write(__name__)


def barron():
    print('barron')
    st.write(__name__)


def economist():
    print('economist')
    st.write(__name__)


# urls = ["https://www.wsj.com/", "https://www.espn.com/", "https://www.washingtonpost.com/regional/",
#         "https://www.barrons.com/", "https://www.economist.com/"]
#
# date = datetime.today().date()
#
# compiled = "<html><head><style> h1 {text-align: center;} </style>" \
#            "<h1 style='color:blue;font-size:200%;'> Compilation of News for " + str(date) + \
#            "\n\n </h1><p style='text-align:center;'>Iain Muir, iam9ez@virginia.edu</p></head><body>" \
#            "<style> p {text-align: left;}</style>"
#
# start_time = time.time()
#
# global i
# for url in urls:
#     if url == "https://www.wsj.com/":
#         continue
#     page = requests.get(url)
#     # print(page.status_code)
#     soup = BeautifulSoup(page.content, "html.parser")
#     index = urls.index(url)
#
#     # ----------------------- WSJ -----------------------
#     if index == 0:
#         driver = webdriver.Chrome('/Users/iainmuir/PycharmProjects/Desktop/Practice/chromedriver')
#         driver.get(url)
#         time.sleep(3)
#         driver.find_element_by_xpath("//a[contains(text(), 'Sign In')]").click()
#
#     # ----------------------- ESPN -----------------------
#     elif index == 1:
#         compiled += "\n <h1> \t\t\t\t----------------------- ESPN ----------------------- </h1>" + "\n"
#
#         stack = soup.find_all("section", class_="headlineStack__listContainer")[1]
#         headlines = stack.find_all("li")
#         for each in headlines:
#             headline = each.a.text
#             link = "https://www.espn.com" + each.a["href"]
#             compiled += "\n<p><strong>" + headline + " - " + "<a href=" + link + "> Link to Article </a></strong></p>\n"
#
#     # ----------------------- Washington Post -----------------------
#     elif index == 2:
#         compiled += "\n <h1> \t\t\t\t----------------------- Washington Post ----------------------- </h1>" + "\n"
#
#         stories = soup.find_all(
#                 "div", class_="no-skin flex-item flex-stack normal-air text-align-left equalize-height-target")[:5]
#         for story in stories:
#             try:
#                 headline = story.h2.a.text
#                 link = story.h2.a["href"]
#             except (Exception, IndexError) as e:
#                 try:
#                     headline = story.h1.a.text
#                     link = story.h1.a["href"]
#                 except (Exception, IndexError) as e:
#                     continue
#             byline = story.ul.text
#             for let in byline:
#                 if let.isdigit():
#                     i = byline.find(let)
#                     break
#             by = byline[:i]
#             time_written = byline[i:]
#             try:
#                 blurb = story.find_all("div")[-1].text
#             except (Exception, IndexError) as e:
#                 blurb = None
#
#             compiled += "\n<p><strong>" + headline + ": " + by +\
#                         " (" + time_written + ") - <a href=" + link + "> Link to Article </a></strong></p>\n"
#
#             if blurb is not None and len(blurb) > 0:
#                 compiled += "<p>      " + blurb + "</p>\n"
#
#     # ----------------------- Barron's -----------------------
#     elif index == 3:
#         compiled += "\n <h1> \t\t\t\t----------------------- Barron's -----------------------  </h1>" + "\n"
#
#         top_news = soup.find_all("article", class_="BarronsTheme--story--13Re0lAk")
#         top_news = top_news[:7]
#         for news in top_news:
#             # try:
#             info = news.find_all("div", class_="BarronsTheme--headline--1Q8XnyIf")
#             for div in info:
#                 if div["class"] == ["BarronsTheme--headline--1Q8XnyIf"]:
#                     try:
#                         link = div.h3.a["href"]
#                         headline = div.h3.a.text
#                         compiled += "<p><strong>" + headline + " - <a href=" + \
#                                     link + "> Link to Article </a></strong></p>\n"
#                     except (Exception, IndexError) as e:
#                         link = div.h2.a["href"]
#                         headline = div.h2.a.text
#                         compiled += "<p><strong>" + headline + " - <a href=" + \
#                                     link + "> Link to Article </a></strong></p>\n"
#             bullets = news.find_all("li")
#             if len(bullets) != 0:
#                 for bullet in bullets:
#                     sub_link = bullet.a["href"]
#                     sub_head = bullet.a.text
#                     compiled += "\n        <li>" + sub_head + " - <a href=" + sub_link + "> Link to Article </a></li>"
#                 compiled += "\n"
#             else:
#                 compiled += "\n"
#
#     # ----------------------- Economist -----------------------
#     elif index == 4:
#         compiled += "\n <h1> \t\t\t\t  ----------------------- Economist ----------------------- </h1> " + "\n"
#
#         articles = soup.find_all("div", class_="teaser__text")[:7]
#         for article in articles:
#             section = article.a.text
#             headline = article.h3.a.text
#             link = "https://www.economist.com/" + article.h3.a["href"]
#             blurb = article.p.text
#
#             compiled += "<p><strong>" + section + ": " + headline + " - <a href=" \
#                         + link + "> Link to Article </a></strong></p>\n"
#             compiled += "<p>\t         " + blurb + "</p>\n"
#
#     compiled += "\n"
#
# print("--- Finished news compilation in %s seconds ---" % (time.time() - start_time))
#
# compiled += "</body></html>"
