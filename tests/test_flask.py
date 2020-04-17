import pytest
from beacon import flask_app
import re


def test_home(client):
    rv = client.get('/')
    b_true = re.match(rv.data.decode('utf-8')[365:421],'1-1-A-A')
    b_false = re.match(rv.data.decode('utf-8')[365:421],'24-1-A-A')
    assert b_true
    assert b_false is None
    assert 'Submit' in rv.data.decode('utf-8')
    assert 'SWP' in rv.data.decode('utf-8')
    assert 'Search' in rv.data.decode('utf-8')
    assert rv.status_code is 200
    


def test_handle(client):
    rv = client.post('/results', data={'var': '1-1-A-A'})
    assert rv.status_code is 200
    assert b'Results'in rv.data
    assert b'Your variant 1-1-A-A was found.' or b'Your variant 1-1-A-A was not found.' or b'An Error has occured: no such table: variants' in rv.data
    assert b'go Home' in rv.data