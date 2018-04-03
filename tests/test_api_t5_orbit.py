'''test_api_t5_orbit.py'''

# pragma pylint: disable=relative-beyond-top-level
# pragma pylint: disable=C0413, E0401

import sys
import os
import pytest
import falcon
from falcon import testing
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.app import api
from traveller_api.t5.orbit import Orbit

@pytest.fixture
def client():
    '''API test client'''
    return testing.TestClient(api)


def test_api_valid_orbit_number(client):
    '''Test valid orbit number call'''
    orbit_number = 3
    expected = {
        "au": 1.0,
        "mkm": 150,
        "orbit_number": 3.0
    }
    resp = client.simulate_get(
        '/t5/orbit',
        query_string='orbit_number={}'.format(orbit_number))

    for key in ['au', 'mkm', 'orbit_number']:
        assert resp.json[key] == expected[key]
    assert resp.status == falcon.HTTP_200


def test_api_invalid_orbit_number(client):
    '''Test invalid orbit number call'''
    # Invalid type
    for orbit_number in [None, 'Foo', []]:
        resp = client.simulate_get(
            '/t5/orbit',
            query_string='orbit_number={}'.format(orbit_number))
        assert resp.status == '400 Invalid parameter'

    # Value out of range
    for orbit_number in [-1, 23]:
        resp = client.simulate_get(
            '/t5/orbit',
            query_string='orbit_number={}'.format(orbit_number))
        assert resp.status == '400 Invalid parameter'


def test_api_doc(client):
    '''Test API doc'''
    resp = client.simulate_get(
        '/t5/orbit',
        query_string='doc=true')
    
    assert resp.status == falcon.HTTP_200
    assert resp.json['doc'] == Orbit.__doc__.replace(
        '<apiserver>', 'http://falconframework.org')
