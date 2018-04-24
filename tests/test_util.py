'''test_util.py'''

# pragma pylint: disable=E0402, W0621, C0413, W0613, C0103

import logging
import sys
import os
import unittest
import falcon
from falcon import testing
import pytest
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
print(sys.path)
from traveller_api.app import api
from traveller_api.util import parse_query_string, RequestProcessor

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


@pytest.fixture
def client():
    '''API test client'''
    return testing.TestClient(api)


def test_parse_query_string_ok(client):
    '''Test valid query string'''
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

    with pytest.raises(falcon.HTTPError):
        actual_query_parameters = parse_query_string(
            query_string=query_string,
            valid_query_parameters=valid_params)
        del actual_query_parameters


def test_ping(client):
    '''Test ping endpoint'''
    resp = client.simulate_get(
        '/ping'
    )
    assert resp.json["status"] == "OK"


class DummyRequest(object):
    '''Dummy request object for testing get_doc()'''

    def __init__(self):
        self.prefix = 'http://unittest'


class TestRequestProcessor(unittest.TestCase):
    '''Test RequestProcessor methods'''

    def setUp(self):
        '''Set up RequestProcessor object'''
        self.rp = RequestProcessor()
        self.rp.query_parameters = {
            'string': '',
            'number': None,
            'list': []
        }

    def tearDown(self):
        '''Tear down RequestProcessor object'''
        del self.rp

    def test_parse_query_string(self):
        '''Test parse_query_string() method'''
        query_string = 'string=how+long&list=item1&list=item2'
        self.rp.parse_query_string(query_string)
        self.assertTrue(
            self.rp.query_parameters['string'] == 'how+long')
        self.assertTrue(
            sorted(self.rp.query_parameters['list']) == ['item1', 'item2'])

        # Empty query string
        self.rp.query_parameters = {
            'string': '',
            'number': None,
            'list': [],
            'boolean': True
        }
        query_string = ''
        self.rp.parse_query_string(query_string)
        self.assertTrue(self.rp.query_parameters['string'] == '')
        self.assertTrue(self.rp.query_parameters['number'] is None)
        self.assertTrue(self.rp.query_parameters['list'] == [])
        self.assertTrue(self.rp.query_parameters['boolean'] is True)

        # Repeated list
        query_string = 'list=item1&list=item1'
        self.rp.query_parameters['list'] = []
        self.rp.parse_query_string(query_string)
        LOGGER.debug(
            'query_parameters["list"] = %s',
            self.rp.query_parameters['list'])
        self.assertTrue(
            self.rp.query_parameters['list'] == ['item1']
        )

        # Boolean
        query_string = 'boolean=false'
        self.rp.parse_query_string(query_string)
        self.assertTrue(self.rp.query_parameters['boolean'] is False)
        query_string = 'boolean=tRuE'
        self.rp.parse_query_string(query_string)
        self.assertTrue(self.rp.query_parameters['boolean'] is True)

    def test_get_doc(self):
        '''Test get_doc() method'''
        req = DummyRequest()
        LOGGER.debug('rp.get_doc(req) = %s', self.rp.get_doc(req))
        self.assertTrue(self.rp.get_doc(req)['doc'] == 'Request processor')

    def test_get_doc_json(self):
        '''Test get_doc_json() method()'''
        req = DummyRequest()
        LOGGER.debug('rp.get_doc(req) = %s', self.rp.get_doc(req))
        self.assertTrue(self.rp.get_doc(req)['doc'] == 'Request processor')
