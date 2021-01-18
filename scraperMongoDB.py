import requests
from bs4 import BeautifulSoup
import time
import threading
from pymongo import MongoClient


client = MongoClient("mongodb://127.0.01:27017")
BTCdb = client["BTCs"]
col_BTCdb = BTCdb["BTCs"]

def scraper():
    page = requests.get('https://www.blockchain.com/btc/unconfirmed-transactions')
    soup = BeautifulSoup(page.content, 'html.parser')
    HashedElements = soup.select("a.sc-1r996ns-0.fLwyDF.sc-1tbyx6t-1.kCGMTY.iklhnl-0.eEewhk.d53qjk-0.ctEFcK")
    RestElements = soup.select("span.sc-1ryi78w-0.cILyoi.sc-16b9dsl-1.ZwupP.u3ufsr-0.eQTRKC")

    content = []    
    for i in range(len(HashedElements)):
        line = []
        line.append(HashedElements[i].text)
        line.append(RestElements[i*3].text)
        line.append(float(RestElements[i*3+1].text.replace(" BTC", "")))
        line.append(RestElements[i*3+2].text)
        content.append(line)
    
    content.sort(key=lambda x:x[2])
    myDaDb = {"Hash": content[-1][0], "Time": content[-1][1], "BTC":  content[-1][2], "Dollars":  content[-1][3]}
    y = col_BTCdb.insert_one(myDaDb)
    print(y.inserted_id)

while True:
    scraper()
    time.sleep(60)
