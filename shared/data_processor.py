from __app__.shared import data_getter, db
import os
from datetime import datetime


def process_new_data_from_webpage():

    [product_name, original_price, new_price,
        percentage_discount, category] = data_getter.get_data_from_webpage()

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d %H")

    new_document = {'date': current_date, 'Product name': product_name,
                    'Original price': original_price.amount_text, 'New price': new_price.amount_text, 'Category': category}

    db.insert(new_document)
    print('Inserted new document: ' + str(new_document))
