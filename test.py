import unittest

from app import app

TODO_LIST_URL = 'http://localhost:8000/api/v1/todos'
# Add a number to this url for it to work.
TODO_ITEM_URL = 'http://localhost:8000/api/v1/todos/{}'


class TodoApplicationTests(unittest.TestCase):
    def setUp(self):
        '''This prepares the test_client for testing.'''
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_homepage_HTTP_status(self):
        '''This ensures that the application's homepage works.'''
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_homepage_information(self):
        '''This checks to see if the title and new task button is found'''
        result = self.app.get('/')
        self.assertIn("My TODOs!", result.data.decode())
        self.assertIn("Add a New Task", result.data.decode())

    # def test_todo_list_get(self):
    #     '''This checks to see if the TodoList GET api is working.'''
    #     response = self.app.get(TODO_LIST_URL)
    #     import pdb; pdb.set_trace()


if __name__ == '__main__':
    unittest.main()
