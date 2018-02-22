from operator import attrgetter

from flask import Blueprint

from flask_restful import (Api, fields, marshal,
                           marshal_with, reqparse, Resource, url_for)

from auth import auth
import models

TODO_FIELDS = {
    'id': fields.Integer,
    'name': fields.String
}


def todo_validation(todo_id):
    '''This tries to find a todo instand with the given id. If not
    this function returns False'''
    try:
        models.Todo.get(models.Todo.id == todo_id)
    except models.Todo.DoesNotExist:
        return False
    else:
        return True


class TodoList(Resource):
    '''This class defines what happens when HTTP requests are used without
    an item id number.'''
    def __init__(self):
        '''Initializes reqparse to be used later on.'''
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='You must provide a name for your Todo object.',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        '''Returns all Todo objects in the database.'''
        sorted_todos = sorted(
            models.Todo.select(), key=attrgetter('created_at'), reverse=True)
        todos = [marshal(todo, TODO_FIELDS) for todo in sorted_todos]
        return todos

    @marshal_with(TODO_FIELDS)
    @auth.login_required
    def post(self):
        args = self.reqparse.parse_args()
        todo = models.Todo.create(**args)
        return (todo, 201,
                {'Location': url_for('resources.todo.todo', id=todo.id)})


class Todo(Resource):
    '''This class defines what happens to HTTP requests of a certain item.'''
    def __init__(self):
        '''Initializes reqparse to be used later on.'''
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='You must provide an updated name argument.',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(TODO_FIELDS)
    @auth.login_required
    def put(self, id):
        if todo_validation(id):
            args = self.reqparse.parse_args()
            query = models.Todo.update(**args).where(models.Todo.id == id)
            query.execute()
            todo = models.Todo.get(models.Todo.id == id)
            return (todo, 200,
                    {'Location': url_for('resources.todo.todo', id=id)})
        return (
            'The todo id ({}) you tried '.format(id) +
            'to update does not exist.', 404)

    @auth.login_required
    def delete(self, id):
        '''This tries to delete a Todo object in the database.'''
        if todo_validation(id):
            query = models.Todo.delete().where(models.Todo.id == id)
            query.execute()
            return ('', 204)
        return (
            'The todo id ({}) you tried '.format(id) +
            'to delete does not exist.', 404)


# This section registers the Todo API with a Blueprint
todo_api = Blueprint('resources.todo', __name__)
api = Api(todo_api)
api.add_resource(
    TodoList,
    '/todos',
    endpoint='todos'
)
api.add_resource(
    Todo,
    '/todos/<int:id>',
    endpoint='todo'
)
