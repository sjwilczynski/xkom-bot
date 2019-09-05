import bs4
import requests
from price_parser import Price

# Constants
NEW_PRICE_CLASS = "new-price"
OLD_PRICE_CLASS = "old-price"
PRODUCT_NAME_ATTRIBUTE = "data-product-name"
HOT_SHOT_ID = "#hotShot"

response = requests.get("https://www.x-kom.pl")
response.raise_for_status()
response_text = bs4.BeautifulSoup(response.text, features="lxml")

hot_shot_subtree = response_text.select(HOT_SHOT_ID)[0]

product_name = hot_shot_subtree.find(attrs={("%s" % PRODUCT_NAME_ATTRIBUTE): True})[PRODUCT_NAME_ATTRIBUTE]
original_price = Price.fromstring(hot_shot_subtree.find(class_=OLD_PRICE_CLASS).text)
new_price = Price.fromstring(hot_shot_subtree.find(class_=NEW_PRICE_CLASS).text)
percentage_discount = str(int((1 - new_price.amount/original_price.amount) * 100)) + "%"

message_text = 'New deal is available: %s. The original price is %s and the new price is %s. %s discount!' % (product_name,
                                                                                                              original_price.amount_text + original_price.currency,
                                                                                                              new_price.amount_text + original_price.currency,
                                                                                                              percentage_discount)
print(message_text)
