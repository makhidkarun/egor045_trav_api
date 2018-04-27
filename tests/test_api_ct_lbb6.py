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


def test_orbit_valid_orbit_no(client):
    '''Test valid orbit_no for Orbit()'''
    # No star
    resp = client.simulate_get(
        '/ct/lbb6/orbit',
        query_string='orbit_no=4'
    )
    expected = {
        "angular_diameter": None,
        "au": 1.6,
        "mkm": 239.3,
        "notes": [],
        "orbit_no": 4,
        "period": None,
        "star": None
    }
    assert resp.json == expected
    assert resp.status == falcon.HTTP_200

    # Star = F7 V
    resp = client.simulate_get(
        '/ct/lbb6/orbit',
        query_string='orbit_no=4&star=F7V'
    )
    expected = {
        "angular_diameter": 0.416,
        "au": 1.6,
        "mkm": 239.3,
        "notes": [],
        "orbit_no": 4,
        "period": 1.848,
        "star": "F7 V"
    }
    assert resp.json == expected
    assert resp.status == falcon.HTTP_200


def test_orbit_invalid_params(client):
    '''Test orbit with invalid params'''
    for query in [
            'orbit_no=whoosh',
            'orbit_no=whoosh&star=F7V',
            'orbit_no=whoosh&star=big+shiny+thing',
            'orbit_no=4&star=big+shiny+thing'
        ]:
        resp = client.simulate_get(
            '/ct/lbb6/orbit',
            query_string=query
        )
        assert resp.status == '400 Invalid parameter'


def test_orbit_api_doc(client):
    '''Test API doc'''
    resp = client.simulate_get(
        '/ct/lbb6/orbit',
        query_string='doc=true')

    assert resp.status == falcon.HTTP_200
    assert resp.json['doc'] == Orbit.__doc__.replace(
        '<apiserver>', 'http://falconframework.org')


def test_planet_valid_params(client):
    '''Test planet API call with valid params'''
    # name, mainworld, orbit, star
    for test in [
            {
                'query_string': 'uwp=B432654-A&is_mainworld=false',
                'expected': {
                    'is_mainworld': False,
                    'name': None,
                    'orbit': None,
                    'orbital_period': None,
                    'star': None,
                    'temperature': {'max': None, 'min': None},
                    'temperature_factors': {
                        'albedo': {'max': 0.287, 'min': 0.247},
                        'cloudiness': 0.1,
                        'greenhouse': {'max': 1.0, 'min': 1.0}
                    },
                    'trade_codes': ['Na', 'Ni', 'Po'],
                    'uwp': 'B432654-A'
                }
            },

            {
                'query_string': 'uwp=B432654-A',
                'expected': {
                    'is_mainworld': True,
                    'name': None,
                    'orbit': None,
                    'orbital_period': None,
                    'star': None,
                    'temperature': {'max': None, 'min': None},
                    'temperature_factors': {
                        'albedo': {'max': 0.287, 'min': 0.247},
                        'cloudiness': 0.1,
                        'greenhouse': {'max': 1.0, 'min': 1.0}
                    },
                    'trade_codes': ['Na', 'Ni', 'Po'],
                    'uwp': 'B432654-A'
                }
            },
            {
                'query_string': 'uwp=B432654-A&name=Barsoom',
                'expected': {
                    'is_mainworld': True,
                    'name': 'Barsoom',
                    'orbit': None,
                    'orbital_period': None,
                    'star': None,
                    'temperature': {'max': None, 'min': None},
                    'temperature_factors': {
                        'albedo': {'max': 0.287, 'min': 0.247},
                        'cloudiness': 0.1,
                        'greenhouse': {'max': 1.0, 'min': 1.0}
                    },
                    'trade_codes': ['Na', 'Ni', 'Po'],
                    'uwp': 'B432654-A'
                }
            },
            {
                'query_string': 'uwp=B432654-A&name=Barsoom&orbit_no=2',
                'expected': {
                    'is_mainworld': True,
                    'name': 'Barsoom',
                    'orbit': 'Orbit 2: 0.7 AU, 104.7 Mkm',
                    'orbital_period': None,
                    'star': None,
                    'temperature': {'max': None, 'min': None},
                    'temperature_factors': {
                        'albedo': {'max': 0.287, 'min': 0.247},
                        'cloudiness': 0.1,
                        'greenhouse': {'max': 1.0, 'min': 1.0}
                    },
                    'trade_codes': ['Na', 'Ni', 'Po'],
                    'uwp': 'B432654-A'}
            },
            {
                'query_string': 'uwp=B432654-A&name=Barsoom&orbit_no=2&star=K3V',
                'expected': {
                    'is_mainworld': True,
                    'name': 'Barsoom',
                    'orbit': 'Orbit 2: 0.7 AU, 104.7 Mkm',
                    'orbital_period': 0.716,
                    'star': 'K3 V',
                    'temperature': {'max': 209.0, 'min': 197.0},
                    'temperature_factors': {
                        'albedo': {'max': 0.353, 'min': 0.313},
                        'cloudiness': 0.1,
                        'greenhouse': {'max': 1.0, 'min': 1.0}
                    },
                    'trade_codes': ['Na', 'Ni', 'Po'],
                    'uwp': 'B432654-A'
                }
            },
        ]:
        resp = client.simulate_get(
            '/ct/lbb6/planet',
            query_string=test['query_string']
        )
        LOGGER.debug('expected  = %s', test['expected'])
        LOGGER.debug('resp.json = %s', resp.json)
        assert resp.json == test['expected']
        assert resp.status == falcon.HTTP_200


def test_planet_api_doc(client):
    '''Test API doc'''
    resp = client.simulate_get(
        '/ct/lbb6/planet',
        query_string='doc=true')

    assert resp.status == falcon.HTTP_200
    assert resp.json['doc'] == Planet.__doc__.replace(
        '<apiserver>', 'http://falconframework.org')
