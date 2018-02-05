from flask import Blueprint, jsonify

from flask.ext.restful import (Api, Resource)

TEST_JSON = [{'name': 'Get groceries'}, {'name': 'Go to the park'}]


class Todo(Resource):
    '''This class defines what happens when HTTP requests are used.'''
    def get(self):
        return jsonify([
            {'name': 'Take the garbage.'},
            {'name': 'Go to the store.'},
            {'name': 'Feed the dog.'},
            {'name': 'Get the GET API working.'}
        ])


# This section registers the Todo API with a Blueprint
todo_api = Blueprint('resources.todo', __name__)
api = Api(todo_api)
api.add_resource(
    Todo,
    '/todos/',
    endpoint='/todos/'
)
