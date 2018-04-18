'''test_api_ct_lbb2_cargogen.py'''

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
from traveller_api.ct.lbb2.cargogen import Purchase, Sale

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


@pytest.fixture
def client():
    '''API test client'''
    return testing.TestClient(api)


def test_purchase_valid_source_uwp(client):
    '''Test basic purchase'''
    resp = client.simulate_get(
        '/ct/lbb2/cargogen/purchase',
        query_string='source_uwp=B56889C-A'
    )
    LOGGER.debug('resp.json = %s', resp.json)
    assert resp.status == falcon.HTTP_200


def test_purchase_invalid_source_uwp(client):
    '''Test purchase, bogus UWP'''
    for uwp in ['Foo', None, []]:
        resp = client.simulate_get(
            '/ct/lbb2/cargogen/purchase',
            query_string='source_uwp={}'.format(uwp)
        )
        assert resp.status == '400 Invalid UWP'


def test_api_doc_purchase(client):
    '''Test API doc'''
    resp = client.simulate_get(
        '/ct/lbb2/cargogen/purchase',
        query_string='doc=true')

    assert resp.status == falcon.HTTP_200
    assert resp.json['doc'] == Purchase.__doc__.replace(
        '<apiserver>', 'http://falconframework.org')


def test_sale_valid_query_strings(client):
    '''Test sale: valid cargo (name), cargo (id), market_uwp, market_tcs'''
    for query in [
            'cargo=33',
            'cargo=Meat',
            'cargo=33&market_uwp=B56889C-A',
            'cargo=33&market_tc=In&market_tc=Ri'
        ]:
        resp = client.simulate_get(
            '/ct/lbb2/cargogen/sale',
            query_string=query
        )
        assert resp.status == falcon.HTTP_200

def test_sale_multiple_market_tcs(client):
    '''Test market TCs are captured correctly'''
    tcs_to_test = {
        'In&Ri': ['In', 'Ri'],
        'In&In': ['In']
    }
    for tcs in tcs_to_test:
        LOGGER.debug('tcs = %s', tcs)
        query = '&market_tc='.join(tcs.split('&'))
        query = 'cargo=33&market_tc={}'.format(query)
        LOGGER.debug('query = %s', query)
        resp = client.simulate_get(
            '/ct/lbb2/cargogen/sale',
            query_string=query
        )
        LOGGER.debug('resp TCs = %s', resp.json['sale']['trade_codes'])
        assert tcs_to_test[tcs] == sorted(resp.json['sale']['trade_codes'])


def test_sale_invalid_query_strings(client):
    '''Test invalid query strings'''
    pass


def test_api_doc_sale(client):
    '''Test API doc'''
    resp = client.simulate_get(
        '/ct/lbb2/cargogen/sale',
        query_string='doc=true')

    assert resp.status == falcon.HTTP_200
    assert resp.json['doc'] == Sale.__doc__.replace(
        '<apiserver>', 'http://falconframework.org')
