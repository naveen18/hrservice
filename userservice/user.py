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
from config.configparser import getConfig

app = Flask(__name__)

@app.route('/userservice/api/v1.0/user', methods=['GET'])
def getUser():
	sessionid = request.headers.get("sessionid")
	userid = request.headers.get("userid")
	response = {}
	if not isValidSessionId(sessionid, userid):
		response["message"] = "Your session has expired, Please login again"
		response["code"] = httperrors.UNAUTHORIZED_ERROR
		resp = make_response(jsonify(success = False, error = response))
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp
	doc = getUserDetails(userid)
	response["userid"] = str(doc["_id"])
	response["sessionid"] = sessionid
	response["firstname"] = doc["firstname"]
	response["lastname"] = doc["lastname"]
	response["email"] = doc["email"]
	resp = make_response(jsonify(success = True, data = response))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp

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
		response = make_response(jsonify(success = False, message = "Invalid email or passord"))
		response.headers['Access-Control-Allow-Origin'] = '*'
		response.status = httperrors.UNAUTHORIZED_ERROR
		return response
	else:
		sessionid = str(uuid.uuid4())
		expire_date = datetime.datetime.now()
		expire_date = expire_date + datetime.timedelta(days=10)
		createSession(docs["_id"], sessionid)
		response = make_response(jsonify(success = True, sessionid = sessionid))
		response.set_cookie("sessionid", sessionid, expires=expire_date)
		response.set_cookie("userid", str(docs["_id"]), expires=expire_date)
		response.headers['Access-Control-Allow-Origin'] = '*'
		return response

@app.route('/userservice/api/v1.0/user/logout', methods=['PUT'])
def logout():
	sessionid = request.headers.get("sessionid")
	userid = request.headers.get("userid")
	db = getClient()
	cursor = db['hrservice']
	doc  = cursor.session.delete_one({"sessionid":sessionid})
	expire_date = datetime.datetime.now()
	response = make_response(jsonify(success = "true"))
	response.set_cookie("sessionid", "", expires=expire_date)
	response.set_cookie("userid", "", expires=expire_date)
	return response

@app.route('/userservice/api/v1.0/session/<string:sessionid>', methods=['GET'])
def getSession(sessionid):
	db = getClient()
	cursor = db['hrservice']
	docs = cursor.session.find_one({"sessionid":sessionid})
	if docs is not None:
		response = make_response(jsonify(session_valid = True))
	else:
		response = make_response(jsonify(session_valid = False, message = "invalid session id"))
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.status = "200"
	return response

@app.route('/userservice/api/v1.0/visualizations/<string:sessionid>', methods=['GET'])
def getAnalytics(sessionid):
	res = getSession(sessionid);
	res = json.loads(res.get_data())
	if res['session_valid'] is False:
		# redirect to login page
		return jsonify(success = False)
	else:
		generateVisualisations()
		conf = getConfig()
		img1 = "static/images/distributions1.png"
		img2 = "static/images/distributions2.png"
		img3 = "static/images/distributions3.png"
		img4 = "static/images/distributions4.png"
		img5 = "static/images/distributions5.png"
		img6 = "static/images/clusters.png"
		img7 = "static/images/correlation.png"
		images = [img1, img2, img3, img4, img5, img6, img7]
	return jsonify(success = True, images = images)

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
	if userid is None or sessionid is None:
		return False
	db = getClient()
	cursor = db['hrservice']
	docs = cursor.session.find_one({"sessionid":sessionid, "userid":ObjectId(userid)})
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

@app.route('/home')
def renderHomePage():
	return render_template('home.html')

@app.route('/about')
def renderAboutPage():
	return render_template('about.html')

@app.route('/getlabel')
def renderPredictionPage():
	return render_template('predict.html')

@app.route('/signup')
def renderSignupPage():
	return render_template('signup.html')

if __name__ == '__main__':
	# getSession("jjfdjdhfgjfd763276")
	# createSession("23", "kjdfhjshfwfhk")
	conf = getConfig()
	app.run(host = conf.host, port = conf.port, threaded=True, debug=False)