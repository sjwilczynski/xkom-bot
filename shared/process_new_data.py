from get_data_from_webpage import get_data_from_webpage
import os
from datetime import datetime
from db import insert


def process_new_data_from_webpage():

    [product_name, original_price, new_price,
        percentage_discount, category] = get_data_from_webpage()

    now = datetime.now()
    current_date = now.strftime("%d/%m/%Y %H")

    new_document = {'date': current_date, 'Product name': product_name,
                    'Original price': original_price.amount_text, 'New price': new_price.amount_text, 'Category': category}

    insert(new_document)
