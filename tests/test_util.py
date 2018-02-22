'''test_util.py'''

# pylint: disable=E0402

import falcon
from falcon import testing
import pytest
import sys
import os
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
print(sys.path)
from traveller_api.app import api
from traveller_api.util import parse_query_string


@pytest.fixture
def client():
    '''API test client'''
    return testing.TestClient(api)


def test_parse_query_string_ok(client):
    '''Test valid query string'''
    for query_strings in ['foo=value1&bar=value2', '']:
        query_string = 'foo=value1&bar=value2'
        valid_params = {
            'foo': '',
            'bar': ''
        }
        expected_query_parameters = {
            'foo': 'value1',
            'bar': 'value2'
        }
        actual_query_parameters = parse_query_string(
            query_string,
            valid_params)
        assert expected_query_parameters == actual_query_parameters


def test_parse_query_string_bogus(client):
    '''Test bogus query string'''
    query_string = 'bogus=oh_yes'
    valid_params = {
        'foo': '',
        'bar': ''
    }

    with pytest.raises(falcon.HTTPInvalidParam):
        actual_query_parameters = parse_query_string(
            query_string=query_string,
            valid_query_parameters=valid_params)
        del actual_query_parameters
