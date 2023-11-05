from flask import Flask, redirect, render_template, request, session, url_for
import jwt

import sys
sys.path.append('..')

import util.parser as parser
import redis

from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

redis_db = redis.Redis(host='localhost', port=6379, db=0) 

@app.route("/")
def home():
	return "Hello world"

@app.route("/get-search-queries/<token>/<query>", methods = ["GET"])
def get_search(token, query):
	return parser.obtainContents(query)

@app.route("get-bot-message/<token>/<query>", methods = ["GET"])
def open_chatbot(token, query):
	return "penis"

@app.route("/login", methods=["POST"])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		
    user = f"user:{username}"
    
    exp_pass = redis_db.hget(user_key, "password")
    
    if exp_pass != password:
        return jsonify({"status" : "wrong-password"})

    token = jwt.encode({
        "username" : username,
        "exp" : datetime.datetime.utcnow() + datetime.timedelta(minutes=100)
    }, app.config["SECRET_KEY"])

		# Check credentials
    if verify_credentials(username, password):
        session['user'] = username
        token = jwt.encode({
            'username': user['username'], 
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=100)
        }, app.config['SECRET_KEY'])
        return 
    else:
        return "Invalid username/password"

def verify_credentials(username, password):
	"""Check credentials against Redis user table"""
	user_key = f'user:{username}'
	expected_pass = redis_db.hget(user_key, 'password')

	if expected_pass == password:
		return True
	else: 
		return False

if __name__ == "__main__":
	app.run(debug=True, port=4000)
