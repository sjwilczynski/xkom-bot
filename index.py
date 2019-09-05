from html import unescape

import bs4
import requests
from price_parser import Price
from twilio.rest import Client

# Constants
NEW_PRICE_CLASS = "new-price"
OLD_PRICE_CLASS = "old-price"
PRODUCT_NAME_ATTRIBUTE = "data-product-name"
HOT_SHOT_ID = "#hotShot"
XKOM_URL = "https://www.x-kom.pl"
QUANTITY_LEFT_SOLD_CLASS = "gs-quantity"

response = requests.get(XKOM_URL)
response.raise_for_status()
response_text = bs4.BeautifulSoup(response.text, features="lxml")

hot_shot_subtree = response_text.select(HOT_SHOT_ID)[0]

product_name = unescape(hot_shot_subtree.find(attrs={("%s" % PRODUCT_NAME_ATTRIBUTE): True})[PRODUCT_NAME_ATTRIBUTE])
original_price = Price.fromstring(hot_shot_subtree.find(class_=OLD_PRICE_CLASS).text)
new_price = Price.fromstring(hot_shot_subtree.find(class_=NEW_PRICE_CLASS).text)
percentage_discount = str(int((1 - new_price.amount / original_price.amount) * 100)) + "%"
[items_left, items_sold] = list(map(lambda x: x.text, hot_shot_subtree.find_all(class_=QUANTITY_LEFT_SOLD_CLASS)))

left_items_part = 'By now %s were sold and %s are left.' % (
    items_sold, items_left) if items_left is not None else 'Sold out :('

message_text = 'New deal is available: %s. The original price is %s and the new price is %s. %s discount! ' % (
    product_name,
    original_price.amount_text + original_price.currency,
    new_price.amount_text + original_price.currency,
    percentage_discount) + left_items_part

# TODO - move to environment variables

client = Client(account_sid, auth_token)
# message = client.messages.create(
#     body=message_text,
#     from_=from_number,
#     to=to_number
# )

print(message_text)
