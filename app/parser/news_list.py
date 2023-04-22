import requests
from bs4 import BeautifulSoup

news_links = []
result = requests.get("https://news.google.com/hom")
soup = BeautifulSoup(result.text, "html.parser")
for link in soup.findAll('a', class_="WwrzSb"):
    news_links.append(link.get("href"))
print(news_links)

