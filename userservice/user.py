#!flask/bin/python
from flask import Flask, jsonify, abort, request, json
from mongoConnection import getClient
import hashlib

app = Flask(__name__)

@app.route('/userservice/api/v1.0/user/<string:userid>', methods=['GET'])
def getUser(userid):
	db = getClient()
	cursor = db['hrservice']
	docs = cursor.users.find({"sessionid":sessionid})
	for document in docs:
		return jsonify(session_valid = True)
	return jsonify(session_valid = False)

@app.route('/userservice/api/v1.0/user', methods=['PUT'])
def createUser():
	db = getClient()
	bodyparam = request.data
	bodyparam = json.loads(bodyparam)
	isValid = validateParams(bodyparam)
	if not isValid:
		return jsonify(message = "Invalid body param")
	print(bodyparam["password"])
	hashedPassword  = hashlib.sha224(bodyparam["password"].encode('utf-8')).hexdigest()
	cursor = db['hrservice']
	doc  = cursor.users.find({"email":bodyparam["email"]})
	if doc is not None:
		return jsonify(success = True, message = "user with this email already exists")
	result = cursor.users.insert_one({"firstname":bodyparam["firstname"], "lastname":bodyparam["lastname"], "email":bodyparam["email"], "password":bodyparam["password"]})
	if result is not None:
		return jsonify(success = True)
	return jsonify(success = False)

def login():
	db = getClient()
	bodyparam = request.data
	bodyparam = json.loads(bodyparam)
	hashedPassword  = hashlib.sha224(bodyparam["password"].encode('utf-8')).hexdigest()
	docs = db.users.find({"userid":bodyparam["userid"], "password":bodyparam["password"]})
	if docs is None:
		return jsonify(user_valid = False, message = "Invalid email or passord")
	else:
	 return jsonify(user_valid = True)

def deleteUser(userid):
	db = getClient()
	cursor = db['hrservice']
	result = cursor.users.delete_one({"userid":userid})

def validateParams(body):
	for key, value in body.items():
		if len(value.strip()) < 3:
			return False
	return True

if __name__ == '__main__':
	# getSession("jjfdjdhfgjfd763276")
	# createSession("23", "kjdfhjshfwfhk")
    app.run(debug=False)