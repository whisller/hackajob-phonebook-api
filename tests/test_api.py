import json

import pytest
import requests
from flask import url_for
from hackajob_phone_book_api import API_AUTH


@pytest.mark.usefixtures('live_server')
class TestAuth:
    def test_it_handles_not_authorised_users(self):
        r = requests.get(url_for('get_one', entry_id=404, _external=True))
        assert r.status_code == 401


@pytest.mark.usefixtures('live_server')
class TestGet:
    def test_handles_situation_when_entry_does_not_exist(self):
        r = requests.get(url_for('get_one', entry_id=404, _external=True), auth=API_AUTH)
        assert r.status_code == 404
        assert json.loads(r.text) == {'err': 'Entity with id "404" does not exist.'}

    def test_get_one_entry(self):
        r = requests.get(url_for('get_one', entry_id=1, _external=True), auth=API_AUTH)
        assert r.status_code == 200
        assert json.loads(r.text) == {'addresses': [{'id': 1, 'value': 'Room 67 \n14 Tottenham Court Road \nLondon '
                                                                       '\nEngland\\W1T 1JY'}],
                                      'emails': [{'id': 1, 'value': 'john.doe@example.com'}],
                                      'first_name': 'John', 'id': 1, 'last_name': 'Doe',
                                      'phones': [{'id': 1, 'value': '12345678'},
                                                 {'id': 2, 'value': '87654321'}]}


@pytest.mark.usefixtures('live_server')
class TestPost:
    def test_no_payload(self):
        r = requests.post(url_for('create_one', _external=True), auth=API_AUTH)
        assert r.status_code == 400
        assert json.loads(r.text) == {'err': 'Please provide payload'}

    def test_creates_entry(self):
        r = requests.post(url_for('create_one', _external=True),
                          json={'addresses': [{'value': 'Box 777 \n91 Western Road \nBrighton \nEngland\\BN1 2NW'}],
                                'emails': [{'value': 'john.rambo@example.com'}],
                                'first_name': 'John', 'last_name': 'Rambo',
                                'phones': [{'value': '999999999'},
                                           {'value': '111111111'}]},
                          auth=API_AUTH)
        assert r.status_code == 200
        assert json.loads(r.text) == {'addresses': [], 'emails': [{'id': 2, 'value': 'john.rambo@example.com'}],
                                      'first_name': 'John', 'id': 2, 'last_name': 'Rambo',
                                      'phones': [{'id': 3, 'value': '999999999'}, {'id': 4, 'value': '111111111'}]}


@pytest.mark.usefixtures('live_server')
class TestDelete:
    def test_it_deletes_entry(self):
        r = requests.delete(url_for('delete_one', entry_id=1, _external=True), auth=API_AUTH)
        assert r.status_code == 200

        r = requests.get(url_for('get_one', entry_id=1, _external=True), auth=API_AUTH)
        assert r.status_code == 404
