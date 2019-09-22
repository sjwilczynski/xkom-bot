from html import unescape

import bs4
import requests
import os
from price_parser import Price
from twilio.rest import Client

NEW_PRICE_CLASS = "new-price"
OLD_PRICE_CLASS = "old-price"
PRODUCT_NAME_ATTRIBUTE = "data-product-name"
HOT_SHOT_ID = "#hotShot"
XKOM_URL = "https://www.x-kom.pl"
QUANTITY_LEFT_SOLD_CLASS = "gs-quantity"

def send_sms():
    
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

    message_text = '%s. OP: %s, NP: %s. %s disc.! ' % (
        product_name,
        original_price.amount_text + original_price.currency,
        new_price.amount_text + original_price.currency,
        percentage_discount)

    account_sid = os.environ['account_sid']
    auth_token = os.environ['auth_token']
    to_number = os.environ['to_number']
    from_number = os.environ['from_number']

    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message_text,
        from_=from_number,
        to=to_number
    )

    print(message_text)