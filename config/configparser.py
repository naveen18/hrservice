import json
import sys
import os

config = None

class Config:
	def __init__(self, config_file_path):
		with open(config_file_path) as config_file:
			config = json.load(config_file)
		self.project_directory = os.environ['HR_SERVICE_ROOT_DIR']
		# self.mongo_path = os.environ['MONGO_PATH']
		self.mongo_password = os.environ['MONGO_PASS']
		self.mongo_username = os.environ['MONGO_USERNAME']
		self.hash_salt = os.environ['HASH_SALT']
		self.mongo_shard = ["", "", ""]
		self.mongo_shard[0] = config["mongo-shard-0"]
		self.mongo_shard[1] = config["mongo-shard-1"]
		self.mongo_shard[2] = config["mongo-shard-2"]
		self.mongo_replica = config["mongo-replica"]
		self.port = config["port"]
		self.host = config["host"]

def getConfig():
	global config
	if config is None:
		config = Config(os.environ['HR_SERVICE_ROOT_DIR'] + "/config/config.json")
	return config

if __name__ == "__main__":
	conf = getConfig()
	print(conf.project_directory);
	# print(conf.mongo_path);
	print(conf.hash_salt)