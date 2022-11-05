import os
import json
import requests
import xmltodict
from tag import Tag
from bs4 import BeautifulSoup
from fastapi import FastAPI,HTTPException,status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="QuestionnaireAPI",
    version="0.2.0",
    license_info={
        "name":"Find me on linkedin",
        "url":"https://www.linkedin.com/in/hasindu-sithmin-9a1a12209/"
    },
    description="### question and answer API for programmers."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def redirect():
    return RedirectResponse('/docs')

@app.get("/tags")
def find_tags():
    with open('tag.json','r') as fp:
        return json.load(fp)

def gen_dct(obj):
    return {
        "author":obj['author']['name'],
        "date":obj['updated'],
        "question":obj['title']['#text'],
        "answer":BeautifulSoup(obj['summary']['#text'],'lxml').text
    }

@app.get('/{tag}')
async def find_tag(tag:Tag):
    domain = os.getenv('DOMAIN')
    if domain == None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    url = f"{domain}/{tag.value}"
    res = requests.get(url,headers={'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'})
    if res.status_code != 200:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Try again later")
    dct = xmltodict.parse(res.text)
    entries = dct['feed']['entry']
    return [gen_dct(entry) for entry in entries]

