import pandas as pd
import redis
import json
import pymongo as mongo
import numpy as np
from datetime import date
import time

r = redis.Redis(host='dockercompose_redis_1',port='6379')
print(r)
client = mongo.MongoClient("mongodb://dockercompose_db_1/")

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
                    
            #print(x)


            mycol.insert_one(outputdict)
            print(outputdict)
            r.delete("BitcoinDatabase")
    except:
        print("waited")
        time.sleep(60)
<<<<<<< HEAD
        
=======
        print("waited filtering")
>>>>>>> 7cb4bfde6ea146f8a4f9ec375c1a7f9253ffd127
        Filter()
while(True):
    print("filtering")
    Filter()
    print("done")
    
     
