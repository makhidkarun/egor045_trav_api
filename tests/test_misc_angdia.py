'''test_misc_angdia.py'''

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


def test_angdia_valid(client):
    '''Test result of valid misc/angdia API call'''
    expected_result = {
        "ang_dia_deg": 36.87,
        "ang_dia_rad": 1
    }
    resp = client.simulate_get('/misc/angdia/4/3')

    assert expected_result == resp.json
    assert resp.status == falcon.HTTP_200
