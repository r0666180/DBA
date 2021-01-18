import requests
from bs4 import BeautifulSoup
import time
import threading


def scraper():
    page = requests.get('https://www.blockchain.com/btc/unconfirmed-transactions')
    soup = BeautifulSoup(page.content, 'html.parser')

    HashedElement = soup.select("a.sc-1r996ns-0.fLwyDF.sc-1tbyx6t-1.kCGMTY.iklhnl-0.eEewhk.d53qjk-0.ctEFcK")
    RestElement = soup.select("span.sc-1ryi78w-0.cILyoi.sc-16b9dsl-1.ZwupP.u3ufsr-0.eQTRKC")
    
    content = []

    for i in range(len(HashedElement)):

        Regel = []
        Regel.append(HashedElement[i].text)
        Regel.append(RestElement[i*3].text)
        Regel.append(float(RestElement[i*3+1].text.replace(" BTC", "")))
        Regel.append(RestElement[i*3+2].text)
        content.append(Regel)

    content.sort(key=lambda x:x[2])
    with open("ScraperLogfile.txt", "a") as f:
        print(content[-1], file=f)
    print("Weggeschreven")

    time.sleep(60)
    
        
while True:
    scraper()
    