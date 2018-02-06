from flask import Blueprint, jsonify

from flask.ext.restful import (Api, fields, inputs, marshal,
                               marshal_with, reqparse, Resource, url_for)

import models

TODO_FIELDS = {
    'id': fields.Integer,
    'name': fields.String
}


class Todo(Resource):
    '''This class defines what happens when HTTP requests are used.'''
    def get(self):
        '''Returns all Todo objects in the database.'''
        todos = [marshal(todo, TODO_FIELDS) for todo in models.Todo.select()]
        return todos


# This section registers the Todo API with a Blueprint
todo_api = Blueprint('resources.todo', __name__)
api = Api(todo_api)
api.add_resource(
    Todo,
    '/todos/',
    endpoint='todos'
)
