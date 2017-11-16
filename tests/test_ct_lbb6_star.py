''' test_star.py'''

import falcon
from falcon import testing
import pytest
import sys
import os
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.app import api


@pytest.fixture
def client():
    '''API test client'''
    return testing.TestClient(api)


def test_star_valid(client):
    '''Test result of valid ct/lbb6/star API call'''
    expected_result = {
        "decimal": 7,
        "hz_orbit": 4,
        "hz_period": 1.848,
        "int_orbit": None,
        "luminosity": 2.584,
        "magnitude": 3.87,
        "mass": 1.2,
        "min_orbit": 0,
        "radius": 1.25,
        "size": "V",
        "temperature": 6420,
        "type": "F"
    }

    resp = client.simulate_get('/ct/lbb6/star/F7V')

    assert expected_result == resp.json
    assert resp.status == falcon.HTTP_200


def test_star_invalid(client):
    '''Test result of invalid ct/lbb6/star API call'''
    resp = client.simulate_get('/ct/lbb6/star/U')

    assert resp.status == falcon.HTTP_400
