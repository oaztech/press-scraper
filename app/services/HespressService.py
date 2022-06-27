import re
import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.hespress.com"


def get_all_categories():
    html_doc = requests.get(BASE_URL).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    details_categories = list()

    categories = soup.select(".nav li a")
    del categories[0]

    for category in categories:
        slug = category.get_attribute_list("href")[0].replace(BASE_URL + "/", "")

        details_categories.append({
            "wording": category.get_text(),
            "slug": slug,
            "url": category.get_attribute_list("href")[0],
            "id": get_category_id(slug)
        })

    return details_categories


def get_category_id(category_slug):
    html_doc = requests.get(
        BASE_URL + "/" + category_slug,
        headers={'User-agent': 'Mozilla/5.0'}
    ).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    script_text = soup \
        .select_one("#listing > script") \
        .get_text() \
        .replace("\n", "") \
        .replace(" ", "") \
        .replace("'", "\"") \
        .replace("parseInt(1)+", "")

    pyload_str = "{" + re.search(r"(?<={).+?(?=})", script_text).group()[:-1] + "}"

    pyload_json = json.loads(pyload_str)

    return pyload_json["id"]


def get_articles_of_category(category_slug, page=1):
    category_id = get_category_id(category_slug)

    html_doc = requests.get(
        BASE_URL,
        params={
            'action': 'ajax_listing',
            'type': 'category',
            'id': category_id,
            'paged': page
        },
        headers={'User-agent': 'Mozilla/5.0'}
    ).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    articles = list()

    for article in soup.select(".col-xl-4"):
        anchor = article.find("a")
        img = article.find("img")
        date = article.find("small")

        articles.append({
            "title": anchor.attrs["title"] if anchor is not None and 'title' in anchor.attrs else "",
            "image": img.attrs["src"] if img is not None and 'src' in img.attrs else "",
            "url": anchor.attrs["href"] if anchor is not None and 'href' in anchor.attrs else "",
            "id": int(re.search(r"-\d+\.html", anchor.attrs["href"]).group()
                .replace("-", "")
                .replace(".html", "")),
            "created_at": date.get_text() if date is not None else ""
        })

    return articles


def get_article(id_article):
    html_doc = requests.get(
        BASE_URL,
        params={'p': id_article},
        headers={'User-agent': 'Mozilla/5.0'}
    ).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    content = ""
    for paragraphe in soup.select("div.article-content > p"):
        content += paragraphe.get_text()

    return {
        "title": soup.find("h1").get_text(),
        "image": soup.select_one(".post-thumbnail img").attrs["src"],
        "author": soup.select_one(".author a").get_text().replace("هسبريس - ", "").strip(),
        "content": content
    }
