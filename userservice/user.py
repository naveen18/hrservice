#!flask/bin/python

import sys
# sys.path.append("/Users/naveen/Documents/hrservice")
from flask import Flask, jsonify, abort, json, make_response, request, render_template
from mongoConnection import getClient
import uuid
import datetime
import httperrors
from bson.objectid import ObjectId
import hashlib
from mlmodel.model import predict
from mlmodel.analytics import generateVisualisations

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
		createSession(docs["_id"], sessionid)
		response = make_response(jsonify(success = True, sessionid = sessionid))
		response.set_cookie("sessionid", sessionid, expires=expire_date)
		response.set_cookie("userid", str(docs["_id"]), expires=expire_date)
		return response

@app.route('/userservice/api/v1.0/session/<string:sessionid>', methods=['GET'])
def getSession(sessionid):
	db = getClient()
	cursor = db['hrservice']
	docs = cursor.session.find({"sessionid":sessionid})
	for document in docs:
		return jsonify(session_valid = True)
	return jsonify(session_valid = False, message = "invalid session id")


@app.route('/userservice/api/v1.0/visualizations/<string:sessionid>', methods=['GET'])
def getAnalytics(sessionid):
	res = getSession(sessionid);
	res = json.loads(res.get_data())
	if res['session_valid'] is False:
		# redirect to login page
		pass
	else:
		generateVisualisations()
	return jsonify(success = True)


@app.route('/userservice/api/v1.0/predict/<string:sessionid>', methods=['GET'])
def getPredictionLabel(sessionid):
	res = getSession(sessionid);
	res = json.loads(res.get_data())
	if res['session_valid'] is False:
		# redirect to login page
		pass
	else:
		satisfaction_level = request.args.get('satisfaction_level')
		last_evaluation = request.args.get('last_evaluation')
		number_project = request.args.get('number_project')
		average_montly_hours = request.args.get('average_montly_hours')
		time_spend_company = request.args.get('time_spend_company')
		Work_accident = request.args.get('Work_accident')
		promotion_last_5years = request.args.get('promotion_last_5years')
		dept = request.args.get('sales')
		sal = request.args.get('salary')
		department = [0]*10
		salary = [0]*3
		department_values = ["product_mng", "marketing", "technical", "sales", "hr", "IT", "RandD", "accounting", "management", "support"]
		salary_values = ["low", "medium", "high"]
		dept_index = department_values.index(dept)
		salary_index = salary_values.index(sal)
		department[dept_index] = 1
		salary[salary_index] = 1
		sample = [satisfaction_level, last_evaluation, number_project, average_montly_hours, time_spend_company,\
		Work_accident, promotion_last_5years]
		sample.extend(department)
		sample.extend(salary)
		res = predict(sample)
		res = res.item() 
	return jsonify(success = True, left = res)


def createSession(userid, sessionid):
	db = getClient()
	cursor = db['hrservice']
	result = cursor.session.insert_one({"sessionid":sessionid, "userid":userid})

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

@app.route('/')
def main():
	 return render_template('index.html')

if __name__ == '__main__':
	# getSession("jjfdjdhfgjfd763276")
	# createSession("23", "kjdfhjshfwfhk")
	app.run(debug=False)