'''test_class_t5_orbit.py'''

# pragma pylint: disable=relative-beyond-top-level
# pragma pylint: disable=C0413, E0401

import json
import logging
import os
import sys
import unittest
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.t5.orbit.orbit import Orbit

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class TestOrbit(unittest.TestCase):
    '''Test Orbit() class'''

    def test_orbit_basic(self):
        '''Basic Orbit() tests'''
        for orbit_number in [1, 1.3]:
            orbit = Orbit(orbit_number)
            self.assertTrue(isinstance(orbit, Orbit))
            self.assertTrue(orbit.orbit_number == float(orbit_number))

    def test_orbit_bogus(self):
        '''Test create with bogus orbit_numbers'''
        # Test orbit number invalid type
        for orbit_number in ['String', None, []]:
            with self.assertRaises(TypeError):
                _ = Orbit(orbit_number)
        # Test orbit number out of range
        for orbit_number in [-1, 21]:
            with self.assertRaises(ValueError):
                _ = Orbit(21)

    def test_json(self):
        '''Test JSON representation'''
        expected = {
            "au": 1.0,
            "mkm": 150,
            "orbit_number": 3.0
        }
        orbit = Orbit(3)
        LOGGER.debug(
            'expected = %s', json.dumps(expected, sort_keys=True)
        )
        LOGGER.debug(
            'actual = %s', orbit.json()
        )
        self.assertTrue(orbit.json() == json.dumps(expected, sort_keys=True))
