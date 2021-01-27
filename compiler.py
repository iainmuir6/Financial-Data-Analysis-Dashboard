# Iain Muir
# iam9ez

from bs4 import BeautifulSoup
from constants import API_KEY
from datetime import datetime
import streamlit as st
import pandas as pd
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
    """
    6-8 second request time...
    """

    start = time.time()

    url = "https://www.washingtonpost.com/"
    page = requests.get(url)
    print('page load in %s seconds' % (time.time() - start))
    soup = BeautifulSoup(page.content, "html.parser")
    classes = [
        'no-wrap-text left art-size--lg',
        'no-wrap-text left art-size--fullWidth',
        'wrap-text left art-size--sm',
        'wrap-text left art-size--md'
    ]

    data = []
    stories = []
    for class_ in classes:
        stories += soup.find_all('div', class_=class_)
    print('loop in %s seconds' % (time.time() - start))

    for story in stories:
        try:
            headline = story.find('div', class_='relative gray-darkest pb-xs').text
            link = story.find_all('a')[0]['href']
            section = link.split('/')[3]
            description = story.find('div', class_='bb pb-xs font--subhead 1h-fronts-sm font-light gray-dark ')
            description = description.text if description is not None else None
            image = story.find('img')
            image = image['src'] if image is not None else None
        except (AttributeError, Exception):
            continue

        data.append(['Washington Post', section, headline, description, image, link])

    print(' --- Finished Washington Post in %s seconds ---' % (time.time() - start))
    return data


def espn():
    start = time.time()

    url = 'https://www.espn.com/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    data = []
    stacks = soup.find_all('div', class_='headlineStack')
    for stack in stacks:
        try:
            headler = stack.header.text
            stories = stack.section.ul.find_all('li')
            for story in stories:
                headline = story.text
                link = url + story.a['href'][1:]
                data.append(['ESPN', None, headline, None, None, link])

        except AttributeError:
            continue

    print(' --- Finished ESPN in %s seconds ---' % (time.time() - start))
    return data


def barron():
    start = time.time()

    url = 'https://www.barrons.com/?mod=errorpage'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    articles = soup.find_all('article', class_='BarronsTheme--story--13Re0lAk')

    for article in articles:
        print(article)

    print(' --- Finished Barrons in %s seconds ---' % (time.time() - start))


def economist():
    start = time.time()

    url = 'https://www.economist.com/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    data = []
    articles = [item for item in soup.find_all('div') if 'data-test-id' in item.attrs]

    for article in articles:
        info = article.div
        try:
            section = info.a.text
        except AttributeError:
            continue
        headline = info.h3.text
        link = url + info.h3.a['href']
        description = info.p.text if info.p is not None else None
        image = article.find('div', class_='teaser__image')
        image = image.img['src'] if image is not None else article.find('div', class_='collection-item__image') \
            if article.find('div', class_='collection-item__image') is not None else None

        data.append(['Economist', section, headline, description, image, link])

    print(' --- Finished Economist in %s seconds ---' % (time.time() - start))
    return data


def ft():
    start = time.time()

    url = 'https://www.ft.com/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    articles = soup.find_all('div', class_='o-teaser__content')
    images = soup.find_all('div', class_='o-teaser__image-container js-teaser-image-container')

    img = []
    for image in images:
        id_ = image.a['href'][9:]
        try:
            link = image.a.div.img['src']
        except KeyError:
            link = image.a.div.img['data-src']
        img.append([link, id_])
    image_df = pd.DataFrame(img, columns=['link', 'id'])

    data = []
    for article in articles:
        section = article.div.a.text
        info = article.find('div', class_='o-teaser__heading')
        headline = info.a.text
        extension = info.a['href'][1:]
        link = url + extension
        story_id = extension[extension.rfind('/') + 1:]
        description = article.p.text if article.p is not None else None

        try:
            image = list(image_df.query('id == "' + story_id + '"')['link'])[0]
        except IndexError:
            image = None

        data.append(['Financial Times', section, headline, description, image, link])

    print(' --- Finished Financial Times in %s seconds ---' % (time.time() - start))
    return data


if __name__ == '__main__':
    start_time = time.time()

    d = []
    d += espn()
    d += ft()
    d += economist()

    df = pd.DataFrame(d, columns=['source', 'section', 'headline', 'description', 'image', 'link'])
    df.to_csv('/Users/iainmuir/PycharmProjects/Desktop/streamlitApp/stockMarket/news.csv')

    print('\n\n --- Finished Compilation in %s seconds ---' % (time.time() - start_time))

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
