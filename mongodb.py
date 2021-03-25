"""
user: admin
pass: aHLmUebY9AT8QsDn
"""
import pymongo
from pymongo import MongoClient
from datetime import datetime
import time



cluster = MongoClient("mongodb+srv://admin:aHLmUebY9AT8QsDn@cluster0.lnlrh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["guestbook"]
collection = db["messages"]


def write_message(from_whom,to_whom,message):
    post = {"from": from_whom, "to": to_whom, "datetime": datetime.utcnow(), "message": message}
    collection.insert_one(post)

