import requests
from bs4 import BeautifulSoup as soupObj
from urllib.parse import urljoin

vox = "https://www.vox.com/climate"
req = requests.get(vox)
voxObj = soupObj(req.content, "lxml")

# For first page
articles_list = []
article_containers = voxObj.findAll("div", {"class": "c-entry-box--compact__body"})
for container in article_containers:
    obj = container.find("h2", {"class": "c-entry-box--compact__title"})
    link = obj.find("a")["href"]
    # absolute_link = urljoin(vox_base, relative_link)
    headline = obj.find("a").text
    page = requests.get(link)
    pageObj = soupObj(page.content, "lxml")
    content = ""
    content_obj = pageObj.find("div", {"class": "c-entry-content"})
    content_elements = content_obj.findAll("p")
    for element in content_elements:
        content += element.text.strip()
    articles_dict = {
        "headline": headline,
        "link": link,
        "content": content,
    }
    articles_list.append(articles_dict)

# For the more stories articles/ article from climate archives
numPages = 5
news_list = []
for i in range(1, numPages + 1):
    voxArchives = f"https://www.vox.com/climate/archives/{i}"
    req = requests.get(voxArchives)
    voxArchivesObj = soupObj(req.content, "lxml")
    news_containers = voxArchivesObj.findAll(
        "div", {"class": "c-entry-box--compact__body"}
    )
    for container in news_containers:
        obj = container.find("h2", {"class": "c-entry-box--compact__title"})
        link = obj.find("a")["href"]
        # absolute_link = urljoin(vox_base, relative_link)
        headline = obj.find("a").text
        page = requests.get(link)
        pageObj = soupObj(page.content, "lxml")
        content = ""
        content_obj = pageObj.find("div", {"class": "c-entry-content"})
        content_elements = content_obj.findAll("p")
        for element in content_elements:
            content += element.text.strip()
        news_dict = {
            "headline": headline,
            "link": link,
            "content": content,
        }
        news_list.append(news_dict)

file = open("vox.txt", "w", encoding="utf-8")
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
