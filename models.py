import datetime

from argon2 import PasswordHasher
from flask_login import UserMixin
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from peewee import *

import config

HASHER = PasswordHasher()

DATABASE = SqliteDatabase('todos.sqlite')


class Todo(Model):
    """This is the Model class for a ToDo item."""
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class User(Model, UserMixin):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def user_create(cls, username, password):
        """This tries to create a User unless the user is already created."""
        try:
            cls.select().where(cls.username**username).get()
        except cls.DoesNotExist:
            user = cls(username=username)
            user.password = user.create_password(password)
            user.save()
            return user
        else:
            raise Exception("A user with that username already exists.")

    @staticmethod
    def verify_auth_token(token):
        """This checks to see if the given token is correct."""
        serializer = Serializer(config.SECRET_KEY)
        try:
            data = serializer.loads(token)
        except (SignatureExpired, BadSignature):
            return None
        else:
            user = User.get(User.id == data['id'])
            return user

    @staticmethod
    def create_password(password):
        """This hashes a given password."""
        return HASHER.hash(password)

    def verify_password(self, password):
        """This checks that a given password and the user's password match."""
        return HASHER.verify(self.password, password)

    def generate_auth_token(self, expires=36000):
        """This genereates an authentication token"""
        serializer = Serializer(config.SECRET_KEY, expires_in=expires)
        return serializer.dumps({'id': self.id})


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Todo], safe=True)
    DATABASE.close()


initialize()
