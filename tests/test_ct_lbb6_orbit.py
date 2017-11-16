'''test_ct_lbb6_orbit.py'''

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


def test_orbit_valid(client):
    '''Test result of valid ct/lbb6/star/orbit API call'''
    expected_result = {
        "angular_dia_deg": 0.416,
        "angular_dia_sun": 0.797,
        "au": 1.6,
        "mkm": 239.3,
        "period": 1.848
    }

    resp = client.simulate_get('/ct/lbb6/star/F7V/orbit/4')

    assert expected_result == resp.json
    assert resp.status == falcon.HTTP_200


def test_orbit_invalid(client):
    '''Test result of invalid ct/lbb6/star/orbit API call (invalid orbit)'''
    resp = client.simulate_get('/ct/lbb6/star/F7V/orbit/-1')

    assert resp.status == falcon.HTTP_400
    assert resp.json == {"message": "Invalid orbit number"}


def test_orbit_invalid_star(client):
    '''Test result of invalid ct/lbb6/star/orbit API call (invalid star)'''
    resp = client.simulate_get('/ct/lbb6/star/F7U/orbit/1')

    assert resp.status == falcon.HTTP_400
    assert resp.json == {"message": "Invalid star classification"}
