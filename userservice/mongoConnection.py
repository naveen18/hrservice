import sys
from pymongo import MongoClient
import urllib 
# sys.path.append("/Users/naveen/Documents/hrservice")
from config.configparser import getConfig

client = None;

def getClient():
	global client
	if client is None:
		conf  = getConfig()
		print(conf.mongo_password)
		url = "mongodb://" + conf.mongo_username + ":" + urllib.parse.quote(conf.mongo_password) + "@" + \
		conf.mongo_shard[0] + "," + conf.mongo_shard[1] + "," + conf.mongo_shard[2] + "/admin?ssl=true&replicaSet=" + conf.mongo_replica + "&authSource=admin"
		client = MongoClient(url)
		# client = MongoClient(conf.mongo_path)
	return client;

if __name__ == "__main__":
	client = getClient()
	# cursor = client["hrservice"];
	# doc  = cursor.testdb.find()
	# print(doc)
