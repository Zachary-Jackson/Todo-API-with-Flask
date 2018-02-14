from flask import g

from flask.ext.httpauth import HTTPBasicAuth

import models

basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
pass
