# Iain Muir
# iam9ez

from bs4 import BeautifulSoup
from constants import API_KEY
from datetime import datetime
import pandas as pd
import requests
import time


def overall():
    data = []
    data += home()
    data += ap()
    data += espn()
    data += ft()
    data += economist()

    news_df = pd.DataFrame(data, columns=['source', 'section', 'headline', 'description', 'image', 'link'])
    # news_df.to_csv('/Users/iainmuir/PycharmProjects/Desktop/streamlitApp/stockMarket/news.csv')

    return news_df


def home():
    """
        RESPONSE FORMAT:
        {
            "category": str,
            "datetime": timestamp,
            "headline": str,
            "id": int,
            "image": str (link),
            "related": str (ticker or blank),
            "source": str (news company),
            "summary": str,
            "url": str (link)
        },
    """

    m_news = requests.get('https://finnhub.io/api/v1/news?category=general&token=' + API_KEY).json()

    data = []
    for news in m_news:
        if datetime.fromtimestamp(news['datetime']).date() == datetime.today().date():
            data.append(['Home', None, news['headline'], None, news['image'], news['url']])
    return pd.DataFrame(data, columns=['source', 'section', 'headline', 'description', 'image', 'link'])


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

    # print(' --- Finished Washington Post in %s seconds ---' % (time.time() - start))
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

        except (Exception, AttributeError):
            continue

    # print(' --- Finished ESPN in %s seconds ---' % (time.time() - start))
    return pd.DataFrame(data, columns=['source', 'section', 'headline', 'description', 'image', 'link'])


def barron():
    """
    Link loads error page
    """

    start = time.time()

    url = 'https://www.barrons.com/?mod=errorpage'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    articles = soup.find_all('article', class_='BarronsTheme--story--13Re0lAk')

    for article in articles:
        print(article)

    # print(' --- Finished Barrons in %s seconds ---' % (time.time() - start))


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

    # print(' --- Finished Economist in %s seconds ---' % (time.time() - start))
    return pd.DataFrame(data, columns=['source', 'section', 'headline', 'description', 'image', 'link'])


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
        try:
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
        except (Exception, AttributeError):
            continue

    # print(' --- Finished Financial Times in %s seconds ---' % (time.time() - start))
    return pd.DataFrame(data, columns=['source', 'section', 'headline', 'description', 'image', 'link'])


def ap():
    start = time.time()

    url = 'https://apnews.com/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    top_stories = None
    for wrapper in soup.find_all('div', class_='fluid-wrapper'):
        try:
            text = wrapper.div.text
            if text == 'Top stories':
                top_stories = wrapper
                break
        except AttributeError:
            continue

    if top_stories is None:
        return pd.DataFrame.empty

    data = []
    for story in top_stories.find_all('div')[2].find_all('div'):
        try:
            is_story = story['data-tb-region-item']
            if bool(is_story):
                type_ = 'main' if 'main' in story['class'][0] else 'other'

                # section = story.find('a', class_='HubTag') if type_ != 'main' else None
                headline = story.a.h1.text if type_ == 'main' else story.a.div.text
                link = url + story.a['href'][1:]
                try:
                    image = story.find('img')['src']
                except TypeError:
                    image = None
                description = story.find('p').text if type_ == 'main' else None

                data.append(['Associated Press', None, headline, description, image, link])
        except (KeyError, AttributeError):
            continue

    # print(' --- Finished Associated Press in %s seconds ---' % (time.time() - start))
    return pd.DataFrame(data, columns=['source', 'section', 'headline', 'description', 'image', 'link'])


if __name__ == '__main__':
    start_time = time.time()

    overall()

    print('\n\n --- Finished Compilation in %s seconds ---' % (time.time() - start_time))
