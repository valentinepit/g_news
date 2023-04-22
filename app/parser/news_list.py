import requests
from bs4 import BeautifulSoup


def get_news_links():
    news_links = []
    result = requests.get("https://news.google.com/hom")
    soup = BeautifulSoup(result.text, "html.parser")
    for link in soup.findAll('a', class_="WwrzSb"):
        news_links.append(link.get("href"))
    return news_links
