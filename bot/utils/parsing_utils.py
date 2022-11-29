import time
from random import randint

import requests as req
from bs4 import BeautifulSoup
import lxml
from typing import Any, Text, Dict, List, Tuple


def getHTML(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    res = req.get(url, headers=headers)
    return res

def parsing_article(url: Text) -> Tuple:
    html_code = getHTML('https://theconversation.com/us/arts').text
    soup = BeautifulSoup(html_code, 'lxml')
    articles = soup.find_all('article')
    n = len(articles)
    article = randint(0, n-1)
    link = articles[article].find('a').get('href')

    prefix_link = 'https://theconversation.com'
    article_html_code = getHTML(prefix_link + link).text
    soup_article = BeautifulSoup(article_html_code, 'lxml')
    content = soup_article.find(class_='entry-content')
    title = soup_article.find(class_='content-header-block').text
    title = title.replace('\n', '')
    title = title.replace('\xa0', ' ')
    actual_key = title
    content_dict = {actual_key: []}
    for tag in content:
        if tag.name == 'h2':
            content_dict[tag.text] = []
            actual_key = tag.text
        if tag.name == 'p':
            content_dict[actual_key].append(tag.text)

    return content_dict


async def parsing_dict(word, url):
    # TODO: добавить разные словари
    #url = 'https://www.collinsdictionary.com/dictionary/english/' + word
    html_code = getHTML(url).text
    soup = BeautifulSoup(html_code, 'lxml')
    examples_obj = soup.find_all(class_='cit')
    examples = [exmp.find('quote').text.replace(word, '_____') for exmp in examples_obj]

    def_obj = soup.find(class_="content definitions cobuild br ").find_all(class_='def')
    definitions = [d.text.replace(word, '_____') for d in def_obj]
    return examples, definitions

# ar = ArticleRecipient()
# print(ar.parsing('https://theconversation.com/us/arts'))