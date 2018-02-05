from flask import Flask, g, jsonify, render_template


import resources.config
from resources.todo import todo_api

app = Flask(__name__)
app.register_blueprint(todo_api, url_prefix='/api/v1')


@app.route('/')
def my_todos():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=resources.config.DEBUG,
            host=resources.config.HOST, port=resources.config.PORT)
