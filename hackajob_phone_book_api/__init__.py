import os

from peewee import SqliteDatabase

API_AUTH = ('user', 'pass')
database = SqliteDatabase(os.environ['DATABASE'])
