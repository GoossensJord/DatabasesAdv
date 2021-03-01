import pandas as pd
import redis
import json

r = redis.Redis()

pandatje = r.lrange("data",0,r.llen("data"))

testing = []
for x in range(len(pandatje)):
    testing.append(pd.read_json(pandatje[x]))

compdf = pd.concat(testing,ignore_index=True)
print(compdf)