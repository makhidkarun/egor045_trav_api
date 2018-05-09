'''test_class_c6_lbb6_expanded_sysgen.py'''

# pragma pylint: disable=C0413, W0613, C0301, W0212

import json
import logging
import os
import sys
import unittest
from mock import patch
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.ct.lbb6_expanded_sysgen.system import LBB6ExpandedStar
from traveller_api.ct.lbb6.planet import LBB6Planet

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

def mock_d6_roll_1(dice=1, modifier=0, floor=0, ceiling=9999):
    '''Mock D6.roll() - return 3 * dice + modifier'''
    result = 1 * dice + modifier
    result = max(floor, result)
    result = min(ceiling, result)
    # LOGGER.debug('returning %s', result)
    return result


class TestExpandedStar(unittest.TestCase):
    '''LBB6ExpandedStar tests'''

    def test_create(self):
        '''Basic create tests'''
        star = LBB6ExpandedStar(mainworld=None, code='G2 V')
        self.assertTrue(str(star) == 'G2 V')

    @patch('traveller_api.ct.util.Die.roll', side_effect=mock_d6_roll_1)
    def test_create_random(self, mock_fn):
        '''Test codeless create'''
        # This mainworld gets a +4 on size and type rolls
        mainworld = LBB6Planet(uwp='A788767-8')
        LOGGER.debug('mainworld type = %s', type(mainworld))
        star = LBB6ExpandedStar(mainworld)
        self.assertTrue(star.type == 'M')
        self.assertTrue(star.size == 'V')


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
        star = LBB6ExpandedStar(mainworld=None, code=code)
        LOGGER.debug('json = %s', star.json())
        self.assertTrue(expected == star.json())
