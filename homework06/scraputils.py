import requests  # type: ignore
from bs4 import BeautifulSoup


def extract_news(parser: BeautifulSoup) -> list:
    """Extract news from https://news.ycombinator.com/newest site"""
    news = []
    title_lines = list(
        map(
            lambda x: x.find("span", {"class": "titleline"}),
            parser.findAll("tr", {"class": "athing"}),
        )
    )
    sub_lines = parser.findAll("td", {"class": "subtext"})

    for i in range(len(title_lines)):
        title_line = title_lines[i]
        sub_line = sub_lines[i]
        title = title_line.find("a").text
        author = sub_line.find("a", {"class": "hnuser"}).text
        url = title_line.find("a")["href"]
        if comments := sub_line.findAll("a")[-1].text != "discuss":
            comments = int(comments)
        else:
            comments = 0
        points = sub_line.find("span", {"class": "score"}).text
        news.append(
            {"title": title, "author": author, "url": url, "comments": comments, "points": points}
        )

    return news


def extract_next_page(parser: BeautifulSoup) -> str:
    """Extract next page URL"""
    next_page = parser.find("a", {"class": "morelink"})["href"]
    return next_page


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    for i in range(n_pages):
        response = requests.get(url)
        parser = BeautifulSoup(response.content, "html.parser")
        news.extend(extract_news(parser))
        url = extract_next_page(parser)
    return news
