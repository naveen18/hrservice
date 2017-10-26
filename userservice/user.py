#!flask/bin/python

from flask import Flask, jsonify, abort, request, json, make_response
from mongoConnection import getClient
import uuid
import datetime
import httperrors
from session import createSession
from bson.objectid import ObjectId
import hashlib

app = Flask(__name__)

@app.route('/userservice/api/v1.0/user', methods=['GET'])
def getUser():
	sessionid = request.headers.get("sessionid")
	userid = request.headers.get("userid")
	response = {}
	if not isValidSessionId(sessionid, userid):
		response["message"] = "Your session has expired, Please login again"
		response["code"] = httperrors.UNAUTHORIZED_ERROR
		return jsonify(success = False, error = response)
	doc = getUserDetails(userid)
	response["userid"] = str(doc["_id"])
	response["sessionid"] = sessionid
	response["firstname"] = doc["firstname"]
	response["lastname"] = doc["lastname"]
	return jsonify(success = True, data = response)

@app.route('/userservice/api/v1.0/user', methods=['PUT'])
def createUser():
	db = getClient()
	bodyparam = request.data
	bodyparam = json.loads(bodyparam)
	isValid = validateParams(bodyparam)
	response = {}
	if not isValid:
		response["message"] = "Invalid body param"
		response["code"] = httperrors.BAD_REQUEST_ERROR
		return jsonify(success = False, error = response["error"])
	hashedPassword  = hashlib.sha224(bodyparam["password"].encode('utf-8')).hexdigest()
	cursor = db['hrservice']
	doc  = cursor.users.find_one({"email":bodyparam["email"]})
	if doc is not None:
		response["message"] = "user with this email already exists"
		response["code"] = httperrors.BAD_REQUEST_ERROR
		return jsonify(success = False, error = response)
	result = cursor.users.insert_one({"firstname":bodyparam["firstname"], "lastname":bodyparam["lastname"], "email":bodyparam["email"], "password":bodyparam["password"]})
	if result is not None:
		return jsonify(success = True)
	return jsonify(success = False)

@app.route('/userservice/api/v1.0/user/login', methods=['PUT'])
def login():
	db = getClient()
	cursor = db['hrservice']
	bodyparam = request.data
	bodyparam = json.loads(bodyparam)
	hashedPassword  = hashlib.sha224(bodyparam["password"].encode('utf-8')).hexdigest()
	docs = cursor.users.find_one({"email":bodyparam["email"], "password":bodyparam["password"]})
	if docs is None:
		return jsonify(user_valid = False, message = "Invalid email or passord")
	else:
		sessionid = str(uuid.uuid4())
		expire_date = datetime.datetime.now()
		expire_date = expire_date + datetime.timedelta(days=10)
		response = make_response(jsonify(success = True, sessionid = sessionid))
		response.set_cookie("sessionid", sessionid, expires=expire_date)
		response.set_cookie("userid", str(docs["_id"]), expires=expire_date)
		return response

def deleteUser(userid):
	db = getClient()
	cursor = db['hrservice']
	result = cursor.users.delete_one({"userid":ObjectId(userid)})

def validateParams(body):
	for key, value in body.items():
		if len(value.strip()) < 3:
			return False
	return True

def isValidSessionId(sessionid, userid):
	db = getClient()
	cursor = db['hrservice']
	docs = cursor.session.find_one({"sessionid":sessionid, "userid":userid})
	if docs is None:
		return False;
	return True

def getUserDetails(userid):
	db = getClient()
	cursor = db['hrservice']
	docs = cursor.users.find_one({"_id":ObjectId(userid)})
	return docs

if __name__ == '__main__':
	# getSession("jjfdjdhfgjfd763276")
	# createSession("23", "kjdfhjshfwfhk")
    app.run(debug=False)