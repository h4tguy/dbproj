#Put your flask here
from flask import Flask, session, redirect,abort, render_template
import os
import json
import md5

app = Flask(__name__)

# This is here so that app is defined

from authentication import get_salt, requires_auth
from answer_q import *
from get_user_data import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_question')
def get_question():
	#session['curr_q']=get_q(session['username'])
	session['curr_q']=Question()
	session['curr_q'].body="This is a question"
	session['curr_q'].ans='ans'
	session['curr_q'].qno=42
	return json.dumps({'question':session['curr_q'].body})

@app.route('/answer_question')
def answer_question():
	their_ans=(json.loads(request.data)['answer']).strip()
	correct=their_ans.strip()==session['curr_q'].ans.strip()
	record_q(session['username'],session['curr_q'].qno,their_ans)

	return json.dumps({'correct':correct})

@app.route('/get_rate_question')
def get_rate_question():
	session['rate_q']=get_q(session['username'],True)
	return json.dumps({'question':session['rate_q'].body,'answer':session['rate_q'].ans})

@app.route('/rate_question')
@requires_auth(['users', 'admin'])
def rate_question():
	data=json.loads(response.data)
	record_rating(session['username'],session['rate_q'].qno,data['points'],data['reason'])
	return ""

@app.route('/performance')
def performance():
	name=json.loads(response.data)['name']
	ans=answer_info(name)
	return json.dumps({'total_answered':ans.total,'total_correct':ans.correct,'details':ans.detail})

@app.route('/questions')
def questions():
	name=json.loads(response.data)['name']
	return json.dumps({'question_info':question_info(name)})

@app.route('/classlist')
def classlist():
	return json.dumps({'classlist':get_classlist()})

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
