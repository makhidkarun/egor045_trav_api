'''test_api_t5_orbit.py'''

# pragma pylint: disable=relative-beyond-top-level
# pragma pylint: disable=C0413, E0401

import logging
import sys
import os
import pytest
import falcon
from falcon import testing
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.app import api
from traveller_api.t5.cargogen import CargoGen

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

@pytest.fixture
def client():
    '''API test client'''
    return testing.TestClient(api)


def test_api_valid_uwps(client):
    '''Test valid UWPs call'''

    resp = client.simulate_get(
        '/t5/cargogen',
        query_string='source_uwp=B56789C-A')

    expected = {
        'cost': 5000,
        'tech_level': 10,
        'source': {
            'trade_codes': ['Ph', 'Pa', 'Ri'],
            'uwp': 'B56789C-A'
        }
    }

    for key in ['cost', 'tech_level', 'source']:
        assert resp.json[key] == expected[key]
    assert resp.status == falcon.HTTP_200


def test_api_invalid_uwps(client):
    '''Test invalid orbit number call'''
    # Invalid type
    for uwp in [None, 'Foo', []]:
        resp = client.simulate_get(
            '/t5/cargogen',
            query_string='source_uwp={}'.format(uwp))
        assert resp.status == '400 Invalid parameter'
        resp = client.simulate_get(
            '/t5/cargogen',
            query_string='source_uwp=A867868-7&market_uwp={}'.format(uwp))
        assert resp.status == '400 Invalid parameter'

    resp = client.simulate_get('/t5/cargogen')  # Empty query string
    assert resp.status == '400 Invalid parameter'


def test_api_doc(client):
    '''Test API doc'''
    resp = client.simulate_get(
        '/t5/cargogen',
        query_string='doc=true')

    assert resp.status == falcon.HTTP_200
    assert resp.json['doc'] == CargoGen.__doc__.replace(
        '<apiserver>', 'http://falconframework.org')


def test_valid_broker(client):
    '''Test valid broker setting'''
    query_string = 'source_uwp=A867979-7'
    query_string += '&market_uwp=E421315-9'
    query_string += '&broker=2'
    LOGGER.debug('query_string = %s', query_string)
    
    resp = client.simulate_get(
        '/t5/cargogen',
        query_string=query_string)
    assert resp.status == falcon.HTTP_200


def test_invalid_broker(client):
    '''Test invalid broker'''
    query_string = 'source_uwp=A867979-7'
    query_string += '&market_uwp=E421315-9'
    query_string += '&broker=Two'
    LOGGER.debug('query_string = %s', query_string)
    
    resp = client.simulate_get(
        '/t5/cargogen',
        query_string=query_string)
    assert resp.status == '400 Invalid parameter'
