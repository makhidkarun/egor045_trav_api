'''cargo.py'''

import re
import json
import logging
from ehex import ehex
from ...util import Die


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)

RE_QUANTITY = re.compile('^([0-9]+)D')
RE_QUANTITY_X = re.compile('^([0-9]+)Dx([0-9]+)')
RE_ID = re.compile('^[1-6][1-6]$')

D6 = Die(6)


class Cargo(object):
    '''Base cargo object'''

    def __init__(self, trade_codes, population=6):
        self._populate_trade_goods()
        self.name = ''
        self.id = 0
        self.base_price = 0
        self.purchase_dms = {}
        self.resale_dms = {}
        self.quantity = 0
        self.actual_unit_price = 0
        self.actual_lot_price = 0
        self.trade_codes = trade_codes
        self.units = ''

        self.select_cargo(population)
        self.determine_actual_unit_price()
        self.actual_lot_price = self.actual_unit_price * self.quantity
        self.set_units()

    def _populate_trade_goods(self):
        '''Populate _trade_goods dict'''
        self._trade_goods = {
            '11': {
                'name': 'Textiles',
                'base_price': 3000,
                'purchase_dms': {'Ag': -7, 'Na': -5, 'Ni': -3},
                'resale_dms': {'Ag': -6, 'Na': +1, 'Ri': +3},
                'quantity': '3Dx5'},
            '12': {
                'name': 'Polymers',
                'base_price': 7000,
                'purchase_dms': {'In': -2, 'Ri': -3, 'Po': +2},
                'resale_dms': {'In': -2, 'Ri': +3},
                'quantity': '4Dx5'},
            '13': {
                'name': 'Liquor',
                'base_price': 10000,
                'purchase_dms': {'Ag': -4},
                'resale_dms': {'Ag': -3, 'In': +1, 'Ri': +2},
                'quantity': '1Dx5'},
            '14': {
                'name': 'Wood',
                'base_price': 1000,
                'purchase_dms': {'Ag': -6},
                'resale_dms': {'Ag': -6, 'In': +1, 'Ri': +2},
                'quantity': '2Dx10'},
            '15': {
                'name': 'Crystals',
                'base_price': 20000,
                'purchase_dms': {'Na': -3, 'In': +4},
                'resale_dms': {'Na': -3, 'In': +3, 'Ri': +3},
                'quantity': '1D'},
            '16': {
                'name': 'Radioactives',
                'base_price': 1000000,
                'purchase_dms': {'In': +7, 'Ni': -3, 'Ri': +5},
                'resale_dms': {'In': +6, 'Ni': -3, 'Ri': -4},
                'quantity': '1D'},
            '21': {
                'name': 'Steel',
                'base_price': 500,
                'purchase_dms': {'In': -2, 'Ri': -1, 'Po': +1},
                'resale_dms': {'In': -2, 'Ri': -1, 'Po': +3},
                'quantity': '4Dx10'},
            '22': {
                'name': 'Copper',
                'base_price': 2000,
                'purchase_dms': {'In': -3, 'Ri': -2, 'Po': +1},
                'resale_dms': {'In': -3, 'Ri': -1},
                'quantity': '2Dx10'},
            '23': {
                'name': 'Aluminum',
                'base_price': 1000,
                'purchase_dms': {'In': -3, 'Ri': -2, 'Po': +1},
                'resale_dms': {'In': -3, 'Ni': +4, 'Ri': -1},
                'quantity': '5Dx10'},
            '24': {
                'name': 'Tin',
                'base_price': 9000,
                'purchase_dms': {'In': -3, 'Ri': -2, 'Po': +1},
                'resale_dms': {'In': -3, 'Ri': -1},
                'quantity': '3Dx10'},
            '25': {
                'name': 'Silver',
                'base_price': 70000,
                'purchase_dms': {'In': +5, 'Ri': -1, 'Po': +2},
                'resale_dms': {'In': +5, 'Ri': -1},
                'quantity': '1Dx5'},
            '26': {
                'name': 'Special Alloys',
                'base_price': 200000,
                'purchase_dms': {'In': -3, 'Ni': +5, 'Ri': -2},
                'resale_dms': {'In': -3, 'Ni': +4, 'Ri': -1},
                'quantity': '1D'},
            '31': {
                'name': 'Petrochemicals',
                'base_price': 10000,
                'purchase_dms': {'Na': -4, 'In': +1, 'Ni': -5},
                'resale_dms': {'Na': -4, 'In': +3, 'Ni': -5},
                'quantity': '1D'},
            '32': {
                'name': 'Grain',
                'base_price': 300,
                'purchase_dms': {'Ag': -2, 'Na': +1, 'In': +2},
                'resale_dms': {'Ag': -2},
                'quantity': '8Dx5'},
            '33': {
                'name': 'Meat',
                'base_price': 1500,
                'purchase_dms': {'Ag': -2, 'Na': +2, 'In': +3},
                'resale_dms': {'Ag': -2, 'In': +2, 'Po': +1},
                'quantity': '4Dx5'},
            '34': {
                'name': 'Spices',
                'base_price': 6000,
                'purchase_dms': {'Ag': -2, 'Na': +3, 'In': +2},
                'resale_dms': {'Ag': -2, 'Ri': +2, 'Po': +3},
                'quantity': '1Dx5'},
            '35': {
                'name': 'Fruit',
                'base_price': 1000,
                'purchase_dms': {'Ag': -3, 'Na': +1, 'In': +2},
                'resale_dms': {'Ag': -2, 'In': +3, 'Po': +2},
                'quantity': '2Dx5'},
            '36': {
                'name': 'Pharmaceuticals',
                'base_price': 100000,
                'purchase_dms': {'Na': -3, 'In': +4, 'Po': +3},
                'resale_dms': {'Na': -3, 'In': +5, 'Ri': +4},
                'quantity': '1D'},
            '41': {
                'name': 'Gems',
                'base_price': 1000000,
                'purchase_dms': {'In': +4, 'Ni': -8, 'Po': -3},
                'resale_dms': {'In': +4, 'Ni': -2, 'Ri': +8},
                'quantity': '2D'},
            '42': {
                'name': 'Firearms',
                'base_price': 30000,
                'purchase_dms': {'In': -3, 'Ri': -2, 'Po': +3},
                'resale_dms': {'In': -2, 'Ri': -1, 'Po': +3},
                'quantity': '2D'},
            '43': {
                'name': 'Ammunition',
                'base_price': 30000,
                'purchase_dms': {'In': -3, 'Ri': -2, 'Po': +3},
                'resale_dms': {'In': -2, 'Ri': -1, 'Po': +3},
                'quantity': '2D'},
            '44': {
                'name': 'Blades',
                'base_price': 10000,
                'purchase_dms': {'In': -3, 'Ri': -2, 'Po': +3},
                'resale_dms': {'In': -2, 'Ri': -1, 'Po': +3},
                'quantity': '2D'},
            '45': {
                'name': 'Tools',
                'base_price': 10000,
                'purchase_dms': {'In': -3, 'Ri': -2, 'Po': +3},
                'resale_dms': {'In': -2, 'Ri': -1, 'Po': +3},
                'quantity': '2D'},
            '46': {
                'name': 'Body Armor',
                'base_price': 50000,
                'purchase_dms': {'In': -1, 'Ri': -3, 'Po': +3},
                'resale_dms': {'In': -2, 'Ri': +1, 'Po': +4},
                'quantity': '2D'},
            '51': {
                'name': 'Aircraft',
                'base_price': 1000000,
                'purchase_dms': {'In': -4, 'Ri': -3},
                'resale_dms': {'Ni': +2, 'Po': +1},
                'quantity': '1D'},
            '52': {
                'name': 'Air/raft',
                'base_price': 6000000,
                'purchase_dms': {'In': -3, 'Ri': -2},
                'resale_dms': {'Ni': +2, 'Po': +1},
                'quantity': '1D'},
            '53': {
                'name': 'Computers',
                'base_price': 10000000,
                'purchase_dms': {'In': -2, 'Ri': -2},
                'resale_dms': {'Ni': +2, 'Po': +1, 'Ag': -3},
                'quantity': '1D'},
            '54': {
                'name': 'All Terrain Vehicles',
                'base_price': 3000000,
                'purchase_dms': {'In': -2, 'Ri': -2},
                'resale_dms': {'Ni': +2, 'Po': +1, 'Ag': +1},
                'quantity': '1D'},
            '55': {
                'name': 'Armored Vehicles',
                'base_price': 7000000,
                'purchase_dms': {'In': -5, 'Ri': -2, 'Po': +4},
                'resale_dms': {'Na': -2, 'Ag': +2, 'Ri': +1},
                'quantity': '1D'},
            '56': {
                'name': 'Farm Machinery',
                'base_price': 150000,
                'purchase_dms': {'In': -5, 'Ri': -2},
                'resale_dms': {'Ag': +5, 'Na': -8, 'Po': +1},
                'quantity': '1D'},
            '61': {
                'name': 'Electronics Parts',
                'base_price': 100000,
                'purchase_dms': {'In': -4, 'Ri': -3},
                'resale_dms': {'Ni': +2, 'Po': +1},
                'quantity': '1Dx5'},
            '62': {
                'name': 'Mechanical Parts',
                'base_price': 70000,
                'purchase_dms': {'In': -5, 'Ri': -3},
                'resale_dms': {'Ni': +3, 'Ag': +2},
                'quantity': '1Dx5'},
            '63': {
                'name': 'Cybernetic Parts',
                'base_price': 250000,
                'purchase_dms': {'In': -4, 'Ri': -1},
                'resale_dms': {'Ni': +4, 'Ag': +1, 'Na': +2},
                'quantity': '1Dx5'},
            '64': {
                'name': 'Computer Parts',
                'base_price': 150000,
                'purchase_dms': {'In': -5, 'Ri': -3},
                'resale_dms': {'Ni': +3, 'Ag': +1, 'Na': +2},
                'quantity': '1Dx5'},
            '65': {
                'name': 'Machine Tools',
                'base_price': 750000,
                'purchase_dms': {'In': -5, 'Ri': -4},
                'resale_dms': {'Ni': +3, 'Ag': +1, 'Na': +2},
                'quantity': '1Dx5'},
            '66': {
                'name': 'Vacc Suits',
                'base_price': 400000,
                'purchase_dms': {'Na': -5, 'In': -3, 'Ri': +1},
                'resale_dms': {'Na': -1, 'Ni': +2, 'Po': +1},
                'quantity': '1Dx5'}
        }

    def select_cargo(self, population):
        '''Select cargo'''
        # population DM
        LOGGER.debug('population = %s', population)
        die_mod = 0
        if population is not None:
            population = ehex(population)
            if int(population) >= 9:
                die_mod = 1
            elif int(population) <= 5:
                die_mod = -1
        LOGGER.debug('Die 1 DM = %s', die_mod)
        cargo_id = '{}{}'.format(
            D6.roll(dice=1, modifier=die_mod, floor=1, ceiling=6),
            D6.roll())
        self.name = self._trade_goods[cargo_id]['name']
        self.id = cargo_id
        self.base_price = self._trade_goods[cargo_id]['base_price']
        self.purchase_dms = self._trade_goods[cargo_id]['purchase_dms']
        self.resale_dms = self._trade_goods[cargo_id]['resale_dms']
        self.quantity = self.determine_quantity(
            self._trade_goods[cargo_id]['quantity'])

    def set_units(self):
        '''Set units - cargo ID in range 51-56 => individual, tons otherwise'''
        if self.id[0] in '12346':
            self.units = 'tons'

    @staticmethod
    def determine_quantity(quantity_string):
        '''Determine lot size'''
        resp = 0
        if 'Dx' in quantity_string:
            match = RE_QUANTITY_X.match(quantity_string)
            if match:
                resp = int(
                    D6.roll(int(match.group(1))) * int(match.group(2)))
        else:
            match = RE_QUANTITY.match(quantity_string)
            if match:
                resp = int(D6.roll(int(match.group(1))))
        return resp

    def determine_actual_unit_price(self):
        '''Determine actual unit price'''
        # Determine DM
        die_mod = 0
        for code in self.trade_codes:
            if code in self.purchase_dms:
                die_mod += self.purchase_dms[code]

        self.actual_unit_price = int(
            self.base_price * self.determine_actual_value(die_mod))

    def json(self):
        '''Return JSON representation'''
        doc = {
            'name': self.name,
            'id': self.id,
            'base_price': self.base_price,
            'purchase_dms': self.purchase_dms,
            'resale_dms': self.resale_dms,
            'quantity': self.quantity,
            'actual_unit_price': self.actual_unit_price,
            'actual_lot_price': self.actual_lot_price,
            'trade_codes': self.trade_codes,
            'units': self.units
        }
        return json.dumps(doc)

    @staticmethod
    def determine_actual_value(die_mod):
        '''Determine actual value table'''
        result = 0.0
        roll = D6.roll(2, die_mod)
        roll = max(2, roll)
        roll = min(15, roll)
        if roll <= 3:
            result = float((roll - 2) / 10) + 0.4
        elif roll >= 4 and roll <= 10:
            result = float((roll - 4) / 10) + 0.7
        elif roll == 11:
            result = 1.5
        elif roll == 12:
            result = 1.7
        elif roll >= 13:
            result = float(roll - 11)
        return result


class CargoSale(Cargo):
    '''Sale object'''

    def __init__(
            self,
            cargo,
            admin=0, bribery=0, broker=0,
            quantity=0,
            trade_codes=[]):

        self._populate_trade_goods()
        self.actual_gross_unit_price = 0
        self.actual_gross_lot_price = 0
        self.actual_net_unit_price = 0
        self.actual_net_lot_price = 0
        self.commission = 0
        self.units = ''

        try:
            var = 'admin'
            self.admin = int(admin)
            assert self.admin >= 0
            var = 'bribery'
            self.bribery = int(bribery)
            assert self.bribery >= 0
            var = 'broker'
            self.broker = int(broker)
            assert self.broker <= 4
            assert self.broker >= 0
            var = 'quantity'
            self.quantity = int(quantity)
            assert self.quantity >= 0
            var = 'trade_codes'
            self.trade_codes = trade_codes
        except AssertionError:
            raise ValueError(var)
        except ValueError:
            raise ValueError(var)
        self.find_cargo(cargo)

        self._determine_actual_unit_price()
        self._determine_commission()
        self.set_units()

    def find_cargo(self, cargo):
        '''Find cargo (may be name or id), set ID and name'''
        if cargo is None:
            raise ValueError('cargo parameter (cargo ID/name) cannot be None')
        else:
            cargo = str(cargo)
        if RE_ID.match(cargo):
            # cargo is id. not name
            self.name = self._trade_goods[cargo]['name']
            self.id = cargo
            self.purchase_dms = self._trade_goods[cargo]['purchase_dms']
            self.resale_dms = self._trade_goods[cargo]['resale_dms']
            self.base_price = self._trade_goods[cargo]['base_price']
        else:
            # cargo should be name, raise ValueError if not'''
            is_valid = False
            for cargo_id in self._trade_goods:
                if self._trade_goods[cargo_id]['name'].lower() == \
                        cargo.lower():
                    is_valid = True
                    self.name = self._trade_goods[cargo_id]['name']
                    self.id = cargo_id
                    self.purchase_dms = \
                        self._trade_goods[cargo_id]['purchase_dms']
                    self.resale_dms = \
                        self._trade_goods[cargo_id]['resale_dms']
                    self.base_price = \
                        self._trade_goods[cargo_id]['base_price']
            if not is_valid:
                raise ValueError('cargo {} not known'.format(cargo))

    def _determine_actual_unit_price(self):
        '''Determine actual sale price'''
        die_mod = self.broker + self.admin + self.bribery
        for code in self.trade_codes:
            if code in self.resale_dms:
                die_mod += self.resale_dms[code]

        self.actual_gross_unit_price = int(
            self.base_price * self.determine_actual_value(die_mod))
        self.actual_gross_lot_price = \
            self.actual_gross_unit_price * self.quantity

    def _determine_commission(self):
        '''Determine commission, net prices'''
        LOGGER.debug(
            'base_price is %s = %s',
            type(self.base_price), self.base_price)
        LOGGER.debug(
            'broker is %s = %s',
            type(self.broker), self.broker)
        LOGGER.debug(
            'quantity is %s = %s',
            type(self.quantity), self.quantity)
        unit_commission = int(self.base_price * self.broker * 0.05)
        self.commission = unit_commission * self.quantity
        self.actual_net_unit_price = self.actual_gross_unit_price - \
            unit_commission
        self.actual_net_lot_price = self.actual_net_unit_price * \
            self.quantity

    def json(self):
        '''JSON representation'''

        doc = {
            'name': self.name,
            'id': self.id,
            'base_price': self.base_price,
            'quantity': self.quantity,
            'commission': self.commission,
            'admin': self.admin,
            'bribery': self.bribery,
            'broker': self.broker,
            'actual_gross_unit_price': self.actual_gross_unit_price,
            'actual_gross_lot_price': self.actual_gross_lot_price,
            'actual_net_unit_price': self.actual_net_unit_price,
            'actual_net_lot_price': self.actual_net_lot_price,
            'trade_codes': self.trade_codes,
            'units': self.units
        }
        return json.dumps(doc)
