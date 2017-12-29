from peewee import Model, CharField, ForeignKeyField
from hackajob_phone_book_api import database as db


class Entry(Model):
    first_name = CharField(null=True)
    last_name = CharField(null=True)

    class Meta:
        database = db


class BaseElement(Model):
    value = CharField(null=True)

    class Meta:
        database = db


class Phone(BaseElement):
    entry = ForeignKeyField(rel_model=Entry, related_name='phones', on_delete='CASCADE')


class Email(BaseElement):
    entry = ForeignKeyField(rel_model=Entry, related_name='emails', on_delete='CASCADE')


class Address(BaseElement):
    entry = ForeignKeyField(rel_model=Entry, related_name='addresses', on_delete='CASCADE')
