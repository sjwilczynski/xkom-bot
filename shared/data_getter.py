from html import unescape
import json
import bs4
import requests
from price_parser import Price

NEW_PRICE_CLASS = "new-price"
OLD_PRICE_CLASS = "old-price"
PRODUCT_NAME_ATTRIBUTE = "data-product-name"
HOT_SHOT_ID = "#hotShot"
MAIN_TREE_ID = "#app"
XKOM_URL = "https://www.x-kom.pl"
HOT_SHOT_URL = "https://www.x-kom.pl/goracy_strzal"
QUANTITY_LEFT_SOLD_CLASS = "gs-quantity"
JSON_PROPERTY_BREADCRUMBS_LIST = "itemListElement"
JSON_PROPERTY_CATEGORY = "name"


def get_data_from_webpage():

    response = requests.get(XKOM_URL)
    response.raise_for_status()
    response_text = bs4.BeautifulSoup(response.text, features="lxml")

    hot_shot_subtree = response_text.select(HOT_SHOT_ID)[0]

    product_name = unescape(hot_shot_subtree.find(
        attrs={("%s" % PRODUCT_NAME_ATTRIBUTE): True})[PRODUCT_NAME_ATTRIBUTE])
    original_price = Price.fromstring(
        hot_shot_subtree.find(class_=OLD_PRICE_CLASS).text)
    new_price = Price.fromstring(
        hot_shot_subtree.find(class_=NEW_PRICE_CLASS).text)
    percentage_discount = str(
        int((1 - new_price.amount / original_price.amount) * 100)) + "%"

    category = get_category(HOT_SHOT_URL)

    return [product_name, original_price, new_price, percentage_discount, category]


def get_category(url):
    response = requests.get(url)
    response.raise_for_status()
    response_text = bs4.BeautifulSoup(response.text, features="lxml")

    category = 'Brak'
    try:
        app_tree = response_text.select(MAIN_TREE_ID)[0]

        # Extract category based on HTML page structure - not that reliable
        def does_tag_contain_breadcrumbs(
            tag): return tag.name == 'script' and 'breadcrumb' in tag.text.lower()
        script_tag_to_json = json.loads(
            app_tree.find(does_tag_contain_breadcrumbs).text)
        category = script_tag_to_json[JSON_PROPERTY_BREADCRUMBS_LIST][-1][JSON_PROPERTY_CATEGORY]
    except Exception as e:
        print(e)

    return category
