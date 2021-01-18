import requests
from bs4 import BeautifulSoup
import time
import threading
import redis
import json

r = redis.Redis()


def scraper():
    page = requests.get('https://www.blockchain.com/btc/unconfirmed-transactions')

    soup = BeautifulSoup(page.content, 'html.parser')

    HashedElement = soup.select("a.sc-1r996ns-0.fLwyDF.sc-1tbyx6t-1.kCGMTY.iklhnl-0.eEewhk.d53qjk-0.ctEFcK")

    RestEl = soup.select("span.sc-1ryi78w-0.cILyoi.sc-16b9dsl-1.ZwupP.u3ufsr-0.eQTRKC")

    content = []
    for i in range(len(HashedElement)):
        line = []
        line.append(HashedElement[i].text)
        line.append(RestEl[i*3].text)
        line.append(float(RestEl[i*3+1].text.replace(" BTC", "")))
        line.append(RestEl[i*3+2].text)
        content.append(line)
    
    content.sort(key=lambda x:x[2])

    jsonRedis = {"TopValHash": content[-1][0], "Time": content[-1][1], "BTCval": str(content[-1][2]), "DolVal": content[-1][3]} 
    json_dump = json.dumps(jsonRedis)
    r.set("topHash",json_dump, ex=60)
    
    r.get("topHash")
    print("json storeed")
    time.sleep(60)

while True:
    scraper()
    