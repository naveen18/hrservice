#!flask/bin/python
from flask import Flask, jsonify, abort
from mongoConnection import getClient

app = Flask(__name__)

@app.route('/userservice/api/v1.0/session/<string:sessionid>', methods=['GET'])
def getSession(sessionid):
	db = getClient()
	cursor = db['hrservice']
	docs = cursor.session.find({"sessionid":sessionid})
	for document in docs:
		return jsonify(session_valid = True)
	return jsonify(session_valid = False, message = "invalid session id")

def createSession(userid, sessionid):
	db = getClient()
	cursor = db['hrservice']
	result = cursor.session.insert_one({"sessionid":sessionid, "userid":userid})
	print(result)

if __name__ == '__main__':
	# getSession("jjfdjdhfgjfd763276")
	# createSession("23", "kjdfhjshfwfhk")
    app.run(debug=False)