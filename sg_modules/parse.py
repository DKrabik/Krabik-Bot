import requests
import random
import math
from bs4 import BeautifulSoup
from sg_modules.editor import edit_text

URL = 'https://stopgame.ru/news'
HEADERS = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
           'accept': '*/*'}


def get_html(url, params=None):
    return requests.get(url, headers=HEADERS, params=params)


def get_random_color():
    r = math.floor(random.random() * 255)
    g = math.floor(random.random() * 255)
    b = math.floor(random.random() * 255)
    return r * 65536 + g * 256 + b


def get_content(response):
    soup = BeautifulSoup(response, 'html.parser')
    items = soup.find_all('div', "item article-summary article-summary-card")

    articles = []
    for item in items:
        link = 'https://stopgame.ru' + item.find('div', 'caption caption-bold').find_next('a').get('href')
        article_page = BeautifulSoup(get_html(link).text, 'html.parser')
        title = article_page.find('h1', 'article-title').get_text()
        if title == str(open('sg_modules/Last_Article.txt', 'r').readline()):
            break
        else:
            print("Parsing " + str(items.index(item) + 1) + '/' + str(len(items)))

        text = '\n'.join([p.get_text() for p in article_page.find('section', 'article').find_all('p') if
                          not p.get('class') and (
                                      (p.find('a') and "https://t.co/" not in p.find('a').get('href')) or not p.find('a'))])
        author_img = article_page.find_all('div', 'article-info-item')[0].find_next('div', 'photo').get(
            'style').replace('background-image: url(', '').replace(');', '')
        articles.append({
            'title': title,
            'date': article_page.find_all('div', 'article-info-item')[1].get_text(),
            "tags": item.find('div', 'tags').get_text(),
            "link": link,
            "author": article_page.find('div', 'compact-view').find_next('a').get_text(),
            "author_img": author_img,
            "text": edit_text(text),
            "color": get_random_color(),
            "img": item.find('div', 'image').get('style').replace('background-image: url(', '')[:-2]
        })
    return articles


def parse():
    response = get_html(URL)
    if response.status_code == 200:
        articles = get_content(response.text)
        return articles
    else:
        return 'Error'
