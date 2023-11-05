from flask import Flask, redirect, render_template, request, session, url_for
import os
import util.parser as parser

app = Flask(__name__)

@app.route("/get_search_queries/<query>", methods = ["GET"])
def get_search(query):
	return parser.obtainContents(query)

@app.route("/<query>", methods = ["GET"])
def open_chatbot(query):
	return render_template("index.html", query=query)


if __name__ == "__main__":
	app.run(debug=True, port=4000)