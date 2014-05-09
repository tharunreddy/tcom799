"""
This script deploys restaurants to mongo database collection called restaurants.
We chose random locations for the restaurants and inserted into the db.
"""

from pymongo import MongoClient, GEO2D
import random
counter = 0

db = MongoClient().tcom799

def generate_restaurant():
    global counter
    counter += 1
    restaurant = {}
    restaurant['name'] = "Restaurant"+str(counter)
    lon = random.random()*360 - 180
    lat = random.random()*180 - 90
    restaurant['loc'] = [lon, lat]
    return restaurant

def insert_restaurants(n):
    for _ in range(n):
        db.restaurants.insert(generate_restaurant())

def main():
    db.locations.create_index([("loc", GEO2D)])
    insert_restaurants(100000)

if __name__ == "__main__":
    main()

