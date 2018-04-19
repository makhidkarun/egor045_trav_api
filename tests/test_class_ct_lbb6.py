'''CT LBB6 unit tests'''

# pragma pylint: disable=C0413

import json
import logging
import os
import sys
import unittest
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.ct.lbb6.star import Star
from traveller_api.ct.lbb6.orbit import Orbit

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

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
