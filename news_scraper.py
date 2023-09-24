import requests
from bs4 import BeautifulSoup as soupObj
from urllib.parse import urljoin

bbc = "https://www.bbc.com/news/science-environment-56837908"
bbc_base = "https://www.bbc.com"
req = requests.get(bbc)
bbcObj = soupObj(req.content, "lxml")

# For the articles highlited on the page
articles_list = []
article_containers = bbcObj.findAll("div", {"class": "gs-c-promo-body"})
for container in article_containers:
    relative_link = container.find("a", {"class": "gs-c-promo-heading"})["href"]
    absolute_link = urljoin(bbc_base, relative_link)
    headline = container.find(
        "h3",
        {"class": "gs-c-promo-heading__title"},
    ).text
    page = requests.get(absolute_link)
    pageObj = soupObj(page.content, "lxml")
    content = ""
    content_elements = pageObj.findAll(
        "p", {"class": "ssrcss-1q0x1qg-Paragraph e1jhz7w10"}
    )
    for element in content_elements:
        content += element.text.strip()
    articles_dict = {
        "headline": headline,
        "link": absolute_link,
        "content": content,
    }
    articles_list.append(articles_dict)

# For the latest update articles
news_list = []
news_containers = bbcObj.findAll("li", {"class": "lx-stream__post-container"})
for container in news_containers:
    relative_link = container.find("a", {"class": "qa-heading-link"})["href"]
    absolute_link = urljoin(bbc_base, relative_link)
    headline = container.find(
        "span",
        {"class": "lx-stream-post__header-text"},
    ).text
    page = requests.get(absolute_link)
    pageObj = soupObj(page.content, "lxml")
    content = ""
    content_elements = pageObj.findAll(
        "p", {"class": "ssrcss-1q0x1qg-Paragraph e1jhz7w10"}
    )
    for element in content_elements:
        content += element.text.strip()
    news_dict = {
        "headline": headline,
        "link": absolute_link,
        "content": content,
    }
    news_list.append(news_dict)


file = open("bbc.txt", "w")
for article in articles_list:
    headline = article["headline"]
    link = article["link"]
    content = article["content"]

    file.write("Headline: " + headline + "\n")
    file.write("Link: " + link + "\n")
    file.write("Content:\n" + content + "\n\n")

for news in news_list:
    headline = news["headline"]
    link = news["link"]
    content = news["content"]

    file.write("Headline: " + headline + "\n")
    file.write("Link: " + link + "\n")
    file.write("Content:\n" + content + "\n\n")
file.flush()
file.close()
