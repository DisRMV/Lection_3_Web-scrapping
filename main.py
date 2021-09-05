import re
import requests
from bs4 import BeautifulSoup

KEYWORDS = ['PHP*', 'IT-компании', 'Карьера в IT-индустрии', 'Список', 'Процесс']
URL = 'https://habr.com/ru/all/'


def get_html_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, features='html.parser') if response.ok else response.status_code


def get_hubs(article):
    hubs = article.find_all(class_='tm-article-snippet__hubs-item')
    return {hub.text.strip() for hub in hubs}


def get_article_list(url):
    soup = get_html_soup(url)
    articles = soup.find_all('article')
    return [
        'https://habr.com' + article.find('a', class_='tm-article-snippet__title-link').attrs.get('href')
        for article in articles
    ]


def get_articles_with_preview(url, keywords):
    soup = get_html_soup(url)
    articles = soup.find_all('article')
    for article in articles:
        hubs_set = get_hubs(article)
        if hubs_set & set(keywords):
            article_date = article.find(class_='tm-article-snippet__meta').find('time').attrs.get('title')
            article_title = article.find(class_='tm-article-snippet__title-link').find('span')
            article_href = article.find('a', class_='tm-article-snippet__title-link').attrs.get('href')
            print(article_date)
            print(article_title.text)
            print('https://habr.com' + article_href)
            print('-------')
    return print('Search with preview ended')


def get_articles_with_text(url_list, keywords):
    for url in url_list:
        soup = get_html_soup(url)
        text = soup.find('div', id="post-content-body")
        hubs_set = get_hubs(soup)
        for word in keywords:
            if re.findall(word, text.text) and not hubs_set & set(keywords):
                article_date = soup.find(class_='tm-article-snippet__meta').find('time').attrs.get('title')
                article_title = soup.find(class_='tm-article-snippet__title tm-article-snippet__title_h1').find('span')
                print(article_date)
                print(article_title.text)
                print(url)
                print('-------')
                break
    return print('Search with text ended')


if __name__ == '__main__':
    articles_url_list = get_article_list(URL)
    articles_from_hub_search = get_articles_with_preview(URL, KEYWORDS)
    print('****************************')
    articles_from_text_search = get_articles_with_text(articles_url_list, KEYWORDS)

