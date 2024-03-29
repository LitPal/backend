from flask import Flask, request, jsonify
import jwt
from flask_cors import CORS

import sys
import os
sys.path.append('..')

import util.parser as parser

from llm import LLM, getPDF

import redis
import datetime

from dotenv import load_dotenv

import redisUtil

load_dotenv()

url = ""

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
	return "Hello world"

@app.route("/get-search-queries/<token>/<query>", methods = ["GET"])
def get_search(token, query):
    if not redisUtil.decode(token, os.getenv("SECRET_KEY")):
       return jsonify({"status" : "unauthorized"})

    contents = parser.obtainContents(query)
    return jsonify(contents)

@app.route("/post-url", methods = ["POST"])
def post_url():
    token = request.json['token']
    if not redisUtil.decode(token, os.getenv("SECRET_KEY")):
       return jsonify({"status" : "unauthorized"})
 
    global url 
    url = request.json['url'] 

    global llm 
    llm = LLM(url)

    return jsonify({"status" : "success"})

@app.route("/get-bot-message/<token>/<query>", methods = ["GET"])
def open_chatbot(token, query):
    if not redisUtil.decode(token, os.getenv("SECRET_KEY")):
       return jsonify({"status" : "unauthorized"})

    global llm
    answer = llm.query(query)
    return jsonify({"answer" : answer["result"]})

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
