# Copied from http://flask.pocoo.org/snippets/8/ and then modified
from functools import wraps
from flask import  request, Response, session, redirect, url_for
import json
from dbproj import app

# not sure if this is necessary anymore, just commenting out for now, sorry - Jarred
#def make_login_screen(bad=False):
#pulling out making the login screen to a separate method
#TODO: templatise this.
    #return template_lookup.get_template('./temp_login.html').render(bad=bad)

@app.route('/get_salt', methods=['POST'])
def get_salt():
    '''
    NOTE TO SEAN: Sorry about this gorilla commenting stuff out, just wanted to get the json working. - Jarred
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
    '''
    print 'This is what the client sent:'
    print request.data

    # fake some data back to the client
    tmp = json.dumps({'studentno': 'pfiekk345', 'salt': '12345', 'temp_salt': '67890'})
    return tmp

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    NOTE TO SEAN: Here I go again! sorry - Jarred.
    try:
        if 'username' in session:
            # User is logged in aleady.
            return redirect(url_for('index'))
        if 'username' in request.form and request.form['username']  == 'avoid3d':
            session['username'] = 'avoid3d'
            return redirect(url_for('index'))
        else:
            # adjusting this too, sorry once again, just trying to test without the templating - Jarred
            #return make_login_screen()
            return redirect(url_for('index'))
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
                session['user_role'] = user_role
                #TODO: store from_url so as to direct them to where they were trying to go.
                return redirect(url_for('index'))
        else:
            return make_login_screen()
        """
    finally:
        session.pop('temp_salt', None)
    '''
    print 'This is what the client sent:'
    print request.data
    # sending back dummy status
    return json.dumps({'status': 'true'})

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
