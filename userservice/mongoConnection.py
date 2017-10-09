from pymongo import MongoClient

client = None;

def getClient():
	global client
	if client is None:
		client = MongoClient("mongodb://127.0.0.1:27017")
	return client;