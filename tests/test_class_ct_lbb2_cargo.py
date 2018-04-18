'''test_ct_lbb2_cargo.py'''

# pylint: disable=E0402, C0413

import json
import logging
import unittest
import sys
import os
from mock import patch
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.ct.lbb2.cargogen.cargo import Cargo

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def mock_d6_roll(dice=1, modifier=0, floor=0, ceiling=9999):
    '''Mock D6 roller - return dice * 3 + modifier'''
    result = 3 * dice + modifier
    result = max(floor, result)
    result = min(ceiling, result)
    LOGGER.debug('Mock D6.roll returning %s', result)
    return result


class TestCargoBasic(unittest.TestCase):
    '''Cargo unit tests'''

    @patch(
        'traveller_api.ct.util.Die.roll',
        side_effect=mock_d6_roll
    )
    def test_cargo_create(self, roll_fn):
        '''Create cargo tests'''
        expected = {
            "base_price": 1500, "id": "33", "name": "Meat",
            "purchase": {
                "actual_lot_price": 80940,
                "actual_unit_price": 1349,
                "notes": {"actual_value_dm": 0, "actual_value_roll": 6},
                "trade_codes": []
            },
            "purchase_dms": {"Ag": -2, "In": 3, "Na": 2},
            "quantity": 60,
            "resale_dms": {"Ag": -2, "In": 2, "Po": 1},
            "sale": {
                "actual_gross_lot_price": None,
                "actual_gross_unit_price": None,
                "actual_net_lot_price": None,
                "actual_net_unit_price": None,
                "admin": None,
                "bribery": None,
                "broker": None,
                "commission": None,
                "notes": {"actual_value_dm": None, "actual_value_roll": None},
                "trade_codes": []
            },
            "units": "tons"
        }

        cargo = Cargo()
        cargo.purchase([])
        result = json.loads(cargo.json())
        LOGGER.debug('result = %s', result)
        LOGGER.debug('result is %s', type(result))
        self.assertTrue(result == expected)


class TestCargoSaleBasic(unittest.TestCase):
    '''CargoSale unit tests'''

    def test_cargosale_basic(self):
        '''Create CargoSale tests'''
        # Test with valid cargo params
        cargo = Cargo()
        cargo.sale('Wood')
        del cargo
        with self.assertRaises(TypeError):
            cargo = Cargo()
            # pylint: disable=E1120
            cargo.sale()
            del cargo
            # pylint: enable=E1120
        with self.assertRaises(ValueError):
            cargo = Cargo()
            cargo.sale(None)
            del cargo
        cargo = Cargo()
        cargo.sale('22')
        self.assertTrue(cargo.name == 'Copper')
        with self.assertRaises(ValueError):
            cargo = Cargo()
            cargo.sale('Foo')
            del cargo
        with self.assertRaises(ValueError):
            cargo = Cargo()
            cargo.sale(77)
            del cargo

    def test_cargosale_calculations(self):
        '''Test cargo sale calculations'''
        cargo = Cargo()
        cargo.sale('Copper', quantity=10, broker=1)
        self.assertTrue(
            cargo.sale_actual_gross_lot_price ==
            cargo.quantity * cargo.sale_actual_gross_unit_price)
        self.assertTrue(
            cargo.commission == 0.05 * cargo.quantity * cargo.base_price)
