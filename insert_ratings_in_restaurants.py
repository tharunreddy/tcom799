"""
This script updates the restaurants inserted in the restaurants collection with ratings generated at random into the
restaurants collection.
"""
import random
from pymongo import MongoClient

db = MongoClient().tcom799

def generate_rating():
    return random.random()*5

def insert_rating(collection, document):
    collection.update(document, {'$set': {'rating': generate_rating()}})

def main():
    for restaurant in db.restaurants.find():
        insert_rating(db.restaurants, restaurant)

if __name__ == "__main__":
    main()
          
    
    
    
    