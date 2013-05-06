#Put your flask here
from flask import Flask, session, redirect,abort
import os
import json
import md5
from mako.template import Template
from mako.lookup import TemplateLookup

app = Flask(__name__)
template_lookup = TemplateLookup(directories=['./dbproj/templates'])

# This is here so that app is defined

from authentication import get_salt, requires_auth

@app.route('/')
def index():
    return "hello world"

@app.route('/answer_question')
def answer_question():
	pass

@app.route('/rate_question')
@requires_auth
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

app.secret_key = ' \xfe#\x9eO\xd1,\xd3\xb14\xfe\xca\x12\xee\xb1\x89\xd9\xf4\xa1[\x0e\xcb\x0f\xe8'
if __name__ == "__main__":
    #conn = psycopg.connect("dbname=dbass user=dbass host=hamdulay.co.za")
    #cur = conn.cursor()
    app.run()
