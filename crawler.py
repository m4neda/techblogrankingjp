from typing import List
import requests
from bs4 import BeautifulSoup
import time
from logging import getLogger
logger = getLogger(__name__)


def get_keywords_for_search(file_name: str) -> list[str]:
    with open(file_name) as f:
        keyword_list = [s.rstrip() for s in f.readlines()]
    return keyword_list


def get_articles_from_hatebu(url: str) -> BeautifulSoup:
    endpoint = 'https://b.hatena.ne.jp/entrylist'
    try:
        r = requests.get(endpoint, params={'url': url, 'sort': 'eid'})
    except requests.exceptions.SSLError:
        r = requests.get(
            endpoint,
            params={
                'url': url,
                'sort': 'eid'},
            verify=False)
    time.sleep(1)

    soup = BeautifulSoup(r.content, 'lxml')
    articles = soup.find_all('a',
                             {'class': 'js-keyboard-openable',
                              'data-gtm-click-label': 'entry-info-title',
                              'href': True})

    MAX_NUMBER_OF_ARTICLES_IN_ONE_PAGE = 29
    if len(articles) > MAX_NUMBER_OF_ARTICLES_IN_ONE_PAGE:
        logger.error(f"length of articles={len(articles)}")
        raise Exception('length of articles was over 29, Something wrong')
    return soup


def save_article_urls(soup: BeautifulSoup):
    for tag in soup:
        article_url = tag['href']
    pass


def main():
    keywords: List[str] = get_keywords_for_search(
        file_name='hatena_keyword.txt')

    for keyword in keywords:
        soup: BeautifulSoup = get_articles_from_hatebu(url=keyword)

        save_article_urls(soup)


if __name__ == '__main__':
    main()
