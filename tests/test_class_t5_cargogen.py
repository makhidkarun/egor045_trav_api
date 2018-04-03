'''test_class_t5_cargogen.py'''

import json
import logging
import os
import sys
import unittest
from mock import patch
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.t5.cargogen.trade_cargo import TradeCargo, FluxRoll

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

def mock_randint(v_1, v_2):
    '''Mock randint response'''
    LOGGER.debug('mock_randint returning %s', v_2)
    return v_2

def mock_fluxroll():
    '''Mock FluxRoll.roll() response'''
    ret = 0
    LOGGER.debug('mock_fluxroll returning %s', ret)
    return ret

class TestFluxRoll(unittest.TestCase):
    '''Test FluxRoll with mock'''
    @patch(
        'traveller_api.t5.cargogen.trade_cargo.randint',
        side_effect=mock_randint)
    def test_fluxroll(self, mock_randint):
        '''Test FluxRoll'''
        f = FluxRoll()
        self.assertTrue(f.roll() == 0)


class TestTradeCargo(unittest.TestCase):
    '''TradeCargo() tests'''
    @patch('traveller_api.t5.cargogen.trade_cargo.randint', side_effect=mock_randint)
    def test_generate_cargo(self, randint_fn):
        '''Test cargo generation'''
        # Valid UWP - Efate A646930-D Hi In cost=Cr2300
        # Valid UWP - Alell B56789C-A Ri Pa Ph cost=Cr5000
        expected = {
            'A646930-D': {'tcs': ['Hi', 'In'], 'cost': 2300},
            'B56789C-A': {'tcs': ['Ri'], 'cost': 5000}
        }
        for source_uwp in expected:
            cargo = TradeCargo()
            cargo.generate_cargo(source_uwp)
            self.assertTrue(cargo.cost == expected[source_uwp]['cost'])
            self.assertTrue(cargo.source_world.trade_codes)

    def test_generate_cargo_bogus(self):
        '''Test cargo generation with bad UWP'''
        cargo = TradeCargo()
        with self.assertRaises(ValueError):
            cargo.generate_cargo('bogus_UWP')
            cargo.generate_cargo('A646930-D', 'market UWP')

    def test_generate_source_market(self):
        '''Test cargo generation with source and market'''
        # Source world - Alell B56789C-A Ri Pa Ph cost=Cr5000
        # Market world = Uakye B439598-D Ni price=Cr4200
        source_uwp = 'B56789C-A'
        market_uwp = 'B439598-D'
        cargo = TradeCargo()
        cargo.generate_cargo(source_uwp, market_uwp)
        LOGGER.debug('cargo.price = %s', cargo.price)
        LOGGER.debug('json = %s', cargo.json())
        self.assertTrue(cargo.cost == 5000)
        self.assertTrue(cargo.price == 3500)

    @patch(
        'traveller_api.t5.cargogen.trade_cargo.FluxRoll.roll',
        side_effect=mock_fluxroll)
    def test_actual_value(self, fluxroll_fn):
        '''Test actual value'''
        # Source world - Alell B56789C-A Ri Pa Ph cost=Cr5000
        # Market world = Uakye B439598-D Ni price=Cr4200
        source_uwp = 'B56789C-A'
        market_uwp = 'B439598-D'
        cargo = TradeCargo()
        cargo.generate_cargo(source_uwp, market_uwp)
        LOGGER.debug('cargo.price = %s', cargo.price)
        LOGGER.debug('json = %s', cargo.json())
        self.assertTrue(cargo.net_actual_value == 3500)

    def test_json(self):
        '''Test JSON representation'''
        # Source world - Alell B56789C-A Ri Pa Ph cost=Cr5000
        # Market world = Uakye B439598-D Ni price=Cr4200

        source_uwp = 'B56789C-A'
        market_uwp = 'B439598-D'
        cargo = TradeCargo()
        cargo.generate_cargo(source_uwp, market_uwp)

        actual = json.loads(cargo.json())
        self.assertTrue(actual['cargo'] == str(cargo))
        self.assertTrue(actual['cost'] == cargo.cost)
        self.assertTrue(actual['description'] == cargo.description)
        self.assertTrue(
            actual['market']['gross_actual_value'] == cargo.actual_value)
        self.assertTrue(actual['price'] == cargo.price)

    def test_broker_skill(self):
        '''Test broker skill'''
        source_uwp = 'B56789C-A'
        market_uwp = 'B439598-D'
        broker = 2
        cargo = TradeCargo()
        cargo.generate_cargo(source_uwp, market_uwp, broker)
        self.assertTrue(cargo.broker_skill == broker)
        self.assertTrue(
            cargo.broker_dm == int((cargo.broker_skill + 0.5) / 2))

    def test_broker_skill_bogus(self):
        '''Test bogus broker skill'''
        source_uwp = 'B56789C-A'
        market_uwp = 'B439598-D'
        broker = 'Two'
        cargo = TradeCargo()
        with self.assertRaises(ValueError):
            cargo.generate_cargo(source_uwp, market_uwp, broker)
