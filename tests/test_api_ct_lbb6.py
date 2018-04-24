'''test_api_ct_lbb6.py'''

# pragma pylint: disable=relative-beyond-top-level
# pragma pylint: disable=C0413, E0401, W0621

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
from traveller_api.ct.lbb6 import Star
from traveller_api.ct.lbb6 import Orbit
from traveller_api.ct.lbb6 import Planet

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

@pytest.fixture
def client():
    '''API test client'''
    return testing.TestClient(api)


def test_star_valid_code(client):
    '''Test valid code for star API'''
    for code in ['G2 V', 'G2V']:
        resp = client.simulate_get(
            '/ct/lbb6/star',
            query_string='code={}'.format(code)
        )
        expected = {
            "classification": "G2 V",
            "decimal": 2,
            "hz_orbit": 3,
            "hz_period": 1.0,
            "int_orbit": None,
            "luminosity": 0.994,
            "magnitude": 4.82,
            "mass": 1.0,
            "min_orbit": 0,
            "radius": 0.98,
            "size": "V",
            "temperature": 5800,
            "type": "G"
        }
        assert resp.json == expected
        assert resp.status == falcon.HTTP_200
    # Dwarf
    resp = client.simulate_get(
        '/ct/lbb6/star',
        query_string='code=MD'
    )
    expected = {
        "classification": "M D",
        "decimal": "",
        "hz_orbit": None,
        "hz_period": None,
        "int_orbit": None,
        "luminosity": 3e-05,
        "magnitude": 15.9,
        "mass": 1.11,
        "min_orbit": 0,
        "radius": 0.01,
        "size": "D",
        "temperature": 2700,
        "type": "M"
    }
    assert resp.json == expected
    assert resp.status == falcon.HTTP_200


def test_star_invalid_code(client):
    '''Test for 400 response from API for bad code'''
    resp = client.simulate_get(
        '/ct/lbb6/star',
        query_string='code=shiny+thing+in+the+sky'
    )
    assert resp.status == '400 Invalid parameter'


def test_star_api_doc(client):
    '''Test API doc'''
    resp = client.simulate_get(
        '/ct/lbb6/star',
        query_string='doc=true')

    assert resp.status == falcon.HTTP_200
    assert resp.json['doc'] == Star.__doc__.replace(
        '<apiserver>', 'http://falconframework.org')
