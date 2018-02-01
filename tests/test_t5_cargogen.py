'''test_t5_cargogen.py'''

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


def test_source_valid(client):
    '''Test valid t5/cargogen/source/<uwp>'''
    source_uwp = 'A646930-D'
    expected_result = {
        "cargo": "D-Hi In Cr2,300 Isotopes",
        "cost": 2300,
        "description": "Isotopes",
        "source": {
            "trade_codes": [
                "Hi",
                "In",
                "Ht"
            ],
            "uwp": "A646930-D"
        },
        "tech level": 13
    }
    resp = client.simulate_get('/t5/cargogen/source/{}'.format(source_uwp))
    for key in ['cost', 'source', 'tech level']:
        assert resp.json[key] == expected_result[key]
    assert resp.status == falcon.HTTP_200


def test_source_invalid(client):
    '''Test /t5/cargogen/source/<bogus_uwp>'''
    source_uwp = 'Foo'
    resp = client.simulate_get('/t5/cargogen/source/{}'.format(source_uwp))
    assert resp.status == falcon.HTTP_400
