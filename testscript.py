import redis

r = redis.Redis(host ='myredis',port='6379')

r.set("sleutel", "waarde ")
