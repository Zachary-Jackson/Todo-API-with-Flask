import json

from flask import Blueprint, make_response
from flask_restful import (Api, fields, marshal, Resource, reqparse)

import models

user_fields = {
    'username': fields.String,
}


class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password_verification',
            required=True,
            help='No password verification provided',
            location=['form', 'json']
        )
        super().__init__()

    def post(self):
        '''This checks to see if the can log in.'''
        args = self.reqparse.parse_args()
        if args.get('password') == args.get('password_verification'):
            user = models.User.create_user(**args)
            return marshal(user, user_fields), 201
        else:
            return make_response(
                json.dumps(
                    {'error':
                     'password and password_verification do not match'}, 400
                )
            )


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserList,
    '/users',
    endpoint='users'
)
