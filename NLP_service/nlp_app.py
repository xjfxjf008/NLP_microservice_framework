from nlp_core import nlp_predict
import db_process

import numpy as np
import os
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
import uvicorn

app = FastAPI(title='NLP microservice', version=0.2)

## init database
nlp_col = db_process.init_db()

class InputText(BaseModel):
    user_id: str = None
    text: str
     

@app.get("/")
def index():
    return "Natural language processing (NLP) microservice is online."


@app.post("/predict")
async def predict(input_text: InputText):
    score, label = nlp_predict(input_text.text)
    db_process.insert_result(
        user_id=input_text.user_id, 
        text=input_text.text, 
        score=score, 
        label=label, 
        nlp_col=nlp_col)

    return {'score': score, 'label': label}
    

if __name__ == "__main__":
    uvicorn.run("nlp_app:app", host="127.0.0.1", port=1234, log_level="info")