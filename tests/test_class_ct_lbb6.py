'''CT LBB6 unit tests'''

# pragma pylint: disable=C0413, W0613, W0212

import json
import logging
import os
import sys
import unittest
import requests
from mock import patch
from ehex import ehex
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.ct.lbb6.star import Star
from traveller_api.ct.lbb6.orbit import Orbit
from traveller_api.ct.lbb6.planet import EhexSize, LBB6Planet

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

def mock_requests_get_error(req_string):
    '''Mock unable to connect'''
    del req_string
    raise requests.ConnectionError


def mock_d6_roll_1(dice=1, modifier=0, floor=0, ceiling=9999):
    '''Mock D6.roll() - return 3 * dice + modifier'''
    result = 1 * dice + modifier
    result = max(floor, result)
    result = min(ceiling, result)
    LOGGER.debug('returning %s', result)
    return result


class TestStar(unittest.TestCase):
    '''Star() unit tests'''

    def test_create_valid(self):
        '''Test object create (valid star types)'''
        tests = {
            'G2 V': 'G2 V',
            'K5VI': 'K5 VI',
            'MD': 'M D'
        }
        for clas in tests:
            star = Star(clas)
            LOGGER.debug('classification = %s', star.classification)
            self.assertTrue(star.classification == tests[clas])

    def test_create_size_rewrite(self):
        '''
        Test create objects that can't exist - size changes
        - K5-M9 IV
        - B0-F4 VI
        '''
        # IVs
        for decimal in range(5, 10):
            code = 'K{} IV'.format(decimal)
            star = Star(code)
            self.assertTrue(star.size == 'V')
        for decimal in range(0, 10):
            code = 'M{} IV'.format(decimal)
            star = Star(code)
            self.assertTrue(star.size == 'V')

        # VIs
        for decimal in range(0, 10):
            code = 'B{} VI'.format(decimal)
            star = Star(code)
            self.assertTrue(star.size == 'V')
        for decimal in range(0, 5):
            code = 'F{} VI'.format(decimal)
            star = Star(code)
            self.assertTrue(star.size == 'V')

    def test_create_bogus(self):
        '''Test object create (bogus star types)'''
        with self.assertRaises(TypeError):
            _ = Star('foo')

    def test_json(self):
        '''Test JSON representation'''
        expected = json.dumps({
            "type": "G",
            "decimal": 2,
            "size": "V",
            "min_orbit": 0,
            "hz_orbit": 3,
            "hz_period": 1.0,
            "magnitude": 4.82,
            "luminosity": 0.994,
            "temperature": 5800,
            "radius": 0.98,
            "mass": 1.0,
            "int_orbit": None,
            "classification": "G2 V"
        }, sort_keys=True)
        code = 'G2 V'
        star = Star(code)
        LOGGER.debug('json = %s', star.json())
        self.assertTrue(expected == star.json())

    def test_str(self):
        '''Test str() representation'''
        for code in ['G2 V', 'M D']:
            star = Star(code)
            self.assertTrue(str(star) == code)


class TestOrbit(unittest.TestCase):
    '''Star test cases'''

    def test_creates(self):
        '''Test making orbit, valid and invalid values'''
        for orbit_no in [0, 19]:
            orbit = Orbit(orbit_no)
            self.assertTrue(orbit_no == orbit.orbit_no)
            self.assertTrue(orbit.period is None)
        orbit = Orbit(3, Star('G2 V'))
        self.assertTrue(orbit.orbit_no == 3)
        self.assertTrue(str(orbit.star) == 'G2 V')
        self.assertTrue(orbit.period == 1.0)

        # Bogus creates
        for orbit_no in ['foo', -1, 25]:
            with self.assertRaises(ValueError):
                _ = Orbit(orbit_no)

    def test_period_calc(self):
        '''Test period calculation'''
        orbit = Orbit(3, Star('G2 V'))
        self.assertTrue(orbit.period == 1.0)
        orbit = Orbit(2)
        self.assertTrue(orbit.period is None)

    @patch('requests.get', side_effect=mock_requests_get_error)
    def test_angdia(self, mock_fn):
        '''Test angdia response if API server is down'''
        orbit = Orbit(3, Star('G2 V'))
        self.assertTrue(
            'Unable to connect to API endpoint http://api.trav.phraction.org' in orbit.notes
        )

    def test_unavailable_orbits(self):
        '''Test for interior orbit, mnimum orbit'''
        # Interior orbit
        orbit = Orbit(2, Star('M9 Ia'))
        LOGGER.debug('notes = %s', orbit.notes)
        self.assertTrue(
            'Orbit 2 is within M9 Ia star; minimum orbit is 8' in \
            orbit.notes
        )
        # Minimum orbit
        orbit = Orbit(2, Star('B5 V'))
        LOGGER.debug('notes = %s', orbit.notes)
        self.assertTrue(
            'Orbit 2 is unavailable to B5 V star; minimum orbit is 3' in \
            orbit.notes
        )

    def test_str(self):
        '''Test str() representation'''
        orbit = Orbit(3)
        LOGGER.debug('str(orbit) = %s', str(orbit))
        self.assertTrue(str(orbit) == 'Orbit 3: 1.0 AU, 149.6 Mkm')

    def test_json(self):
        '''Test JSON representation'''
        # Test with star specfied
        expected = json.dumps({
            "angular_diameter": 0.522,
            "au": 1,
            "mkm": 149.6,
            "notes": [],
            "orbit_no": 3,
            "period": 1.0,
            "star": "G2 V"
        }, sort_keys=True)
        orbit = Orbit(3, Star('G2 V'))
        LOGGER.debug('orbit.json() = %s', orbit.json())
        self.assertTrue(orbit.json() == expected)

        # Test, no star
        expected = json.dumps({
            "angular_diameter": None,
            "au": 1,
            "mkm": 149.6,
            "notes": [],
            "orbit_no": 3,
            "period": None,
            "star": None
        }, sort_keys=True)
        orbit = Orbit(3)
        LOGGER.debug('orbit.json() = %s', orbit.json())
        self.assertTrue(orbit.json() == expected)

class TestEhexSize(unittest.TestCase):
    '''ehex extended for size S unit tests'''

    def test_s(self):
        '''Tests for ehex S'''
        size = EhexSize('S')
        self.assertTrue(int(size) == 0)
        self.assertTrue(str(size) == 'S')

        # Comparison
        for other in ['S', '0', 0, ehex(0), EhexSize(0)]:
            LOGGER.debug('size = %s other = %s', size, other)
            self.assertTrue(size == other)
            self.assertTrue(size >= other)
            self.assertTrue(size <= other)
        for other in ['1', 1, ehex(1), EhexSize(1)]:
            self.assertTrue(size < other)
            self.assertTrue(size != other)
            self.assertTrue(size <= other)
        size = EhexSize('2')
        for other in ['1', 1, ehex(1), EhexSize(1)]:
            self.assertTrue(size >= other)
            self.assertTrue(size > other)

    def test_comparison_exception(self):
        '''Test comparison exceptions'''
        other = 1.0
        size = EhexSize('2')
        with self.assertRaises(TypeError):
            _ = size == other
            _ = size != other
            _ = size <= other
            _ = size >= other
            _ = size < other
            _ = size > other

    def test_repr(self):
        '''Test __repr__()'''
        size = EhexSize('S')
        size.is_s = True
        self.assertTrue(repr(size) == 'S')
        size = EhexSize('3')
        self.assertTrue(repr(size) == '3')


class TestLBB6Planet(unittest.TestCase):
    '''LBB6 planet tests'''

    def test_create(self):
        '''Basic create tests'''
        planet = LBB6Planet()
        planet.generate()
        self.assertTrue(isinstance(planet, LBB6Planet))
        self.assertTrue(planet.starport in 'ABCDEX')

        # Not mainworld
        planet = LBB6Planet()
        planet.generate(is_mainworld=False)
        self.assertTrue(planet.starport in 'FGHY')

    @patch('traveller_api.ct.util.Die.roll', side_effect=mock_d6_roll_1)
    def test_create_roll1s(self, mock_fn):
        '''Create tests, roll 1 every time'''
        planet = LBB6Planet()
        # Size 0, not mainworld => size = S
        planet.generate(is_mainworld=False)
        LOGGER.debug('planet = %s', str(planet))
        self.assertTrue(planet.size == 'S')
        # Size 0, mainworld => size = 0
        planet.generate(is_mainworld=True)
        self.assertTrue(planet.size == '0')

    def test_wa(self):
        '''Test Wa trade code'''
        planet = LBB6Planet()
        planet.hydrographics = ehex('A')
        planet._determine_env_trade_codes()
        self.assertTrue('Wa' in planet.trade_codes)

    def test_not_wa(self):
        '''Test !Wa trade code'''
        planet = LBB6Planet()
        for hyd in '0123456789':
            planet.hydrographics = ehex(hyd)
            planet._determine_env_trade_codes()
            LOGGER.debug('planet = %s', str(planet))
            self.assertFalse('Wa' in planet.trade_codes)

    def test_de(self):
        '''Test De trade code'''
        planet = LBB6Planet()
        planet.hydrographics = ehex(0)
        for atm in '23456789ABC':
            planet.atmosphere = ehex(atm)
            planet._determine_env_trade_codes()
            LOGGER.debug('planet = %s', str(planet))
            self.assertTrue('De' in planet.trade_codes)

    def test_not_de(self):
        '''Test !De trade code'''
        planet = LBB6Planet()
        for hyd in '123456789A':
            for atm in '3456789ABC':
                planet.hydrographics = ehex(hyd)
                planet.atmosphere = ehex(atm)
                planet._determine_env_trade_codes()
                LOGGER.debug('planet = %s', str(planet))
                self.assertFalse('De' in planet.trade_codes)

    def test_va(self):
        '''Test Va trade code'''
        planet = LBB6Planet()
        planet.atmosphere = ehex(0)
        planet._determine_env_trade_codes()
        LOGGER.debug('planet = %s', str(planet))
        self.assertTrue('Va' in planet.trade_codes)

    def test_not_va(self):
        '''Test !Va trade code'''
        planet = LBB6Planet()
        for atm in '123456789ABC':
            planet.atmosphere = ehex(atm)
            planet._determine_env_trade_codes()
            LOGGER.debug('planet = %s', str(planet))
            self.assertFalse('Va' in planet.trade_codes)

    def test_as(self):
        '''Test As trade code'''
        planet = LBB6Planet()
        planet.is_mainworld = True
        planet.atmosphere = ehex(0)
        planet._determine_env_trade_codes()
        LOGGER.debug('planet = %s', str(planet))
        self.assertTrue('As' in planet.trade_codes)

    def test_not_as(self):
        '''Test !As trade code'''
        planet = LBB6Planet()
        planet.is_mainworld = False
        for atm in '0123456789ABC':
            planet.atmosphere = ehex(atm)
            planet._determine_env_trade_codes()
            LOGGER.debug('planet = %s', str(planet))
            self.assertFalse('As' in planet.trade_codes)

    def test_ic(self):
        '''Test Ic trade code'''
        planet = LBB6Planet()
        for atm in '01':
            for hyd in '123456789A':
                planet.atmosphere = ehex(atm)
                planet.hydrographics = ehex(hyd)
                planet._determine_env_trade_codes()
                LOGGER.debug('planet = %s', str(planet))
                self.assertTrue('Ic' in planet.trade_codes)

    def test_not_ic(self):
        '''Test !Ic trade code'''
        planet = LBB6Planet()
        for atm in '23456789ABC':
            for hyd in '0123456789A':
                planet.atmosphere = ehex(atm)
                planet.hydrographics = ehex(hyd)
                planet._determine_env_trade_codes()
                LOGGER.debug('planet = %s', str(planet))
                self.assertFalse('Ic' in planet.trade_codes)

    def test_load_uwp(self):
        '''Test create with UWP'''
        planet = LBB6Planet(uwp='B433432-A')
        self.assertTrue(str(planet) == 'B433432-A')

        planet = LBB6Planet(uwp='YS00000-0')
        self.assertTrue(str(planet) == 'YS00000-0')

    @patch('traveller_api.ct.util.Die.roll', side_effect=mock_d6_roll_1)
    def test_json(self, mock_fn):
        '''Test JSON representation'''
        # No orbit or star
        expected = json.dumps({
            "is_mainworld": True,
            "name": "",
            "orbit": None,
            "star": None,
            "trade_codes": ["Ni", "Po"],
            "uwp": "B433432-A"
        }, sort_keys=True)
        planet = LBB6Planet(uwp='B433432-A')
        LOGGER.debug('planet.json() = %s', planet.json())
        self.assertTrue(planet.json() == expected)

        # Orbit, star
        expected = json.dumps({
            "is_mainworld": True,
            "name": "",
            "orbit": "Orbit 3: 1.0 AU, 149.6 Mkm",
            "star": "G2 V",
            "trade_codes": ["Ni", "Po"],
            "uwp": "B433432-A"
        }, sort_keys=True)
        planet = LBB6Planet(uwp='B433432-A')
        planet.generate(star=Star('G2 V'), orbit=Orbit(3))
        LOGGER.debug('planet.json() = %s', planet.json())
        self.assertTrue(planet.json() == expected)

    def test_non_hz_orbits(self):
        '''Test non-HZ orbits (hydrographics)'''
        star = Star('G2 V')
        planet = LBB6Planet()
        planet.generate(star=star, orbit=Orbit(1))
        self.assertTrue(int(planet.hydrographics) == 0)
        planet = LBB6Planet()
        planet.generate(star=star, orbit=Orbit(11))
        self.assertTrue(str(planet.atmosphere) in '0A')
