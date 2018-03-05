from flask import g

from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth

import models

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Token')
auth = MultiAuth(token_auth, basic_auth)


@basic_auth.get_password
def get_password(username):
    '''gets the provide user's password'''
    user = models.User.get(username=username)
    if user is not None:
        return user.password
    return None


@basic_auth.verify_password
def verify_password(username, password):
    '''Tries to authenticate a user and if so g.users them'''
    try:
        user = models.User.get(models.User.username == username)
        if not user.verify_password(password):
            return False
    except models.User.DoesNotExist:
        return False
    else:
        g.user = user
        return True


@token_auth.verify_token
def verify_token(token):
    '''Sends the token to the User model for verification'''
    # Not having these two lines of code bellow gave me tons of trouble
    # to figure out what was going on.
    if not token and g.user.is_authenticated:
        token = g.user.generate_auth_token()

    user = models.User.verify_auth_token(token)
    if user is not None:
        g.user = user
        return True
    return False
