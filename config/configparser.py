import json
import sys
import os

config = None

class Config:
	def __init__(self, config_file_path):
		with open(config_file_path) as config_file:
			config = json.load(config_file)
		self.project_directory = os.environ['HR_SERVICE_ROOT_DIR']
		self.mongo_path = os.environ['MONGO_PATH']
		self.hash_salt = os.environ['HASH_SALT']

def getConfig():
	global config
	if config is None:
		config = Config(os.environ['HR_SERVICE_ROOT_DIR'] + "/config/config.json")
	return config

if __name__ == "__main__":
	conf = getConfig()
	print(conf.project_directory);
	print(conf.mongo_path);
	print(conf.hash_salt)