#Put your flask here
from flask import Flask, session, redirect,abort
import psycopg2,os
import json
import md5


@app.route('/')
def index():
	pass

@app.route('/login')
def login():
	try:
		if 'username' in session:
			return redirect(url_for('index'))
		elif request.method=='POST':
			if 'temp_salt' not in session:
				#if this branch occurs, we may have an attacker
				return make_login_screen()
			#do authentication
			cur.execute('select hash,use_type from users where username='+request.form['username'])
			res = cur.fetchone()
			if not res:
				abort(500) #there should always be a match, because the client can't change uname since prev access
			hsh,use_type=res
			hasher=md5.new()
			hasher.update(hsh+temp_salt)
			if(hasher.digest() != request.form['hash']):
				return make_login_screen(True)
			else:
				session['username']=request.form['username']
				session['use_type']=use_type #get use_type from db
				return redirect(url_for('index'))	
		else:
			return make_login_screen()
	finally:
		session.pop('temp_salt',None)

def make_login_screen(bad=False)
#pulling out making the login screen to a separate method
	if(bad):
		return render_template('login',bad=True)
	else:
		return render_template('login')

@app.route('/get_salt', methods=['POST'])
def get_salt():
	tmp = json.loads(request.form['json'])
	cur.execute("select salt from users where username="+tmp['username'])
	res = cur.fetchone()
	if res=None:
		make_login_screen(True)
		return json.dumps({})	
	temp_salt = os.urandom(24)
	session['temp_salt']=temp_salt
	return json.dumps({'salt':res[0],'temp_salt':temp_salt})


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

conn = psycopg.connect("dbname=dbass user=dbass host=hamdulay.co.za")
cur = conn.cursor()
app.secret_key = ' \xfe#\x9eO\xd1,\xd3\xb14\xfe\xca\x12\xee\xb1\x89\xd9\xf4\xa1[\x0e\xcb\x0f\xe8'
app.run()
