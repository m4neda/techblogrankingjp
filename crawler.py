from typing import List
import requests
from bs4 import BeautifulSoup
import time
from logging import getLogger
import urllib.parse as urlparse
from urllib.parse import parse_qs

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


def get_articles_from_hatebu(soup) -> BeautifulSoup:
    articles = soup.find_all('a',
                             {'class': 'js-keyboard-openable',
                              'data-gtm-click-label': 'entry-info-title',
                              'href': True})

    MAX_NUMBER_OF_ARTICLES_IN_ONE_PAGE = 29
    if len(articles) > MAX_NUMBER_OF_ARTICLES_IN_ONE_PAGE:
        logger.error(f"length of articles={len(articles)}")
        raise Exception('length of articles was over 29, Something wrong')
    return articles


def get_all_entrylist(url, entrylist, page_count):
    response: requests.models.Response = get_response(url, page_count)
    soup: BeautifulSoup = get_soup(response)
    entrylist.append(soup)
    nexts: list = soup.select_one(NEXT_PAGE_SELECTOR)
    if nexts:
        next_page_url: str = nexts['href']
        parsed = urlparse.urlparse(next_page_url)
        page_count = parse_qs(parsed.query)['page'][0]
        get_all_entrylist(url, entrylist, page_count)
    return entrylist


def main():
    keywords: List[str] = get_keywords_for_search(
        file_name='hatena_keyword.txt')
    keyword = keywords[0]  # pick one for test
    entrylist: List[BeautifulSoup] = []
    entrylist = get_all_entrylist(keyword, entrylist, page_count=None)
    for entry in entrylist:
        articles = get_articles_from_hatebu(entry)


if __name__ == '__main__':
    main()
