'''test_class_ct_lbb3_animal.py'''

# pragma pylint: disable=C0413, W0613, C0301

import logging
import os
import sys
import unittest
from mock import patch
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.ct.lbb3.encounter.animal import Hits, Herbivore
from traveller_api.ct.lbb3.encounter.encounter_table import EncounterTable6

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def mock_d6_roll_3(dice=1, modifier=0, floor=0, ceiling=9999):
    '''Mock D6.roll() - return 3 * dice + modifier'''
    result = 3 * dice + modifier
    result = max(floor, result)
    result = min(ceiling, result)
    LOGGER.debug('returning %s', result)
    return result


def mock_d6_roll_6(dice=1, modifier=0, floor=0, ceiling=9999):
    '''Mock D6.roll() - return 6 * dice + modifier'''
    result = 6 * dice + modifier
    result = max(floor, result)
    result = min(ceiling, result)
    LOGGER.debug('returning %s', result)
    return result


class TestHits(unittest.TestCase):
    '''Hits unit tests'''

    @patch('traveller_api.ct.util.Die.roll', side_effect=mock_d6_roll_3)
    def test_hits_basic(self, mock_fn):
        '''Basic Hits() tests'''
        hits = Hits(4)
        LOGGER.debug('hits = %s', str(hits))
        self.assertTrue(hits.unconscious == 6)
        self.assertTrue(hits.dead == 6)
        self.assertTrue(str(hits) == '6/6')


class TestAnimal(unittest.TestCase):
    '''Animal unit tests'''

    def test_size_plus_6(self):
        '''Test size +6 entry'''
        pass


class TestHerbivore(unittest.TestCase):
    '''Herbivore unit tests'''

    @patch('traveller_api.ct.util.Die.roll', side_effect=mock_d6_roll_3)
    def test_create(self, mock_fn):
        '''Test create for Animal'''
        herbvivore = Herbivore('Clear')
        LOGGER.debug('Animal = %s', str(herbvivore))
        self.assertTrue(str(herbvivore) == '6 Grazers 50 kg 9/6 none 6 hooves and teeth F3 A5 S2')

class TestEncounterTable6(unittest.TestCase):
    '''6-row encounter table tests'''

    @patch('traveller_api.ct.util.Die.roll', side_effect=mock_d6_roll_3)
    def test_create(self, mock_fn):
        '''Test create for EncounterTable6'''

        expected = '\n'.join([
            'Clear Terrain ',
            'Die Animal Type                  Weight Hits  Armor     Wounds & Weapons',
            '  1  1 Hijacker                   50 kg 9/6   none       6 thrasher            A4 F5 S1',
            '  2  6 Grazers                    50 kg 9/6   none       6 hooves and teeth    F3 A5 S2',
            '  3  6 Grazers                    50 kg 9/6   none       6 hooves and teeth    F3 A5 S2',
            '  4  6 Grazers                    50 kg 9/6   none       6 hooves and teeth    F3 A5 S2',
            '  5  1 Gatherer                   50 kg 9/6   none       3 claws               A6 F5 S1',
            '  6  1 Chaser                     50 kg 9/6   none       9 stinger             A0 F6 S1'
        ])

        table = EncounterTable6('Clear')
        LOGGER.debug('expected = "%s"', expected)
        LOGGER.debug('received = "%s"', str(table))
        self.assertTrue(str(table) == expected)
