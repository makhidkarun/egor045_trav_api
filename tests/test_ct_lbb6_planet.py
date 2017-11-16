'''test_ct_lbb6_planet.py'''

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


def test_planet_valid(client):
    '''Test result of valid ct/lbb6/star/orbit/planet API call'''
    expected_result = {
        "albedo": {
            "max": 0.581,
            "min": 0.293
        },
        "cloudiness": 0.6,
        "temperature": {
            "max": 303.644,
            "min": 179.953
        },
        "trade_classifications": [
            "Ag",
            "Ni"
        ],
        "uwp": "A798565-A"
    }

    resp = client.simulate_get('/ct/lbb6/star/G2V/orbit/3/planet/A798565-A')

    assert expected_result == resp.json
    assert resp.status == falcon.HTTP_200


def test_planet_invalid_uwp(client):
    '''Test result of invalid ct/lbb6/star/orbit/planet API call
    (invalid UWP)'''
    resp = client.simulate_get('/ct/lbb6/star/G2V/orbit/3/planet/A79856A')

    assert resp.status == falcon.HTTP_400
    assert resp.json == {'message': 'Invalid UWP'}


def test_planet_invalid_orbit(client):
    '''Test result of invalid ct/lbb6/star/orbit/planet API call
    (invalid UWP)'''
    resp = client.simulate_get('/ct/lbb6/star/G2V/orbit/999/planet/A79856-A')

    assert resp.status == falcon.HTTP_400
    assert resp.json == {'message': 'Invalid orbit number'}


def test_planet_invalid_star(client):
    '''Test result of invalid ct/lbb6/star/orbit/planet API call
    (invalid UWP)'''
    resp = client.simulate_get('/ct/lbb6/star/U/orbit/3/planet/A79856-A')

    assert resp.status == falcon.HTTP_400
    assert resp.json == {'message': 'Invalid star classification'}
