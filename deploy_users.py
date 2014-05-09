"""
This script deploys restaurants to mongo database collection called users.
"""

from pymongo import MongoClient, GEO2D
import random
counter = 0

db = MongoClient().tcom799

def generate_user():
    global counter
    counter += 1
    user = {}
    user['name'] = "User"+str(counter)
    lon = random.random()*360 - 180
    lat = random.random()*180 - 90
    user['loc'] = [lon, lat]
    return user

def insert_users(n):
    for _ in range(n):
        db.users.insert(generate_user())

def main():
    db.locations.create_index([("loc", GEO2D)])
    insert_users(3000000)

if __name__ == "__main__":
    main()

