"""
We executed geo-spatial queries on mongodb and redis and we measured the execution time using
python's timeit module.

Here are some of our results (for 10000 queries):
1. Query restaurants using only mongodb query (0.375 s)
2. Query users using only mongodb query (0.466 s)
3. Query restaurants using mongodb, and cache the result in redis (1.455 s)
4. Query users using mongodb. and cache the result in redis (1.498 s)

It is quite strange that caching the result in redis produced abnormally high execution time.
In reality this shouldn't be the case. We suspect the either the test redis-server running on the localhost
or the redis module for python to be causing delay.
"""
from pymongo import MongoClient
import redis

import timeit

db = MongoClient().tcom799
r = redis.StrictRedis(host='localhost', port=6379, db=0)

def query_without_redis(collection, query={"loc": {"$within": {"$center": [[0, 0], 1]}}}):    
    return collection.find(query)

def query_with_redis(collection, query={"loc": {"$within": {"$center": [[0, 0], 1]}}}):
    res = r.get((collection, query))
    if res:                
        return res
    else:     
        res = query_without_redis(collection, query)
        r.set((collection, query), res)
        return res 

def query_restaurants_without():
    return query_without_redis(db.restaurants)

def query_users_without():
    return query_without_redis(db.users)

def query_users():
    return query_with_redis(db.users)

def query_restaurants():
    return query_with_redis(db.restaurants)

def main():
    r.flushdb()
    print timeit.timeit("query_restaurants_without()", setup="from __main__ import query_restaurants_without", number=10000)
    print timeit.timeit("query_users_without()", setup="from __main__ import query_users_without", number=10000)
    print timeit.timeit("query_users()", setup="from __main__ import query_users", number=10000)
    print timeit.timeit("query_restaurants()", setup="from __main__ import query_restaurants", number=10000)
    
if __name__ == "__main__":
    main()