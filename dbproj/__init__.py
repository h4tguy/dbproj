#Put your flask here
from flask import Flask, session, redirect, abort, render_template, g, request
import os
import json
import md5

app = Flask(__name__)

# This is here so that app is defined

from authentication import get_salt, requires_auth
from answer_q import *
from get_user_data import *
from difficulty import *
from db import connect_database
import static

@app.before_request
def initialise():
	g.db = connect_database()

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/answerQuestionPage')
def answerQuestionPage():
        return render_template('answerQuestionPage.html')

@app.route('/generateTest')
def generate_test():
	return render_template('generateTest.html')

@app.route('/get_question', methods=['POST', 'GET'])
def get_question():
	question = session['curr_q'] = get_q(session['username'])
	if question is None:
		return json.dumps({'qid': '', 'question': 'Congratulations, you have completed the quiz', 'type': 'MCQ', 'mcq':{}})
	return json.dumps({'qid': question.qno, 'question':question.body, 'type': question.qtype, 'mcq':question.mcq})

@app.route('/answerQuestion', methods=['POST', 'GET'])
def answer_question():
	question = session['curr_q']
	correctAnswer = question.ans
	userAnswer = json.loads(request.data)['answer']

	cur = g.db.cursor()
	cur.execute('select count(*) from answers where regnum = %s and qno = %s', (session['username'], question.qno))
	answeredBefore = cur.fetchone()[0] > 0
	if not answeredBefore:
		cur.execute('insert into answers values (%s, %s, %s)', (session['username'], question.qno, userAnswer))
	else:
		cur.execute('update answers set answer = %s where regnum = %s and qno = %s', (userAnswer, session['username'], question.qno))
	cur.close()
	g.db.commit()

	return json.dumps({'correct': correctAnswer == userAnswer})

@app.route('/get_rate_question', methods=['POST'])
def get_rate_question():
	session['rate_q']=get_q(session['username'],True)
	if session['rate_q']:
		return json.dumps({'question':session['rate_q'].body,'answer':session['rate_q'].ans,'qid':session['rate_q'].qno})
	return "{}"

@app.route('/rate_question', methods=['POST'])
#@requires_auth(['users', 'admin'])
def rate_question():
	print request.data
	data=json.loads(request.data)
	record_rating(session['username'],session['rate_q'].qno,data['rating'],data['reason'])
	return "{}"

@app.route('/performance', methods=['GET', 'POST'])
def performance():
	name=json.loads(request.data)['studentno']
	ans=answer_info(name)
	return json.dumps({'name':ans.name,'total_answered':ans.answered,'total_correct':ans.correct,'details':ans.detail})

@app.route('/questions', methods=['GET', 'POST'])
def questions():
	studentno=json.loads(request.data)['studentno']
	return json.dumps({'questions':question_info(studentno)})

@app.route('/classlist', methods=['GET', 'POST'])
def classlist():
	return json.dumps({'classlist':get_classlist()})

@app.route('/score_questions')
def show_score_questions():
	return json.dumps({'diff_data':score_questions()})

@app.route('/check_weak_questions')
def show_check_weak_question():
	return json.dumps({'questions':check_weak_question()})

@app.route('/update_weak_questions')
def do_update_weak_questions():
	data=json.loads(request.data)
	update_weak_question(data['trues'],data['falses'])
	return "{}"

@app.route('/make_test')
def make_test():
	ans=gen_test()
	return json.dumps({'data':ans})

app.secret_key = ' \xfe#\x9eO\xd1,\xd3\xb14\xfe\xca\x12\xee\xb1\x89\xd9\xf4\xa1[\x0e\xcb\x0f\xe8'
if __name__ == "__main__":
	#conn = psycopg.connect("dbname=dbass user=dbass host=hamdulay.co.za")
	#cur = conn.cursor()
	app.run()
