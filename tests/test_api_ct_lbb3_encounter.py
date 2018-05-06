'''test_api_ct_lbb3_encounter.py'''

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
from traveller_api.ct.lbb3.encounter import EncounterTable

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

@pytest.fixture
def client():
    '''API test client'''
    return testing.TestClient(api)


def test_encounter_table(client):
    '''Test valid terrain type'''
    for terrain in [
            'Clear', 'Prairie', 'Rough', 'Broken', 'Mountain', 'Forest',
            'Jungle', 'River', 'Swamp', 'Marsh', 'Desert', 'Beach',
            'Surface', 'Shallows', 'Depths', 'Bottom', 'Sea Cave', 'Sargasso',
            'Ruins', 'Cave', 'Chasm', 'Crater'
        ]:
        resp = client.simulate_get(
            '/ct/lbb3/encounter',
            query_string='terrain={}'.format(terrain)
        )
        assert resp.json['terrain'] == terrain
        assert len(resp.json['rows']) == 11
        LOGGER.debug('resp.json = %s', resp.json['rows'])
        for row in resp.json['rows']:
            LOGGER.debug('row = %s', row)
            for field in [
                    'terrain', 'quantity', 'weight', 'hits', 'wounds',
                    'armor', 'behaviour'
                ]:
                assert field in row[1]

def test_create_uwp(client):
    '''Test create with UWP supplied'''
    uwp = 'A433543-9'
    for terrain in [
            'Clear', 'Prairie', 'Rough', 'Broken', 'Mountain', 'Forest',
            'Jungle', 'River', 'Swamp', 'Marsh', 'Desert', 'Beach',
            'Surface', 'Shallows', 'Depths', 'Bottom', 'Sea Cave', 'Sargasso',
            'Ruins', 'Cave', 'Chasm', 'Crater'
        ]:
        resp = client.simulate_get(
            '/ct/lbb3/encounter',
            query_string='terrain={}&uwp={}'.format(terrain, uwp)
        )
        LOGGER.debug('resp.json = %s', resp.json)
        assert resp.json['terrain'] == terrain
        assert resp.json['uwp'] == uwp
        assert len(resp.json['rows']) == 11


def test_create_1d(client):
    '''Test create, 1D table'''
    for uwp in [None, 'A433565-6']:
        for terrain in [
                'Clear', 'Prairie', 'Rough', 'Broken', 'Mountain', 'Forest',
                'Jungle', 'River', 'Swamp', 'Marsh', 'Desert', 'Beach',
                'Surface', 'Shallows', 'Depths', 'Bottom', 'Sea Cave', 'Sargasso',
                'Ruins', 'Cave', 'Chasm', 'Crater'
            ]:
            if uwp is None:
                query_string = 'terrain={}&size=1'.format(terrain)
            else:
                query_string = 'terrain={}&uwp={}&size=1'.format(terrain, uwp)
            resp = client.simulate_get(
                '/ct/lbb3/encounter',
                query_string=query_string
            )
            LOGGER.debug('resp.json = %s', resp.json)
            assert resp.json['terrain'] == terrain
            assert resp.json['uwp'] == uwp
            assert len(resp.json['rows']) == 6


def test_list_terrains(client):
    '''Test list_terrains'''

    expected = [
        'Clear', 'Prairie', 'Rough', 'Broken', 'Mountain', 'Forest',
        'Jungle', 'River', 'Swamp', 'Marsh', 'Desert', 'Beach',
        'Surface', 'Shallows', 'Depths', 'Bottom', 'Sea Cave', 'Sargasso',
        'Ruins', 'Cave', 'Chasm', 'Crater'
    ]

    resp = client.simulate_get(
        '/ct/lbb3/encounter',
        query_string='list_terrains=true'
    )
    LOGGER.debug('received = %s', resp.json)
    assert resp.json == expected

def test_api_doc(client):
    '''Test API doc'''
    resp = client.simulate_get(
        '/ct/lbb3/encounter',
        query_string='doc=true')

    assert resp.status == falcon.HTTP_200
    assert resp.json['doc'] == EncounterTable.__doc__.replace(
        '<apiserver>', 'http://falconframework.org')
