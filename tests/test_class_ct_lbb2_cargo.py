'''test_ct_lbb2_cargo.py'''

# pylint: disable=E0402, C0413

import unittest
import sys
import os
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.ct.lbb2.cargogen.cargo import Cargo


class TestCargoBasic(unittest.TestCase):
    '''Cargo unit tests'''

    def test_cargo_create(self):
        '''Create cargo tests'''
        cargo = Cargo()
        cargo.purchase([])
        self.assertTrue(cargo.name != '')
        self.assertTrue(cargo.quantity != 0)
        self.assertTrue(
            cargo.purchase_actual_lot_price ==
            cargo.purchase_actual_unit_price * cargo.quantity)


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
