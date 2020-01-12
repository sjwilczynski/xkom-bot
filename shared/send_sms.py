from twilio.rest import Client
import os
from get_data_from_webpage import get_data_from_webpage


def send_sms():

    [product_name, original_price, new_price,
        percentage_discount, category] = get_data_from_webpage()

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
