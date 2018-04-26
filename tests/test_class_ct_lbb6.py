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
from traveller_api.util import MinMax

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
        with self.assertRaises(ValueError):
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
            "temperature": {"max": 0, "min": 0},
            "temperature_factors": {
                "albedo": {"max": 0.266, "min": 0.226},
                "cloudiness": 0.1,
                'greenhouse': {"max": 1.0, "min": 1.0}
            },
            "trade_codes": ["Ni", "Po"],
            "uwp": "B433432-A"
        }, sort_keys=True)
        planet = LBB6Planet(uwp='B433432-A')
        planet.generate()
        LOGGER.debug('expected      = %s', expected)
        LOGGER.debug('planet.json() = %s', planet.json())
        self.assertTrue(planet.json() == expected)

        # Orbit, star
        expected = json.dumps({
            "is_mainworld": True,
            "name": "Planet 9",
            "orbit": "Orbit 3: 1.0 AU, 149.6 Mkm",
            "star": "G2 V",
            "temperature": {"max": 289.0, "min": 274.0},
            "temperature_factors": {
                "albedo": {"max": 0.266, "min": 0.226},
                "cloudiness": 0.1,
                'greenhouse': {"max": 1.0, "min": 1.0}
            },
            "trade_codes": ["Ni", "Po"],
            "uwp": "B433432-A"
        }, sort_keys=True)
        planet = LBB6Planet('Planet 9', uwp='B433432-A')
        planet.generate(star=Star('G2 V'), orbit=Orbit(3))
        LOGGER.debug('expected      = %s', expected)
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


class TestLBB6PlanetTradeCodes(unittest.TestCase):
    '''Trade code test cases'''

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


class TestLBB6PlanetTemp(unittest.TestCase):
    '''Unit tests for albedo, cloudiness, temperature'''
    def test_albedo(self):
        '''Albedo tests'''
        star = Star('G2 V')
        tests = [
            {
                'uwp': 'A867977-8',
                'star': star,
                'orbit': Orbit(3),
                'expected': (0.265, 0.465)
            }
        ]
        for test in tests:
            planet = LBB6Planet(uwp=test['uwp'])
            planet.generate(star=test['star'], orbit=test['orbit'])
            LOGGER.debug(
                'uwp = %s TCs = %s albedo = %s',
                str(planet), planet.trade_codes, str(planet.albedo)
            )
            self.assertTrue(planet.albedo.min() == test['expected'][0])
            self.assertTrue(planet.albedo.max() == test['expected'][1])

    def test_cloudiness(self):
        '''
        Cloudiness tests
        hyd 0-1: cloudiness = 0%
        hyd 2-3: cloudiness = 10%
        hyd 4: cloudiness = 20%
        hyd 5: cloudiness = 30%
        hyd 6: cloudiness = 40%
        hyd 7: cloudiness = 50%
        hyd 8: cloudiness = 60%
        hyd 9-A: cloudiness = 70%
        atm A+: cloudiness +40%
        atm 3-: max cloudiness = 20%
        atm E: cloudiness / 2
        '''
        test_cases = [
            {'hyd': '0', 'cloudiness': 0.0},
            {'hyd': '1', 'cloudiness': 0.0},
            {'hyd': '2', 'cloudiness': 0.1},
            {'hyd': '3', 'cloudiness': 0.1},
            {'hyd': '4', 'cloudiness': 0.2},
            {'hyd': '5', 'cloudiness': 0.3},
            {'hyd': '6', 'cloudiness': 0.4},
            {'hyd': '7', 'cloudiness': 0.5},
            {'hyd': '8', 'cloudiness': 0.6},
            {'hyd': '9', 'cloudiness': 0.7},
            {'hyd': 'A', 'cloudiness': 0.7}
        ]
        planet = LBB6Planet()
        for test in test_cases:
            planet.hydrographics = ehex(test['hyd'])
            for atm in '0123456789ABCDEF':
                planet.atmosphere = ehex(atm)
                expected = test['cloudiness']
                if atm in '0123':
                    expected = min(expected, 0.2)
                if atm in 'ABCDEF':
                    expected += 0.4
                    expected = min(expected, 1.0)
                if atm == 'E':
                    expected = expected / 2.0
                expected = round(expected, 1)
                planet.determine_cloudiness()
                LOGGER.debug(
                    'hyd = %s, atm = %s, cloudiness = %s, expected = %s',
                    planet.hydrographics,
                    planet.atmosphere,
                    planet.cloudiness,
                    expected
                )
                self.assertTrue(planet.cloudiness == expected)

    def test_temperature(self):
        '''Temperature tests'''
        star = Star('G2 V')
        for test in [
                {'uwp': 'A867A69-F', 'orbit': 3, 'expected': MinMax(221.0, 303.0)},
                {'uwp': 'F20067C-F', 'orbit': 3, 'expected': MinMax(299.0, 299.0)},
                {'uwp': 'F43056A-F', 'orbit': 4, 'expected': MinMax(237.0, 237.0)},
                {'uwp': 'G8B0168-F', 'orbit': 2, 'expected': MinMax(300.0, 707.0)},
                {'uwp': 'F10046C-F', 'orbit': 9, 'expected': MinMax(48.0, 48.0)}
            ]:
            planet = LBB6Planet(uwp=test['uwp'])
            planet.generate(star=star, orbit=Orbit(test['orbit']))
            LOGGER.debug('planet = %s', planet.json())
            LOGGER.debug(
                'uwp = %s expected = %s, actual = %s',
                test['uwp'], test['expected'], planet.temperature

            )
            self.assertAlmostEqual(
                planet.temperature.min(), test['expected'].min(), delta=2
            )
            self.assertAlmostEqual(
                planet.temperature.max(), test['expected'].max(), delta=2
            )

    def test_greenhouse(self):
        '''Greenhouse tests'''
        planet = LBB6Planet()
        tests = [
            {'atm': '0', 'expected': 1.0},
            {'atm': '1', 'expected': 1.0},
            {'atm': '2', 'expected': 1.0},
            {'atm': '3', 'expected': 1.0},
            {'atm': '4', 'expected': 1.05},
            {'atm': '5', 'expected': 1.05},
            {'atm': '6', 'expected': 1.1},
            {'atm': '7', 'expected': 1.1},
            {'atm': '8', 'expected': 1.15},
            {'atm': '9', 'expected': 1.15},
            {'atm': 'A', 'expected': (1.2, 1.7)},
            {'atm': 'B', 'expected': (1.2, 2.2)},
            {'atm': 'C', 'expected': (1.2, 2.2)},
            {'atm': 'D', 'expected': 1.15},
            {'atm': 'E', 'expected': 1.1},
            {'atm': 'F', 'expected': 1.0},
        ]
        for test in tests:
            planet.atmosphere = ehex(test['atm'])
            planet.determine_greenhouse()
            LOGGER.debug(
                'atm = %s expected = %s planet = %s, result = %s',
                test['atm'],
                test['expected'],
                str(planet),
                planet.greenhouse.dict()
            )
            if isinstance(test['expected'], tuple):
                # pragma pylint: disable=E1136
                self.assertTrue(planet.greenhouse.min() == test['expected'][0])
                self.assertTrue(planet.greenhouse.max() == test['expected'][1])
            else:
                self.assertTrue(planet.greenhouse.min() == test['expected'])
                self.assertTrue(planet.greenhouse.max() == test['expected'])

    def test_albedo_land_coverage(self):
        '''
        Test albedo land coverage
        desert_coverage = 10% * (10 - hydrographics)
        Modifiers:
        - Vacuum/trace atmosphere => desert_coverage = 100%
        - Very thin atmosphere => desert_coverage +10%
        - Thin atmosphere => desert_coverage +5%
        - Dense atmosphere => desert_coverage -5%
        '''
        planet = LBB6Planet()
        for hyd in range(0, 11):
            for atm in range(0, 10):
                expected = float((10 - hyd)) * 0.1
                if atm <= 1:
                    expected = 1.0
                if atm >= 2 and atm <= 3:
                    expected += 0.1
                if atm >= 4 and atm <= 5:
                    expected += 0.05
                if atm >= 8 and atm <= 9:
                    expected -= 0.05
                if hyd == 0:
                    expected = 1.0
                expected = round(expected, 2)
                expected = min(1.0, expected)
                expected = max(0.0, expected)
                planet.hydrographics = ehex(hyd)
                planet.atmosphere = ehex(atm)
                desert_coverage = planet._albedo_determine_desert_coverage()
                LOGGER.debug(
                    'uwp %s expected = %s actual = %s',
                    str(planet), expected, desert_coverage)
                self.assertTrue(expected == desert_coverage)

    def test_albedo_ice_coverage(self):
        '''
        Test albedo_ice_coverage
        Inner zone => ice_coverage = 0%
        HZ => ice_coverage == 10%
        Outer zone => ice_coverage = hydrographics
        Can't find orbit or star => ice_coverage = 10%
        '''
        planet = LBB6Planet(uwp='X644000-0')
        # Inner zone
        planet.generate(star=Star('G2 V'), orbit=Orbit(1))
        self.assertTrue(planet._determine_albedo_ice_coverage() == 0.0)
        # Habitable zone
        planet.generate(star=Star('G2 V'), orbit=Orbit(3))
        self.assertTrue(planet._determine_albedo_ice_coverage() == 0.1)
        # Outer zone
        planet.generate(star=Star('G2 V'), orbit=Orbit(5))
        for hyd in range(0, 11):
            planet.hydrographics = ehex(hyd)
            self.assertTrue(planet._determine_albedo_ice_coverage() == float(hyd / 10.0))

    def test_temperature_formula(self):
        '''Test temperature formula'''
        temp = LBB6Planet._temperature_formula(
            1.0,    # Luminosity
            0.3,    # Albedo
            1.0,    # Distance (AU)
            1.1     # Greenhouse effect
        )
        LOGGER.debug('temp = %s', temp)
        self.assertTrue(temp == 288)
