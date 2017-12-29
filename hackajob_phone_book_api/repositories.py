from collections import OrderedDict

from peewee import PeeweeException, logger
from playhouse.shortcuts import model_to_dict, JOIN
from hackajob_phone_book_api import database
from hackajob_phone_book_api.exceptions import DoesNotExistException, GeneralException
from hackajob_phone_book_api.models import Entry, Phone, Email, Address


class EntryRepository:
    @staticmethod
    def get_one(phone_id):
        try:
            q = (Entry.
                 select(Entry, Phone, Email, Address)
                 .join(Phone)
                 .join(Email, JOIN.LEFT_OUTER, Email.entry == Entry.id)
                 .switch(Entry)
                 .join(Address, JOIN.LEFT_OUTER, Address.entry == Entry.id)
                 .switch(Entry)
                 .where(Entry.id == phone_id))

            return OrderedDict(model_to_dict(q.get(), backrefs=True))
        except Entry.DoesNotExist:
            raise DoesNotExistException('Entity with id "{}" does not exist.'.format(phone_id))
        except PeeweeException as e:
            logger.error(e)
            raise GeneralException()

    @staticmethod
    def create_one(model):
        with database.atomic() as nested_txn:
            try:
                e = Entry.create(first_name=model['first_name'], last_name=model['last_name'])

                for class_name in (Phone, Email, Address):
                    for el in model.get(class_name.__name__.lower() + 's', []):
                        class_name.create(entry=e, value=el['value'])

                return OrderedDict(model_to_dict(e, backrefs=True))
            except PeeweeException as e:
                nested_txn.rollback()
                logger.error(e)

                raise GeneralException()

    @staticmethod
    def delete_one(phone_id):
        try:
            Entry.delete().where(Entry.id == phone_id).execute()
        except PeeweeException as e:
            logger.error(e)
            raise GeneralException()
