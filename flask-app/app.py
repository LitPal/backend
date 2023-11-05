from flask import Flask, redirect, render_template, request, session, url_for
import sys
sys.path.append('..')
import util.parser as parser
import redis

app = Flask(__name__)

redis_db = redis.Redis(host='localhost', port=6379, db=0) 

@app.route("/")
def home():
	return "Hello world"

@app.route("/get_search_queries/<query>", methods = ["GET"])
def get_search(query):
	return parser.obtainContents(query)

@app.route("/<query>", methods = ["GET"])
def open_chatbot(query):
	return "penis"

@app.route("/login/<username>/<password>", methods=["POST","GET"])
def login(username, password):
	if request.method == 'GET':
		#username = request.form['username']
		#password = request.form['password']
		
		# Check credentials
		if verify_credentials(username, password):
			session['user'] = username
			return redirect(url_for('home'))
		else:
			return "Invalid username/password"
	return render_template('login.html')

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