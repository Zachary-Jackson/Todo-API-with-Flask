from flask import Flask, flash, g, redirect, render_template, url_for
from flask_login import (LoginManager, current_user, login_user,
                         logout_user, login_required)

import config
import forms
import models
from resources.todo import todo_api
from resources.users import users_api

app = Flask(__name__)
app.register_blueprint(todo_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/api/v1')
app.secret_key = config.SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'register'


@login_manager.user_loader
def load_user(userid):
    """This finds a user or returns None."""
    try:
        return models.User.get(id=userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def my_todos():
    '''This takes the user to the homepage.'''
    return render_template('index.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    '''This is the new user registration page.'''
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("You are registered!", "success")
        models.User.user_create(
            username=form.username.data,
            password=form.password.data
        )
        user = models.User.get(models.User.username == form.username.data)
        login_user(user)
        return redirect(url_for('my_todos'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=config.DEBUG,
            host=config.HOST, port=config.PORT)
