from pymongo import MongoClient
import os

def get_db_handle(db_name):
    uri = os.getenv('MONGO_DB_STRING')
    client = MongoClient(uri)
    return client[db_name]