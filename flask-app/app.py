from flask import Flask, redirect, render_template, request, session, url_for
import os
import util.parser as parser

app = Flask(__name__)

redis_db = redis.Redis(host='localhost', port=6379, db=0) 

@app.route("/get_search_queries/<query>", methods = ["GET"])
def get_search(query):
	return parser.obtainContents(query)

@app.route("/<query>", methods = ["GET"])
def open_chatbot(query):
	return #render_template("index.html", query=query)

@app.route("/login", methods=["POST","GET"])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		
		# Check credentials
		if verify_credentials(username, password):
			session['user'] = username
			return redirect(url_for('home'))
		else:
			return "Invalid username/password"
	return render_template('login.html')

def verify_credentials(username, password):
    """Check credentials against Redis user table"""
    users = redis_db.lrange('user_table', 0, -1) 
    for i in range(0, len(users), 2):
        if users[i].decode('utf-8') == username and users[i+1].decode('utf-8') == password:
            return True
    
    return False

if __name__ == "__main__":
	app.run(debug=True, port=4000)