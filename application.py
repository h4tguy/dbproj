#Put your flask here
from flask import Flask, session, redirect

app=Flask(__name__)

@app.route('/')
def index():
	pass

@app.route('/login')
def login():
	pass

@app.route('/answer_question')
def answer_question():
	pass

@app.route('/rate_question')
def rate_question():
	pass

@app.route('/performance/<name>')
def performance(name=None):
	pass

@app.route('/questions/<name>')
def questions(name=None):
	pass

@app.route('/classlist')
def classlist():
	pass

@app.route('/score_questions')
def score_questions():
	pass

@app.route('/check_weak_question')
def check_weak_question():
	pass

@app.route('/make_test')
def make_test():
	pass

app.secret_key=' \xfe#\x9eO\xd1,\xd3\xb14\xfe\xca\x12\xee\xb1\x89\xd9\xf4\xa1[\x0e\xcb\x0f\xe8'
