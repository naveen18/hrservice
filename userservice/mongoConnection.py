import sys
from pymongo import MongoClient
# sys.path.append("/Users/naveen/Documents/hrservice")
from config.configparser import getConfig

client = None;

def getClient():
	global client
	if client is None:
		conf  = getConfig()
		client = MongoClient(conf.mongo_path)
	return client;

if __name__ == "__main__":
	client = getClient()