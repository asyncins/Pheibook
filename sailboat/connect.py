"""
https://api.mongodb.com/python/current/tutorial.html#making-a-connection-with-mongoclient
"""

from pymongo import MongoClient


client = MongoClient("mongodb://111.231.93.117:27017/")
databases = client.sailb

