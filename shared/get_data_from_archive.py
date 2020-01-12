from html import unescape
import json
import bs4
import requests
from get_data_from_webpage import get_category
from googlesearch import search, get_random_user_agent
from db import insert

ARCHIVE_URL = "https://goracystrzal.pl/archiwum"


def get_data_from_archive():

    response = requests.get(ARCHIVE_URL)
    response.raise_for_status()
    response_text = bs4.BeautifulSoup(response.text, features="lxml")

    table_subtree = response_text.select("table")[0]

    headings = ['date', 'Product name',
                'Original price', 'New price', 'Category']

    for i, row in enumerate(table_subtree.find_all("tr")[1:]):
        tds = row.find_all("td")
        date = tds[0].text[1:-3]
        product_name = tds[1].text[1:]
        original_price = tds[2].text[1:-3]
        new_price = tds[3].text[1:-3]
        print('Getting category for ' + product_name)
        category = get_category_for_archive_element(product_name)
        new_document = {'date': date, 'Product name': product_name,
                        'Original price': original_price, 'New price': new_price, 'Category': category}
        insert(new_document)
        print(str(i) + ': ' + category + ' saved')


def get_category_for_archive_element(product_name):
    user_agent = get_random_user_agent()
    response = search("xkom " + product_name, start=0,
                      stop=5, num=5, user_agent=user_agent)

    try:
        result = ''
        while 'x-kom' not in result or '.html' not in result:
            result = next(response)
        print(result)
        category = get_category(result)
    except StopIteration:
        category = "Brak"
    return category
