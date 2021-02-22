from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import pymongo as mongo
import time


url = 'https://www.blockchain.com/btc/unconfirmed-transactions'
client = mongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb = client["BitcoinValue"]
mycol = mydb["Topvalue"]

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

    maxvalue = max(BTCvalue)
    maxindex = BTCvalue.index(maxvalue)

    data = {'Hash':hashes,'Time':time,'BTC value':BTCvalue,'USD value':USDvalue}
    df = pd.DataFrame(data)
    
    output = df.loc[[maxindex]]
    
    columns = df.columns

    rowdict = {}
    for x in columns:
        rowdict[x] = str(output[x].values)[2:-2]
        #print(output[x].values)
    mycol.insert_one(rowdict) 
    #print(rowdict)

while(True):
    Scrape()
    print("Done!")
    time.sleep(60)