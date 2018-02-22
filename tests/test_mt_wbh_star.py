''' test_star.py'''

# pragma pylint: disable=relative-beyond-top-level

import pytest
import sys
import os
import falcon
from falcon import testing
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.app import api


@pytest.fixture
def client():
    '''API test client'''
    return testing.TestClient(api)


def test_star_valid(client):
    '''Test result of valid mt/wbh/star API call'''
    expected_result = {
        "decimal": 7,
        "hz_orbit": 4,
        "hz_period": 1.848,
        "int_orbit": None,
        "luminosity": 1.24,
        "mass": 1.2,
        "min_orbit": 0,
        "size": "V",
        "type": "F"
    }

    resp = client.simulate_get('/mt/wbh/star/F7V')

    assert expected_result == resp.json
    assert resp.status == falcon.HTTP_200


def test_star_invalid(client):
    '''Test result of invalid mt/wbh/star API call'''
    resp = client.simulate_get('/mt/wbh/star/U')

    assert resp.status == falcon.HTTP_400
