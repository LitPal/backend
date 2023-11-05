from flask import Flask, request, jsonify
import jwt
from flask_cors import CORS

import sys
import os
sys.path.append('..')

import util.parser as parser
import redis
import datetime

from dotenv import load_dotenv

import redisUtil

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
	return "Hello world"

@app.route("/get-search-queries/<token>/<query>", methods = ["GET"])
def get_search(token, query):

    dec_user = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])

    # if redisUtil.authenticate() redis_db.hget(f"user:{dec_user['username']}", "password") == None:
    #    return jsonify({"status" : "unauthorized"})


    contents = parser.obtainContents(query)
    return jsonify(contents)

@app.route("/get-bot-message/<token>/<query>", methods = ["GET"])
def open_chatbot(token, query):
	return "penis"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    if not redisUtil.authenticate(username, password):
        return jsonify({"status" : "wrong-password"})

    token = jwt.encode({
        "username" : username,
        "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=100)
    }, os.getenv("SECRET_KEY"))

    return jsonify({"status" : "authorized", "token" : token + ""})


if __name__ == "__main__":
	app.run(debug=True, port=4000)
