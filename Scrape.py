from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import pymongo as mongo
import time
import redis

r = redis.Redis(host='127.17.0.0',port='6379')
r.delete("BitcoinDatabase")

url = 'https://www.blockchain.com/btc/unconfirmed-transactions'


def Scrape():

    response = get(url)
    htmlsoup = BeautifulSoup(response.text,'html.parser')

    hashnames = htmlsoup.find_all('div',class_='sc-1au2w4e-0 bTgHwk')
    timestamps = htmlsoup.find_all('div',class_='sc-1au2w4e-0 emaUuf')
    BTCamount = htmlsoup.find_all('div',class_ ='sc-1au2w4e-0 fTyXWG')

    BTCvalue = []
    USDvalue = []
    hashes = []
    time = []

    for x in range(len(BTCamount)):
        var = BTCamount[x].text.replace(",","").split()
        
        if (x%2)==0:
            BTCvalue.append(var[1][5:])
        else:
            USDvalue.append(var[1][6:])

    for x in range(len(hashnames)):
        time.append(timestamps[x].text[4:])
        hashes.append(hashnames[x].text)
    
    BTCvalue =BTCvalue[1::]
    USDvalue = USDvalue[1::]
    time = time[1::]
    hashes = hashes[1::]
    #print(hashes)

    data = {'Hash':hashes,'Time':time,'BTCvalue':BTCvalue,'USDvalue':USDvalue}
    df = pd.DataFrame(data)

    jaysonfile = df.to_json()

    r.rpush("BitcoinDatabase",jaysonfile)

#-----------------------------------------------------

while(True):
    Scrape()
    print("done")
    time.sleep(60)
