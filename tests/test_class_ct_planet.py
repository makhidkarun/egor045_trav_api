'''test_class_ct_planet.py'''

# pragma pylint: disable=C0413, W0613, W0212

import logging
import os
import sys
import unittest
from ehex import ehex
from mock import patch
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.ct.planet import Planet

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def mock_d6_roll(dice=1, modifier=0, floor=0, ceiling=9999):
    '''Mock D6.roll() - return 3 * dice + modifier'''
    result = 3 * dice + modifier
    result = max(floor, result)
    result = min(ceiling, result)
    LOGGER.debug('returnng %s', result)
    return result


class TestPlanet(unittest.TestCase):
    '''Planet unit tests'''

    @patch('traveller_api.ct.util.Die.roll', side_effect=mock_d6_roll)
    def test_basic_create(self, mock_fn):
        '''Test basic planet create'''
        planet = Planet('Mongo')
        planet.generate()
        LOGGER.debug('planet = %s', str(planet))
        self.assertTrue(planet.name == 'Mongo')
        self.assertTrue(planet.starport == 'B')
        self.assertTrue(str(planet.size) == '4')
        self.assertTrue(str(planet.atmosphere) == '3')
        self.assertTrue(str(planet.hydrographics) == '3')
        self.assertTrue(str(planet.population) == '4')
        self.assertTrue(str(planet.government) == '3')
        self.assertTrue(str(planet.lawlevel) == '2')
        self.assertTrue(str(planet.techlevel) == 'A')

    def test_load_uwp(self):
        '''Test create with provided UWP'''
        planet = Planet(uwp='B433432-A')
        LOGGER.debug('planet = %s', str(planet))
        self.assertTrue(planet.starport == 'B')
        self.assertTrue(str(planet.size) == '4')
        self.assertTrue(str(planet.atmosphere) == '3')
        self.assertTrue(str(planet.hydrographics) == '3')
        self.assertTrue(str(planet.population) == '4')
        self.assertTrue(str(planet.government) == '3')
        self.assertTrue(str(planet.lawlevel) == '2')
        self.assertTrue(str(planet.techlevel) == 'A')

    @patch('traveller_api.ct.util.Die.roll', side_effect=mock_d6_roll)
    def test_str(self, mock_fn):
        '''Test str() method'''
        expected = 'B433432-A'
        planet = Planet()
        planet.generate()
        self.assertTrue(str(planet) == expected)

    @patch('traveller_api.ct.util.Die.roll', side_effect=mock_d6_roll)
    def test_json(self, mock_fn):
        '''Test json() method'''
        expected = '{"name": "", "trade_codes": ["Ni", "Po"], "uwp": "B433432-A"}'
        planet = Planet()
        planet.generate()
        LOGGER.debug('expected      = %s', expected)
        LOGGER.debug('planet.json() = %s', planet.json())
        self.assertTrue(planet.json() == expected)


class TestPlanetTradeCodes(unittest.TestCase):
    '''Test trade classifications'''

    def test_ag(self):
        '''Test Ag'''
        planet = Planet()
        for atm in '456789':
            for hyd in '45678':
                for pop in '567':
                    planet.atmosphere = ehex(atm)
                    planet.hydrographics = ehex(hyd)
                    planet.population = ehex(pop)
                    planet._determine_trade_codes()

                    self.assertTrue('Ag' in planet.trade_codes)

    def test_not_ag(self):
        '''Test !Ag'''
        planet = Planet()
        for atm in '0123ABC':
            for hyd in '01239A':
                for pop in '0123489A':
                    planet.atmosphere = ehex(atm)
                    planet.hydrographics = ehex(hyd)
                    planet.population = ehex(pop)
                    planet._determine_trade_codes()

                    self.assertFalse('Ag' in planet.trade_codes)

    def test_na(self):
        '''Test Na'''
        planet = Planet()
        for atm in '0123':
            for hyd in '0123':
                for pop in '6789':
                    planet.atmosphere = ehex(atm)
                    planet.hydrographics = ehex(hyd)
                    planet.population = ehex(pop)
                    planet._determine_trade_codes()

                    self.assertTrue('Na' in planet.trade_codes)

    def test_not_na(self):
        '''Test !Na'''
        planet = Planet()
        for atm in '456789ABC':
            for hyd in '456789A':
                for pop in '012345':
                    planet.atmosphere = ehex(atm)
                    planet.hydrographics = ehex(hyd)
                    planet.population = ehex(pop)
                    planet._determine_trade_codes()

                    self.assertFalse('Na' in planet.trade_codes)

    def test_in(self):
        '''Test In'''
        planet = Planet()
        for atm in '012479':
            for pop in '9A':
                planet.atmosphere = ehex(atm)
                planet.population = ehex(pop)
                planet._determine_trade_codes()

                self.assertTrue('In' in planet.trade_codes)

    def test_not_in(self):
        '''Test !In'''
        planet = Planet()
        for atm in '3568ABC':
            for pop in '012345678':
                planet.atmosphere = ehex(atm)
                planet.population = ehex(pop)
                planet._determine_trade_codes()

                self.assertFalse('In' in planet.trade_codes)

    def test_ni(self):
        '''Test Ni'''
        planet = Planet()
        for pop in '0123456':
            planet.population = ehex(pop)
            planet._determine_trade_codes()

            self.assertTrue('Ni' in planet.trade_codes)

    def test_not_ni(self):
        '''Test !Ni'''
        planet = Planet()
        for pop in '789A':
            planet.population = ehex(pop)
            planet._determine_trade_codes()

            self.assertFalse('Ni' in planet.trade_codes)


    def test_ri(self):
        '''Test Ri'''
        planet = Planet()
        for gov in '456789':
            for atm in '68':
                for pop in '678':
                    planet.government = ehex(gov)
                    planet.atmosphere = ehex(atm)
                    planet.population = ehex(pop)
                    planet._determine_trade_codes()

                    self.assertTrue('Ri' in planet.trade_codes)

    def test_not_ri(self):
        '''Test !Ri'''
        planet = Planet()
        for gov in '0123ABC':
            for atm in '01234579ABC':
                for pop in '0123459A':
                    planet.government = ehex(gov)
                    planet.atmosphere = ehex(atm)
                    planet.population = ehex(pop)
                    planet._determine_trade_codes()

                    self.assertFalse('Ri' in planet.trade_codes)

    def test_po(self):
        '''Test Po'''
        planet = Planet()
        for atm in '2345':
            for hyd in '0123':
                planet.atmosphere = ehex(atm)
                planet.hydrographics = ehex(hyd)
                planet._determine_trade_codes()

                self.assertTrue('Po' in planet.trade_codes)

    def test_not_po(self):
        '''Test !Po'''
        planet = Planet()
        for atm in '016789ABC':
            for hyd in '456789A':
                planet.atmosphere = ehex(atm)
                planet.hydrographics = ehex(hyd)
                planet._determine_trade_codes()

                self.assertFalse('Po' in planet.trade_codes)
