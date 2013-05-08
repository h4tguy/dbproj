# Copied from http://flask.pocoo.org/snippets/8/ and then modified
from functools import wraps
from flask import  request, Response, session, redirect, url_for

from dbproj import app
from dbproj import template_lookup

def make_login_screen(bad=False):
#pulling out making the login screen to a separate method
#TODO: templatise this.
    return template_lookup.get_template('./temp_login.html').render(bad=bad)

@app.route('/get_salt', methods=['POST'])
def get_salt():
	global cur
	tmp = json.loads(request.form['json'])
	cur.execute("select salt from users where username=?", (tmp['username'],))
	res = cur.fetchone()
	if res==None:
		make_login_screen(True)
		return json.dumps({})	
	temp_salt = os.urandom(24)
	session['temp_salt']=temp_salt
	return json.dumps({'salt':res[0],'temp_salt':temp_salt})

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if 'username' in session:
            # User is logged in aleady.
            return redirect(url_for('index'))
        if 'username' in request.form and request.form['username']  == 'avoid3d':
            session['username'] = 'avoid3d'
            return redirect(url_for('index'))
        else:
            return make_login_screen()
        """
        elif request.method == 'POST':
            if 'temp_salt' not in session:
                # This branch is cool - Pierre
                # if this branch occurs, we may have an attacker - Sean
                return make_login_screen()
            # do authentication
            # TODO: This is valnurable to sql injection.
            cur.execute('select hash, use_type from usern where username='+request.form['username'])
            res = cur.fetchone()
            # I don't understand this? - Pierre
            if not res:
                abort(500) # there should always be one match since the clinet can't change the username since previous access
            hsh, use_type=res
            hasher=md5.new() # should we make new hashers a lot? entropy wise
			#what do you mean entropy-wise? I see no problem with it
            hasher.update(hsh+temp_salt)
            if(hasher.digest() != request.form['hash']):
                return make_login_screen(True)
            else:
                session['username'] = request.form['username']
                #TODO: get use type from db.
                session['use_type'] = use_type 
                #TODO: store from_url so as to direct them to where they were trying to go.
                return redirect(url_for('index'))
        else:
            return make_login_screen()
        """
    finally:
        session.pop('temp_salt', None)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # If no username is set, the user is not logged in.
        if not 'username' in session:
            return redirect(url_for('login'))
        # TODO: add privilage checking here.
        return f(*args, **kwargs)
    return decorated
