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


load_dotenv()

app = Flask(__name__)
CORS(app)

redis_db = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True) 
redis_db.hset('user:alice', 'password', 'pw123')
redis_db.hset('user:bob', 'password', 'pw456')

@app.route("/")
def home():
	return "Hello world"

@app.route("/get-search-queries/<token>/<query>", methods = ["GET"])
def get_search(token, query):
	return jsonify(parser.obtainContents(query))

@app.route("/get-bot-message/<token>/<query>", methods = ["GET"])
def open_chatbot(token, query):
	return "penis"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data['username']
    password = data['password']


    user_key = f"user:{username}"
    exp_pass = redis_db.hget(user_key, "password")

    if exp_pass != password:
        return jsonify({"status" : "wrong-password"})

    token = jwt.encode({
        "username" : username,
        "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=100)
    }, os.getenv("SECRET_KEY"))

    return jsonify({"status" : "authorized", "token" : token + ""})


if __name__ == "__main__":
	app.run(debug=True, port=4000)
