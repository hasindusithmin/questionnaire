import os
from fastapi import FastAPI,HTTPException,status
from tag import Tag
import requests
import xmltodict
from bs4 import BeautifulSoup
app = FastAPI(title="QuestionnaireAPI")


@app.get('/')
def root():
    return 


def fn(obj):
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
    return [fn(entry) for entry in entries]

