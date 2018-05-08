'''test_class_ct_lbb3_animal.py'''

# pragma pylint: disable=C0413, W0613, C0301

import json
import logging
import os
import sys
import unittest
from mock import patch
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.ct.lbb3.encounter.tables import TERRAIN_TYPES_DM
from traveller_api.ct.lbb3.encounter.animal import Hits
from traveller_api.ct.lbb3.encounter.animal import Herbivore
from traveller_api.ct.lbb3.encounter.animal import Carnivore
from traveller_api.ct.lbb3.encounter.animal import Omnivore
from traveller_api.ct.lbb3.encounter.animal import Scavenger
from traveller_api.ct.lbb3.encounter.event import Event
from traveller_api.ct.lbb3.encounter.encounter_table import EncounterTable1D
from traveller_api.ct.lbb3.encounter.encounter_table import EncounterTable2D

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def mock_d6_roll_3(dice=1, modifier=0, floor=0, ceiling=9999):
    '''Mock D6.roll() - return 3 * dice + modifier'''
    result = 3 * dice + modifier
    result = max(floor, result)
    result = min(ceiling, result)
    # LOGGER.debug('returning %s', result)
    return result


def mock_d6_roll_6(dice=1, modifier=0, floor=0, ceiling=9999):
    '''Mock D6.roll() - return 6 * dice + modifier'''
    result = 6 * dice + modifier
    result = max(floor, result)
    result = min(ceiling, result)
    LOGGER.debug('returning %s', result)
    return result


def mock_randint(lower, upper):
    '''Mock randint'''
    return upper


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
    '''Test quick animal creates'''

    def test_animal_basic(self):
        '''Test quick animal creates by terrain type'''
        for terrain in TERRAIN_TYPES_DM:
            for supertype in [Herbivore, Carnivore, Omnivore, Scavenger]:
                LOGGER.debug('terrain = %s, supertype = %s', terrain, supertype)
                _ = supertype(terrain)

    def test_animal_uwp(self):
        '''Test animal create with terrain type and uwp'''
        uwp = 'A788989-A'
        for terrain in TERRAIN_TYPES_DM:
            for supertype in [Herbivore, Carnivore, Omnivore, Scavenger]:
                LOGGER.debug('terrain = %s, supertype = %s', terrain, supertype)
                _ = supertype(terrain, uwp=uwp)

    def test_create_bogus_uwp(self):
        '''Test for ValueError with bad UWP'''
        uwp = 'Not a UWP, really'
        with self.assertRaises(ValueError):
            _ = Carnivore('Clear', uwp)


class TestHerbivore(unittest.TestCase):
    '''Herbivore unit tests'''

    @patch('traveller_api.ct.util.Die.roll', side_effect=mock_d6_roll_3)
    def test_create(self, mock_fn):
        '''Test create for Animal'''
        herbvivore = Herbivore('Clear')
        LOGGER.debug('Animal = %s', str(herbvivore))
        self.assertTrue(str(herbvivore) == '6 Grazers 50 kg 12/6 none 6 hooves and teeth F3 A5 S2')

    def test_create_invalid_terrain(self):
        '''Test create with invalid terrain type'''
        with self.assertRaises(ValueError):
            _ = Herbivore('map is not the terrain')


class TestEncounterTable1D(unittest.TestCase):
    '''6-row encounter table tests'''

    @patch('traveller_api.ct.util.Die.roll', side_effect=mock_d6_roll_3)
    def test_create(self, mock_fn):
        '''Test create for EncounterTable1D'''

        expected = '\n'.join([
            'Clear Terrain ',
            'Die Animal Type                  Weight Hits  Armor     Wounds & Weapons',
            '  1  1 Hijacker                   50 kg 12/6  none       6 thrasher            A4 F5 S1',
            '  2  6 Grazers                    50 kg 12/6  none       6 hooves and teeth    F3 A5 S2',
            '  3  6 Grazers                    50 kg 12/6  none       6 hooves and teeth    F3 A5 S2',
            '  4  6 Grazers                    50 kg 12/6  none       6 hooves and teeth    F3 A5 S2',
            '  5  1 Gatherer                   50 kg 12/6  none       3 claws               A6 F5 S1',
            '  6  1 Chaser                     50 kg 12/6  none       9 stinger             A0 F6 S1'
        ])

        table = EncounterTable1D('Clear')
        LOGGER.debug('expected = "%s"', expected)
        LOGGER.debug('received = "%s"', str(table))
        self.assertTrue(str(table) == expected)


class TestEncounterTable2D(unittest.TestCase):
    '''6-row encounter table tests'''

    @patch('traveller_api.ct.util.Die.roll', side_effect=mock_d6_roll_3)
    @patch(
        'traveller_api.ct.lbb3.encounter.event.randint',
        side_effect=mock_randint
    )
    def test_create(self, mock_fn, mock_fn2):
        '''Test create for EncounterTable2D'''

        expected = '\n'.join([
            "Clear Terrain ",
            "Die Animal Type                  Weight Hits  Armor     Wounds & Weapons",
            "  2  1 Hijacker                   50 kg 12/6  none       6 thrasher            A4 F5 S1",
            "  3  1 Gatherer                   50 kg 12/6  none       3 claws               A6 F5 S1",
            "  4  1 Hijacker                   50 kg 12/6  none       6 thrasher            A4 F5 S1",
            "  5  1 Gatherer                   50 kg 12/6  none       3 claws               A6 F5 S1",
            "  6  6 Grazers                    50 kg 12/6  none       6 hooves and teeth    F3 A5 S2",
            "  7  6 Grazers                    50 kg 12/6  none       6 hooves and teeth    F3 A5 S2",
            "  8  6 Grazers                    50 kg 12/6  none       6 hooves and teeth    F3 A5 S2",
            "  9  1 Chaser                     50 kg 12/6  none       9 stinger             A0 F6 S1",
            " 10 Light seekers. About 40 large slug-like creatures are attracted to the band's",
            "    lights, and crawl slowly towards them. They are poisonous, inflicting 2D hits per",
            "    touch (50kg 10/2 S1)",
            " 11  1 Chaser                     50 kg 12/6  none       9 stinger             A0 F6 S1",
            " 12  1 Chaser                     50 kg 12/6  none       9 stinger             A0 F6 S1",
        ])
        expected_dict = {
            'rows': [
                ('2',
                 {'armor': 'none',
                  'behaviour': 'A4 F5 S1',
                  'hits': {'dead': 6, 'unconscious': 12},
                  'quantity': 1,
                  'terrain': 'Clear',
                  'type': 'Hijacker',
                  'weapons': 'thrasher',
                  'weight': 50,
                  'wounds': 6}),
                ('3',
                 {'armor': 'none',
                  'behaviour': 'A6 F5 S1',
                  'hits': {'dead': 6, 'unconscious': 12},
                  'quantity': 1,
                  'terrain': 'Clear',
                  'type': 'Gatherer',
                  'weapons': 'claws',
                  'weight': 50,
                  'wounds': 3}),
                ('4',
                 {'armor': 'none',
                  'behaviour': 'A4 F5 S1',
                  'hits': {'dead': 6, 'unconscious': 12},
                  'quantity': 1,
                  'terrain': 'Clear',
                  'type': 'Hijacker',
                  'weapons': 'thrasher',
                  'weight': 50,
                  'wounds': 6}),
                ('5',
                 {'armor': 'none',
                  'behaviour': 'A6 F5 S1',
                  'hits': {'dead': 6, 'unconscious': 12},
                  'quantity': 1,
                  'terrain': 'Clear',
                  'type': 'Gatherer',
                  'weapons': 'claws',
                  'weight': 50,
                  'wounds': 3}),
                ('6',
                 {'armor': 'none',
                  'behaviour': 'F3 A5 S2',
                  'hits': {'dead': 6, 'unconscious': 12},
                  'quantity': 6,
                  'terrain': 'Clear',
                  'type': 'Grazers',
                  'weapons': 'hooves and teeth',
                  'weight': 50,
                  'wounds': 6}),
                ('7',
                 {'armor': 'none',
                  'behaviour': 'F3 A5 S2',
                  'hits': {'dead': 6, 'unconscious': 12},
                  'quantity': 6,
                  'terrain': 'Clear',
                  'type': 'Grazers',
                  'weapons': 'hooves and teeth',
                  'weight': 50,
                  'wounds': 6}),
                ('8',
                 {'armor': 'none',
                  'behaviour': 'F3 A5 S2',
                  'hits': {'dead': 6, 'unconscious': 12},
                  'quantity': 6,
                  'terrain': 'Clear',
                  'type': 'Grazers',
                  'weapons': 'hooves and teeth',
                  'weight': 50,
                  'wounds': 6}),
                ('9',
                 {'armor': 'none',
                  'behaviour': 'A0 F6 S1',
                  'hits': {'dead': 6, 'unconscious': 12},
                  'quantity': 1,
                  'terrain': 'Clear',
                  'type': 'Chaser',
                  'weapons': 'stinger',
                  'weight': 50,
                  'wounds': 9}),
                ('10',
                 {'armor': None,
                  'behaviour': None,
                  'hits': None,
                  'quantity': None,
                  'terrain': 'Clear',
                  'type': 'Light seekers. About 40 large slug-like creatures are '
                          "attracted to the band's lights, and crawl slowly towards "
                          'them. They are poisonous, inflicting 2D hits per touch '
                          '(50kg 10/2 S1)',
                  'weapons': None,
                  'weight': None,
                  'wounds': None}),
                ('11',
                 {'armor': 'none',
                  'behaviour': 'A0 F6 S1',
                  'hits': {'dead': 6, 'unconscious': 12},
                  'quantity': 1,
                  'terrain': 'Clear',
                  'type': 'Chaser',
                  'weapons': 'stinger',
                  'weight': 50,
                  'wounds': 9}),
                ('12',
                 {'armor': 'none',
                  'behaviour': 'A0 F6 S1',
                  'hits': {'dead': 6, 'unconscious': 12},
                  'quantity': 1,
                  'terrain': 'Clear',
                  'type': 'Chaser',
                  'weapons': 'stinger',
                  'weight': 50,
                  'wounds': 9})],
            'terrain': 'Clear',
            'uwp': None}


        expected_json = json.dumps(expected_dict, sort_keys=True)

        table = EncounterTable2D('Clear')

        # str()
        LOGGER.debug('expected = "%s"', expected)
        LOGGER.debug('received = "%s"', str(table))
        self.assertTrue(str(table) == expected)

        # dict()
        LOGGER.debug('expected_dict = %s', expected_dict)
        LOGGER.debug('received dict = %s', table.dict())
        self.assertTrue(table.dict() == expected_dict)

        # json()
        LOGGER.debug('expected_json = %s', expected_json)
        LOGGER.debug('received JSON = %s', expected_json)
        self.assertTrue(table.json() == expected_json)



class TestEvent(unittest.TestCase):
    '''Event() unit tests'''

    def test_create(self):
        '''Basic create test'''
        for terrain in TERRAIN_TYPES_DM:
            LOGGER.debug('terrain = %s', terrain)
            _ = Event(terrain, strict=False)

        # Create with UWP
        uwp = 'A544765-9'
        for terrain in TERRAIN_TYPES_DM:
            LOGGER.debug('terrain = %s', terrain)
            _ = Event(terrain, uwp=uwp, strict=False)

        # Test for ValueError on bogus terrain
        with self.assertRaises(ValueError):
            _ = Event('candyfloss')

        # Test for ValueError on bogus UWP
        with self.assertRaises(ValueError):
            _ = Event('Clear', uwp='flatworld')

    @patch('traveller_api.ct.lbb3.encounter.event.randint', side_effect=mock_randint)
    def test_representations(self, mock_fn):
        '''Test representations - str(), dict(), json()'''
        expected = 'Light seekers. About 40 large slug-like creatures ' +\
        'are attracted to the band\'s lights, and crawl slowly towards ' +\
        'them. They are poisonous, inflicting 2D hits per touch (50kg 10/2 S1)'
        expected_dict = {
            'terrain': 'Clear',
            'quantity': None,
            'type': expected,
            'weight': None,
            'hits': None,
            'wounds': None,
            'weapons': None,
            'armor': None,
            'behaviour': None
        }
        event = Event('Clear')
        LOGGER.debug('event = %s', str(event))

        self.assertTrue(str(event) == expected)
        self.assertTrue(event.dict() == expected_dict)
        self.assertTrue(event.json() == json.dumps(expected_dict, sort_keys=True))
