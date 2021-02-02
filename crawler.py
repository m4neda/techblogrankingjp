from typing import Dict, List, Optional, NamedTuple, TypedDict, Final
import csv
import requests
from bs4 import BeautifulSoup, ResultSet, Tag
import time
from logging import getLogger
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import datetime
import pandas as pd
logger = getLogger(__name__)


NEXT_PAGE_SELECTOR = "[class='entrylist-readmore js-keyboard-selectable-item'] > a"


def get_keywords_for_search(file_name: str) -> list[str]:
    with open(file_name) as f:
        keyword_list = [s.rstrip() for s in f.readlines()]
    return keyword_list


def get_response(url, page):
    endpoint = 'https://b.hatena.ne.jp/entrylist'
    try:
        r = requests.get(
            endpoint,
            params={
                'url': url,
                'page': page,
                'sort': 'eid'})
    except requests.exceptions.SSLError:
        r = requests.get(
            endpoint,
            params={
                'url': url,
                'sort': 'eid'},
            verify=False)
    time.sleep(1)
    return r


def get_soup(response: requests.models.Response) -> BeautifulSoup:
    soup = BeautifulSoup(response.content, 'lxml')
    return soup


def get_articles_from_hatebu(soup: BeautifulSoup) -> ResultSet:
    articles = soup.find_all('div', {'class': 'entrylist-contents-main'})

    MAX_NUMBER_OF_ARTICLES_IN_ONE_PAGE = 29
    if len(articles) > MAX_NUMBER_OF_ARTICLES_IN_ONE_PAGE:
        logger.error(f"length of articles={len(articles)}")
        raise Exception('length of articles was over 29, Something wrong')
    return articles


def get_all_entrylist(
        url: str,
        entrylist: list,
        page_count: Optional[int]) -> List[BeautifulSoup]:

    response: requests.models.Response = get_response(url, page_count)
    soup: BeautifulSoup = get_soup(response)
    entrylist.append(soup)
    next_page: list = soup.select_one(NEXT_PAGE_SELECTOR)
    # return only one for test
    return entrylist
    if next_page:
        next_page_url: str = next_page['href']
        parsed = urlparse.urlparse(next_page_url)
        page_count = parse_qs(parsed.query)['page'][0]
        get_all_entrylist(url, entrylist, page_count)
    return entrylist


class Article(NamedTuple):
    url: str
    published_at: datetime
    hatebu_count: str


def save_url(keyword, urls: Article):
    HEADER = [
        'url',
        'published_at',
        'hatebu_count'
    ]
    with open(keyword + '.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        for row in urls:
            writer.writerow(
                [row.url, row.published_at.strftime('%Y-%m-%d %H:%M')])


def main():
    keywords: List[str] = get_keywords_for_search(
        file_name='hatena_keyword.txt')
    # pick one for test
    keyword = keywords[0]

    entrylist: List[BeautifulSoup] = []
    entrylist = get_all_entrylist(keyword, entrylist, page_count=None)
    for entry in entrylist:
        articles: ResultSet = get_articles_from_hatebu(entry)
        urls: List[Article] = []
        for article in articles:
            article_url: str = article.find('a',
                                            {'class': 'js-keyboard-openable',
                                             'data-gtm-click-label': 'entry-info-title',
                                             'href': True})['href']
            published_date: str = article.find(
                'li', {'class': 'entrylist-contents-date'}).contents[0]
            published_at: datetime = datetime.strptime(
                published_date, '%Y/%m/%d %H:%M')

            hatebu_count: str = article.find(
                'a', {'class': 'js-keyboard-entry-page-openable'}).select_one("span").text

            urls.append(Article(article_url, published_at, hatebu_count))
        save_url(keyword, urls)


if __name__ == '__main__':
    main()
