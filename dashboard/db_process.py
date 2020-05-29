from pymongo import MongoClient
import os

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_NAME = os.environ.get("DB_NAME")
DB_COL_NAME = os.environ.get("DB_COL_NAME")


def init_db(db_host=DB_HOST, db_port=DB_PORT, db_name=DB_NAME, col_name=DB_COL_NAME):
    db = MongoClient(host=db_host, port=db_port, connectTimeoutMS=30000) 
    nlp_db = db[db_name]
    nlp_col = nlp_db[col_name]
    return nlp_col

def extract_all(nlp_col):
    cursor = nlp_col.find({})
    return [item for item in cursor]

def remove_all_data(nlp_col):
    nlp_col.remove()