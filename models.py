import datetime

from argon2 import PasswordHasher
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from peewee import *

import config


class Todo(Model):
    '''This is the Model class for a ToDo item.'''
    name = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = config.DATABASE


def initialize():
    config.DATABASE.connect()
    config.DATABASE.create_tables([User, Todo], safe=True)
    config.DATABASE.close()
