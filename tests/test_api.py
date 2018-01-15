import base64
import json

from hackajob_phone_book_api import API_AUTH, database
from hackajob_phone_book_api.api import app
from hackajob_phone_book_api.models import Entry, Phone, Email, Address

auth = {'Authorization': 'Basic ' + base64.b64encode(bytes(':'.join(API_AUTH), 'ascii')).decode('ascii')}


class TestAuth:
    def test_it_handles_not_authorised_users(self):
        with app.test_client() as c:
            r = c.get('/entries/404')
        assert r.status_code == 401


class TestGet:
    def setup_method(self, method):
        reset_database()

    def test_handles_situation_when_entry_does_not_exist(self):
        with app.test_client() as c:
            r = c.get('/entries/404', headers=auth)
        assert r.status_code == 404
        assert json.loads(r.data) == {'err': 'Entity with id "404" does not exist.'}

    def test_get_one_entry(self):
        with app.test_client() as c:
            r = c.get('/entries/1', headers=auth)
        assert r.status_code == 200
        assert json.loads(r.data) == {'addresses': [{'id': 1, 'value': 'Room 67 \n14 Tottenham Court Road \nLondon '
                                                                       '\nEngland\\W1T 1JY'}],
                                      'emails': [{'id': 1, 'value': 'john.doe@example.com'}],
                                      'first_name': 'John', 'id': 1, 'last_name': 'Doe',
                                      'phones': [{'id': 1, 'value': '12345678'},
                                                 {'id': 2, 'value': '87654321'}]}


class TestPost:
    def setup_method(self, method):
        reset_database()

    def test_no_payload(self):
        with app.test_client() as c:
            r = c.post('/entries', headers=auth)
        assert r.status_code == 400
        assert json.loads(r.data) == {'err': 'Please provide payload'}

    def test_creates_entry(self):
        with app.test_client() as c:
            r = c.post('/entries',
                       data=json.dumps(
                           {'addresses': [{'value': 'Box 777 \n91 Western Road \nBrighton \nEngland\\BN1 2NW'}],
                            'emails': [{'value': 'john.rambo@example.com'}],
                            'first_name': 'John', 'last_name': 'Rambo',
                            'phones': [{'value': '999999999'},
                                       {'value': '111111111'}]}),
                       headers=auth)
        assert r.status_code == 200
        assert json.loads(r.data) == {'addresses': [], 'emails': [{'id': 2, 'value': 'john.rambo@example.com'}],
                                      'first_name': 'John', 'id': 2, 'last_name': 'Rambo',
                                      'phones': [{'id': 3, 'value': '999999999'}, {'id': 4, 'value': '111111111'}]}


class TestDelete:
    def test_it_deletes_entry(self):
        with app.test_client() as c:
            r = c.delete('/entries/1', headers=auth)
            assert r.status_code == 200

            r = c.get('/entries/1', headers=auth)
            assert r.status_code == 404


def reset_database():
    tables = (Entry, Phone, Email, Address)

    database.drop_tables(tables, safe=True)
    database.create_tables(tables, safe=True)

    entry = Entry.create(first_name='John', last_name='Doe')
    Address.create(value='Room 67 \n14 Tottenham Court Road \nLondon \nEngland\\W1T 1JY', entry=entry)
    Email.create(value='john.doe@example.com', entry=entry)
    Phone.create(value='12345678', entry=entry)
    Phone.create(value='87654321', entry=entry)

    database.close()
