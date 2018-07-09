import base64
import json
import unittest

from playhouse.test_utils import test_database
from peewee import *

from app import app
from models import Todo, User

TODO_LIST_URL = 'http://localhost:8000/api/v1/todos'
# Add a number to this url for it to work.
TODO_ITEM_URL = 'http://localhost:8000/api/v1/todos/{}'

# BASIC_AUTH_HEADERS presumes a username of 'username' and a password of
# 'password'
BASIC_AUTH_HEADERS = {'Authorization': 'Basic ' +
                      base64.b64encode('username:password'.encode()).decode()}

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()
TEST_DB.create_tables([User, Todo], safe=True)


class TodoModelTestCase(unittest.TestCase):
    """This tests the Todo model."""
    def test_todo_creation(self):
        """This tests the creation of a Todo object."""
        with test_database(TEST_DB, (User, Todo)):
            Todo.create(
                name='Plant some seeds in the garden.'
            )
            self.assertEqual(Todo.select().count(), 1)


class UserModelTestCase(unittest.TestCase):
    """This tests the User model."""
    def test_todo_creation(self):
        """This tests the creation of a Todo object."""
        with test_database(TEST_DB, (User, Todo)):
            User.create(
                username='username',
                password='password'
            )
            self.assertEqual(User.select().count(), 1)

    def test_duplicate_todo_creation(self):
        """This tests the creation of a duplicate Todo object."""
        with test_database(TEST_DB, (User, Todo)):
            User.create(
                username='username',
                password='password'
            )
            with self.assertRaises(Exception):
                User.create(
                    username='username',
                    password='password'
                )


class ViewTestCase(unittest.TestCase):
    """This sets up the Flask app for testing."""
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()


class LoginpageViewTestCase(ViewTestCase):
    """This tests that the login page looks correct."""
    def test_login_HTTP_status(self):
        """This ensures that the application's loginpage works."""
        with test_database(TEST_DB, (User, Todo)):
            result = self.app.get('/login')
            self.assertEqual(result.status_code, 200)
            self.assertIn("Username", result.data.decode())
            self.assertIn("Password", result.data.decode())
            self.assertNotIn("Confirm Password", result.data.decode())

    def test_login_form(self):
        """This tests to see if the LoginForm works."""
        with test_database(TEST_DB, (User, Todo)):
            User.user_create(
                username='username',
                password='password'
            )

            self.app.get('/login')
            form = {'username': 'username',
                    'password': 'password'}
            response = self.app.post('/login', data=form)
            self.assertEqual(response.status_code, 302)

    def test_bad_login_form(self):
        """This tests to see if the LoginForm works."""
        with test_database(TEST_DB, (User, Todo)):
            User.user_create(
                username='username',
                password='password'
            )

            self.app.get('/login')
            form = {'username': 'username',
                    'password': 'incorrect'}
            response = self.app.post('/login', data=form)
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                "The username or password you interred is incorrect",
                response.data.decode()
            )


class HomepageViewTestCase(ViewTestCase):
    """This tests that the homepage looks correct."""
    def test_homepage_HTTP_status(self):
        """This ensures that the application's homepage works."""
        with test_database(TEST_DB, (User, Todo)):
            result = self.app.get('/')
            self.assertEqual(result.status_code, 200)

    def test_homepage_information(self):
        """This checks to see if the title and new task button is found"""
        with test_database(TEST_DB, (User, Todo)):
            result = self.app.get('/')
            self.assertIn("Add a New Task", result.data.decode())


class RegisterViewTestCase(ViewTestCase):
    """This tests that the register page looks correct."""
    def test_register_HTTP_status(self):
        """This ensures that the application's register page works."""
        with test_database(TEST_DB, (User, Todo)):
            result = self.app.get('/register')
            self.assertEqual(result.status_code, 200)
            self.assertIn("Username", result.data.decode())
            self.assertIn("Confirm Password", result.data.decode())

    def test_register_form(self):
        """This tests to see if the RegisterForm works."""
        with test_database(TEST_DB, (User, Todo)):
            self.app.get('/register')
            form = {'username': 'username',
                    'password': 'password',
                    'password2': 'password'}
            response = self.app.post('/register', data=form)
            self.assertEqual(response.status_code, 302)

            # This checks to see if we actually created a new user
            self.assertTrue(User.get(User.username == 'username'))

    def test_bad_register_form(self):
        """This tests to see if the RegisterForm works."""
        with test_database(TEST_DB, (User, Todo)):
            self.app.get('/register')
            form = {'username': 'username',
                    'password': 'password',
                    'password2': 'incorrect'}
            response = self.app.post('/register', data=form)
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                "Passwords must match",
                response.data.decode()
            )


class APITestCase(ViewTestCase):
    """This ensures that the API is working correctly."""

    def test_create_user(self):
        """This checks to see if create user via API works"""
        with test_database(TEST_DB, (User, Todo)):
            data = {
                'username': 'test',
                'password': 'password',
                'password_verification': 'password'
            }
            user_url = 'http://localhost:8000/api/v1/users'

            # This has created our first user
            response = self.app.post(
                user_url, data=data, headers=BASIC_AUTH_HEADERS
            )

            # This converts the response from JSON to a python dict
            response_decoded = response.data.decode("utf-8")
            response_decoded = json.loads(response_decoded)

            self.assertTrue(type(response.data) is bytes)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(
                response_decoded,
                {"username": "test"})

            # This tests the creation of a second user with the same name
            response = self.app.post(
                user_url, data=data, headers=BASIC_AUTH_HEADERS
            )

            response_decoded = response.data.decode("utf-8")
            response_decoded = json.loads(response_decoded)

            self.assertTrue(type(response.data) is bytes)
            self.assertEqual(
                response_decoded,
                {"error": "A user with that username already exists"})

            # This checks the creation of a user with an invalid password
            data = {
                'username': 'test',
                'password': 'password',
                'password_verification': 'incorrect password'
            }
            response = self.app.post(
                user_url, data=data, headers=BASIC_AUTH_HEADERS
            )

            response_decoded = response.data.decode("utf-8")
            response_decoded = json.loads(response_decoded)

            self.assertTrue(type(response.data) is bytes)
            self.assertEqual(
                response_decoded,
                {"error": "password and password_verification do not match"})

    def test_todo_list_get(self):
        """This checks to see if the TodoList GET api is working."""
        with test_database(TEST_DB, (User, Todo)):
            Todo.create(
                name='Plant some seeds in the garden.'
            )
            # This gets the api response from the server
            response = self.app.get(TODO_LIST_URL)

            # This converts the response from JSON to a python dict
            response_decoded = response.data.decode("utf-8")
            response_decoded = json.loads(response_decoded)

            self.assertTrue(type(response.data) is bytes)
            self.assertEqual(response.status_code, 200)

            # id should be 1 because it is the first item in the database.
            # Name should be the value created above.
            self.assertEqual(
                response_decoded,
                [{"id": 1, "name": "Plant some seeds in the garden."}])

    def test_todo_list_post(self):
        """This checks to see if the TodoList POST api is working."""
        with test_database(TEST_DB, (User, Todo)):
            User.user_create(
                username='username',
                password='password'
            )

            data = {'name': 'Going to the grocery store'}
            response = self.app.post(
                TODO_LIST_URL, data=data, headers=BASIC_AUTH_HEADERS
            )

            # This converts the response from JSON to a python dict
            response_decoded = response.data.decode("utf-8")
            response_decoded = json.loads(response_decoded)

            self.assertTrue(type(response.data) is bytes)
            self.assertEqual(response.status_code, 201)

            # id should be 1 because it is the first item in the database.
            # Name should be the value created above.
            self.assertEqual(
                response_decoded,
                {'id': 1, 'name': 'Going to the grocery store'})
            todo_object = Todo.get(Todo.id == 1)
            self.assertEqual(todo_object.name, 'Going to the grocery store')

    def test_todo_list_post_unauthorized(self):
        """This checks to see if the TodoList POST api is working."""
        with test_database(TEST_DB, (User, Todo)):
            data = {'name': 'Going to the grocery store'}
            response = self.app.post(TODO_LIST_URL, data=data)
            self.assertEqual(response.status_code, 401)

    def test_todo_put(self):
        """This checks to see if the Todo PUT api is working."""
        with test_database(TEST_DB, (User, Todo)):
            User.user_create(
                username='username',
                password='password'
            )

            Todo.create(
                name='Plant some seeds in the garden.'
            )

            # This converts a python dictionary to JSON to send to the API
            data = {"id": 1, "name": "Water the seeds in the garden."}
            response = self.app.put(TODO_ITEM_URL.format(1), data=data,
                                    headers=BASIC_AUTH_HEADERS)

            # This converts the response from JSON to a python dict
            response_decoded = response.data.decode("utf-8")
            response_decoded = json.loads(response_decoded)

            self.assertTrue(type(response.data) is bytes)
            self.assertEqual(response.status_code, 200)
            # id should be 1 because it is the first item in the database.
            # Name should be the new value created above.
            # The response should not be a list, but a dict.
            self.assertEqual(
                response_decoded,
                {"id": 1, "name": "Water the seeds in the garden."})

    def test_todo_put_token(self):
        """This checks to see if the Todo PUT api is working."""
        with test_database(TEST_DB, (User, Todo)):
            user = User.user_create(
                username='username',
                password='password'
            )

            Todo.create(
                name='Plant some seeds in the garden.'
            )

            token = user.generate_auth_token().decode('ascii')
            headers = {'Authorization': 'Token {}'.format(token)}

            # This converts a python dictionary to JSON to send to the API
            data = {"id": 1, "name": "Water the seeds in the garden."}
            response = self.app.put(TODO_ITEM_URL.format(1), data=data,
                                    headers=headers)

            # This converts the response from JSON to a python dict
            response_decoded = response.data.decode("utf-8")
            response_decoded = json.loads(response_decoded)

            self.assertTrue(type(response.data) is bytes)
            self.assertEqual(response.status_code, 200)
            # id should be 1 because it is the first item in the database.
            # Name should be the new value created above.
            # The response should not be a list, but a dict.
            self.assertEqual(
                response_decoded,
                {"id": 1, "name": "Water the seeds in the garden."})

    def test_todo_put_unauthorized(self):
        """This checks to see if the Todo PUT api is working."""
        with test_database(TEST_DB, (User, Todo)):
            Todo.create(
                name='Plant some seeds in the garden.'
            )
            # This converts a python dictionary to JSON to send to the API
            data = {"id": 1, "name": "Water the seeds in the garden."}
            response = self.app.put(TODO_ITEM_URL.format(1), data=data)
            self.assertEqual(response.status_code, 401)

    def test_todo_delete(self):
        """This checks to see if the Todo DELETE API is working."""
        with test_database(TEST_DB, (User, Todo)):
            User.user_create(
                username='username',
                password='password'
            )

            Todo.create(
                name='Plant some seeds in the garden.'
            )

            response = self.app.delete(TODO_ITEM_URL.format(1),
                                       headers=BASIC_AUTH_HEADERS)
            self.assertEqual(response.status_code, 204)
            # This tests to see if the Todo object is in the database.
            self.assertEqual(Todo.select().count(), 0)

    def test_todo_delete_token(self):
        """This checks to see if the Todo DELETE API is working."""
        with test_database(TEST_DB, (User, Todo)):
            user = User.user_create(
                username='username',
                password='password'
            )

            Todo.create(
                name='Plant some seeds in the garden.'
            )

            token = user.generate_auth_token().decode('ascii')
            headers = {'Authorization': 'Token {}'.format(token)}

            response = self.app.delete(TODO_ITEM_URL.format(1),
                                       headers=headers)
            self.assertEqual(response.status_code, 204)
            # This tests to see if the Todo object is in the database.
            self.assertEqual(Todo.select().count(), 0)

    def test_todo_delete_unauthorized(self):
        """This checks to see if the Todo DELETE API is working."""
        with test_database(TEST_DB, (User, Todo)):
            Todo.create(
                name='Plant some seeds in the garden.'
            )
            response = self.app.delete(TODO_ITEM_URL.format(1))
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
