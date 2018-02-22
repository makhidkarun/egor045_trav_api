'''test_basic_api.py'''

# pylint: disable=E402

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


def test_bogus_url(client):
    '''Test bogus API call'''
    resp = client.simulate_get('/bogus_api_call/42')

    assert resp.status == falcon.HTTP_404
