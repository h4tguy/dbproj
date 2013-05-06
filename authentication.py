# Copied from http://flask.pocoo.org/snippets/8/ and then modified
from functools import wraps
from flask import request, Response, session, redirect, url_for

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'secret'

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # If no username is set, the user is not logged in.
        if not session['username']:
            return redirect(url_for('login'))
        # TODO: add privilage checking here.
        return f(*args, **kwargs)
    return decorated

