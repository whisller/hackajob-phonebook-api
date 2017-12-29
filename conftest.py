import pytest

from hackajob_phone_book_api import database
from hackajob_phone_book_api.api import app as flask_api
from hackajob_phone_book_api.models import Entry, Phone, Email, Address


@pytest.fixture
def app():
    tables = (Entry, Phone, Email, Address)

    with database.execution_context():
        database.drop_tables(tables, safe=True)
        database.create_tables(tables, safe=True)

        e = Entry.create(id=1, first_name='John', last_name='Doe')
        Phone.create(entry=e, field_type='mobile', value='12345678')
        Phone.create(entry=e, field_type='mobile', value='87654321')
        Address.create(entry=e, field_type='address',
                       value='Room 67 \n14 Tottenham Court Road \nLondon \nEngland\W1T 1JY')
        Email.create(entry=e, field_type='email', value='john.doe@example.com')

    return flask_api
