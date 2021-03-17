import pandas as pd
import redis
import json
import pymongo as mongo
import numpy as np
from datetime import date

r = redis.Redis(host='myredis',port='6379')

client = mongo.MongoClient("mongodb://mongodb:27017/")
# Mongoserver starten met "Sudo mongod" don't know why, maar de rest werkt niet.
mydb = client["BitcoinValue"]
mycol = mydb["Topvalue"]

pandatje = r.lrange("data",0,r.llen("data"))

dfs = []

for x in range(len(pandatje)):
    dfs.append(pd.read_json(pandatje[x]))

compdf = pd.concat(dfs,ignore_index=True)

uniquetimes = compdf['Time'].unique().tolist()

for x in uniquetimes:
    outputdict = {'Date' : str(date.today())}
    tempdf = compdf[compdf.Time.eq(x)]

    maxrow = tempdf[tempdf.BTCvalue == tempdf.BTCvalue.max()]
    
    #outputdict = {'Hash': maxrow["Hash"],'Time':maxrow["Time"],'BTC value': maxrow["BTCvalue"],'USD value':maxrow["USDvalue"]}
    #print(maxrow)
    for x in maxrow.columns:
        outputdict[x] = str(maxrow[x].values)

    mycol.insert_one(outputdict)

#mycol.insert_one({"test": "xd"})
#print(type(outputdict))
