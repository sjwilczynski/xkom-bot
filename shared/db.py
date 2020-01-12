from pymongo import MongoClient
import os

MONGO_URL = os.environ['mongo_url']
MONGO_USERNAME = os.environ['mongo_username']
MONGO_PASSWORD = os.environ['mongo_password']


def insert(element):
    db = get_db_connection()
    if get(element['date']) is None:
        db.insert(element)


def get_all():
    db = get_db_connection()
    return list(db.find())


def get(date):
    db = get_db_connection()
    return db.find_one({'date': date})


def get_db_connection():
    client = MongoClient(MONGO_URL)
    db = client.xkom_bot
    db.authenticate(name=MONGO_USERNAME, password=MONGO_PASSWORD)

    return db.xkom_bot_data
