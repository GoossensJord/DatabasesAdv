import pandas as pd
import redis
import json
import pymongo as mongo
import numpy as np
from datetime import date
import time
r = redis.Redis(host='myredis',port='6379')
print(r)
client = mongo.MongoClient("mongodb://mongodb:27017/")
# Mongoserver starten met "Sudo mongod" don't know why, maar de rest werkt niet.
mydb = client["BitcoinValue"]
mycol = mydb["Topvalue"]

def Filter():
    
    try:
        pandatje = r.lrange("BitcoinDatabase",0,r.llen("BitcoinDatabase"))

        dfs = []


        for x in range(len(pandatje)):
            dfs.append(pd.read_json(pandatje[x]))
            

        compdf = pd.concat(dfs,ignore_index=True)

        uniquetimes = compdf['Time'].unique().tolist()

        for x in uniquetimes:
            outputdict ={}
            outputdict = {'Date' : str(date.today())}

            tempdf = compdf[compdf.Time.eq(x)]

            maxrow = tempdf[tempdf.BTCvalue == tempdf.BTCvalue.max()]
            
            for y in maxrow.columns:
                outputdict[y] = str(maxrow[y].values)
                    
            print(x)


            mycol.insert_one(outputdict)
            r.delete("BitcoinDatabase")
    except:
        time.sleep(60)
        Filter()
while(True):
    Filter()
    print("done")
    
     
