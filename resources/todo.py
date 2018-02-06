from flask import Blueprint, jsonify

from flask.ext.restful import (Api, fields, inputs, marshal,
                               marshal_with, reqparse, Resource, url_for)

import models

TODO_FIELDS = {
    'id': fields.Integer,
    'name': fields.String
}


def todo_validation(todo_id):
    '''This tries to find a todo instand with the given id. If not
    this function returns False'''
    try:
        todo = models.Todo.get(models.Todo.id == todo_id)
    except models.Todo.DoesNotExist:
        return False
    else:
        return True


class TodoList(Resource):
    '''This class defines what happens when HTTP requests are used without
    an item id number.'''
    def get(self):
        '''Returns all Todo objects in the database.'''
        todos = [marshal(todo, TODO_FIELDS) for todo in models.Todo.select()]
        return todos


class Todo(Resource):
    '''This class defines what happens to HTTP requests of a certain item.'''
    def delete(self, id):
        '''This tries to delete a Todo object in the database.'''
        if todo_validation(id):
            query = models.Todo.delete().where(models.Todo.id == id)
            query.execute()
            return '', 204, {'Location': url_for('resources.todo.todos')}
        return (
            'The todo id ({}) you tried '.format(id) +
            'to delete does not exist.', 404)


# This section registers the Todo API with a Blueprint
todo_api = Blueprint('resources.todo', __name__)
api = Api(todo_api)
api.add_resource(
    TodoList,
    '/todos/',
    endpoint='todos'
)
api.add_resource(
    Todo,
    '/todos/<int:id>',
    endpoint='todo'
)
