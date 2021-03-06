import psycopg2
import random
import string
from functools import wraps
from flask import  request, Response, session, redirect, url_for, g
import json
import hashlib
from dbproj import app


@app.route('/get_salt', methods=['POST'])
def get_salt():
	regnum = json.loads(request.data)['studentno']

	cur = g.db.cursor()
	cur.execute("select regnum, salt from Users where regnum=%s", (regnum,))
	res = cur.fetchone()
	regnum = res[0]
	salt = res[1]
	cur.close()

	#no corresponding user in db
	if res is None:
		return '{}'

	temp_salt = ''.join(random.choice(string.ascii_letters) for i in xrange(24))
	session['temp_salt'] = temp_salt
	return '{"salt": "%s","temp_salt": "%s", "studentno": "%s"}' % (salt, temp_salt, regnum)

@app.route('/register', methods=['POST'])
def register():
	requestData = json.loads(request.data)
	salt = ''.join(random.choice(string.ascii_letters) for i in xrange(20))

	username, passwordHash = requestData['username'], requestData['passwordHash']
	print passwordHash
	hasher = hashlib.md5()
	hasher.update(passwordHash+salt)
	dbHash = hasher.hexdigest()
	print dbHash

	cur = g.db.cursor()
	try:
		cur.execute("insert into Users values (%s, %s, %s, %s, '1')", (username, username, salt, dbHash))
	except psycopg2.IntegrityError:
		g.db.rollback()
	finally:
		cur.close()
		g.db.commit()

	return '{"status": 1}'

@app.route('/login', methods=['GET', 'POST'])
def login():
	cur = g.db.cursor()
	try:
		loggedIn = False
		requestData = json.loads(request.data)
		print requestData
		regnum = requestData['studentno']
		clientHash = requestData['hash']

		# User is logged in aleady.
		if request.method == 'POST':
			# wtf?
			if 'temp_salt' not in session:
				abort(500)

			cur.execute('select hashedpassword, usertype from Users where regnum=%s', (regnum, ))
			res = cur.fetchone()

			if not res:
				abort(500) # there should always be one match since the clinet can't change the username since previous access

			hsh = res[0]
			user_role = res[1]

			hasher = hashlib.md5()
			temphasher = hashlib.md5()
			temphasher.update(session['temp_salt'])
			hasher.update(hsh + temphasher.hexdigest())


			print hasher.hexdigest()
			print clientHash
			if(hasher.hexdigest() != clientHash):
				loggedIn = False
			else:
				loggedIn = True
				session['username'] = regnum
				session['user_role'] = user_role

		if loggedIn:
			return '{"status": 1}'
		else:
			return '{"status": 0}'
	finally:
		cur.close()
		session.pop('temp_salt', None)

def requires_auth(roles):
	def decorator(f):
		@wraps(f)
		def decorated(*args, **kwargs):
			# If no username is set, the user is not logged in.
			if not 'username' in session:
				abort(500)
			else:
				if session['user_role'] not in roles:
					return redirect(url_for('login'))

			return f(*args, **kwargs)
		return decorated
	return decorator
