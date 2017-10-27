import json
import sys
import os
config  = None

def getConfig(name):
	global config
	if config is None:
		with open("/Users/naveen/Documents/hrservice/config/config.json") as config_file:
			config = json.load(config_file)
	return config[name]

if __name__ == "__main__":
	print(getConfig("file_path"))
