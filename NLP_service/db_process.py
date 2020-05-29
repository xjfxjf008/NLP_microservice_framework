from datetime import datetime
import uuid
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

def insert_result(user_id, text, score, label, nlp_col):
    uuid_nlp = str(uuid.uuid4())
    datetime_now = datetime.now().isoformat()
    nlp_col.insert_one({
        'uuid': uuid_nlp,
        'user_id': user_id,
        'text': text,
        'score': score,
        'label': label,
        'datetime': datetime_now
    })