from fastapi import FastAPI, APIRouter, Request, Form  
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles   ## please do `pip install aiofiles` first
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from pymongo import MongoClient
import requests
import json
import db_process

API_NLP_SERVICE_HOST = 'http://127.0.0.1:1234/predict'

app = FastAPI(title='Dashboard', version=1.0)
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")
templates = Jinja2Templates(directory="dashboard/templates")

## init database
nlp_col = db_process.init_db()


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})

## please do `pip install python-multipart` first, if you want to use `Form` parser.
@app.post("/")
async def predict(request: Request, email_text:str=Form('...'), user_id:str=Form('...')):
    results = requests.post(
        API_NLP_SERVICE_HOST, 
        json.dumps(dict({'user_id': user_id, 'text': email_text}))
        ).json()
    return templates.TemplateResponse(
        "index.html", {'request': request, 'user_id': user_id, 'email_text': email_text, 'score': results['score'], 'label': results['label']})

@app.get("/history")
def history(request: Request):
    items = db_process.extract_all(nlp_col)
    return templates.TemplateResponse(
        "history.html", {'request': request, 'items': items})

@app.post("/history")
def reset_db(request: Request):
    db_process.remove_all_data(nlp_col)
    return templates.TemplateResponse(
        "history.html", {'request': request})


if __name__ == "__main__":
    uvicorn.run("dash_app:app", host="127.0.0.1", port=2234, log_level="info")