import csv
import time
import urllib.parse as urlparse
from datetime import datetime
from logging import getLogger
from typing import List, NamedTuple, Optional
from urllib.parse import parse_qs

import pandas as pd
import requests
from bs4 import BeautifulSoup, ResultSet

logger = getLogger(__name__)


NEXT_PAGE_SELECTOR = "[class='entrylist-readmore js-keyboard-selectable-item'] > a"


def get_response(url, page):
    endpoint = "https://b.hatena.ne.jp/entrylist"
    try:
        r = requests.get(endpoint, params={"url": url, "page": page})
    except requests.exceptions.SSLError:
        r = requests.get(endpoint, params={"url": url}, verify=False)
    return r


def get_soup(response: requests.models.Response) -> BeautifulSoup:
    soup = BeautifulSoup(response.content, "lxml")
    return soup


def get_articles_from_hatebu(soup: BeautifulSoup) -> ResultSet:
    articles = soup.find_all("div", {"class": "entrylist-contents-main"})

    MAX_NUMBER_OF_ARTICLES_IN_ONE_PAGE = 29
    if len(articles) > MAX_NUMBER_OF_ARTICLES_IN_ONE_PAGE:
        logger.error(f"length of articles={len(articles)}")
        raise Exception("length of articles was over 29, Something wrong")
    return articles


def get_all_entrylist(
    url: str, entrylist: list, page_count: Optional[int]
) -> List[BeautifulSoup]:

    time.sleep(1)
    response: requests.models.Response = get_response(url, page_count)
    soup: BeautifulSoup = get_soup(response)
    entrylist.append(soup)
    next_page: list = soup.select_one(NEXT_PAGE_SELECTOR)

    if next_page:
        next_page_url: str = next_page["href"]
        parsed = urlparse.urlparse(next_page_url)
        page_count = parse_qs(parsed.query)["page"][0]
        get_all_entrylist(url, entrylist, page_count)
    return entrylist


class Article(NamedTuple):
    url: str
    published_at: datetime
    hatebu_count: str


def save_url(company_name, urls: Article):
    HEADER = ["article_url", "published_at", "hatebu_count"]
    with open("csv/" + company_name + ".csv", "w+") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        for row in urls:
            writer.writerow([row.url, row.published_at.strftime(
                "%Y-%m-%d %H:%M"), row.hatebu_count])


def main():
    df = pd.read_csv("techbloglist.csv", usecols=["company_name", "url"])
    for row in df.itertuples():
        keyword = row.url
        entrylist: List[BeautifulSoup] = []
        entrylist = get_all_entrylist(keyword, entrylist, page_count=None)
        urls: List[Article] = []
        for entry in entrylist:
            articles: ResultSet = get_articles_from_hatebu(entry)
            for article in articles:
                article_url: str = article.find(
                    "a",
                    {
                        "class": "js-keyboard-openable",
                        "data-gtm-click-label": "entry-info-title",
                        "href": True,
                    },
                )["href"]

                published_date: str = article.find(
                    "li", {"class": "entrylist-contents-date"}
                ).contents[0]
                published_at: datetime = datetime.strptime(
                    published_date, "%Y/%m/%d %H:%M"
                )

                hatebu_count: str = (
                    article.find("a", {"class": "js-keyboard-entry-page-openable"})
                    .select_one("span")
                    .text
                )

                urls.append(Article(article_url, published_at, hatebu_count))

        save_url(row.company_name, urls)


if __name__ == "__main__":
    main()
