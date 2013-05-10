# Copied from http://flask.pocoo.org/snippets/8/ and then modified
import random
import string
from functools import wraps
from flask import  request, Response, session, redirect, url_for, g
import json
import hashlib
from dbproj import app

# not sure if this is necessary anymore, just commenting out for now, sorry - Jarred
#def make_login_screen(bad=False):
#pulling out making the login screen to a separate method
#TODO: templatise this.
	#return template_lookup.get_template('./temp_login.html').render(bad=bad)

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

@app.route('/login', methods=['GET', 'POST'])
def login():
	cur = g.db.cursor()
	try:
		loggedIn = False
		requestData = json.loads(request.data)
		regnum = requestData['studentno']
		clientHash = requestData['hash']

		# User is logged in aleady.
		if 'username' in session:
			loggedIn = True
		elif request.method == 'POST':
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

			print 'db hash', hsh
			print 'temp salt hash', temphasher.hexdigest()
			print 'resultant hash', hasher.hexdigest()
			print 'client hash', clientHash


			if(hasher.hexdigest() != clientHash):
				loggedIn = False
			else:
				loggedIn = True
				session['username'] = request.form['username']
				session['user_role'] = user_role

		if loggedIn:
			return "{'status': 1}"
		else:
			return "{'status': 0}"
	finally:
		cur.close()
		session.pop('temp_salt', None)

def requires_auth(roles):
	def decorator(f):
		@wraps(f)
		def decorated(*args, **kwargs):
			# If no username is set, the user is not logged in.
			if not 'username' in session:
				return redirect(url_for('login'))
			else:
				if session['user_role'] not in roles:
					return redirect(url_for('login'))
			# TODO: add privilage checking here.
			return f(*args, **kwargs)
		return decorated
	return decorator
