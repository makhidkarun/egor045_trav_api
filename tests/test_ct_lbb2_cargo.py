'''test_ct_lbb2_cargo.py'''

import unittest
import sys
import os
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.ct.lbb2.cargogen.cargo import Cargo, CargoSale


class TestCargoBasic(unittest.TestCase):
    '''Cargo unit tests'''

    def test_cargo_create(self):
        '''Create cargo tests'''
        cargo = Cargo([])
        self.assertTrue(cargo.name != '')
        self.assertTrue(cargo.quantity != 0)
        self.assertTrue(
            cargo.actual_lot_price ==
            cargo.actual_unit_price * cargo.quantity)


class TestCargoSaleBasic(unittest.TestCase):
    '''CargoSale unit tests'''

    def test_cargosale_basic(self):
        '''Create CargoSale tests'''
        # Test with valid cargo params
        cargo = CargoSale('Wood')
        del cargo
        with self.assertRaises(TypeError):
            cargo = CargoSale()
            del cargo
        with self.assertRaises(ValueError):
            cargo = CargoSale(None)
            del cargo
        cargo = CargoSale('22')
        self.assertTrue(cargo.name == 'Copper')
        with self.assertRaises(ValueError):
            cargo = CargoSale('Foo')
            del cargo
        with self.assertRaises(ValueError):
            cargo = CargoSale(77)
            del cargo

    def test_cargosale_calculations(self):
        cargo = CargoSale('Copper', quantity=10, broker=1)
        self.assertTrue(
            cargo.actual_gross_lot_price ==
            cargo.quantity * cargo.actual_gross_unit_price)
        self.assertTrue(
            cargo.commission == 0.05 * cargo.quantity * cargo.base_price)
