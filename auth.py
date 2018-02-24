from flask import g

from flask_httpauth import HTTPBasicAuth

import models

basic_auth = HTTPBasicAuth()
auth = basic_auth


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
