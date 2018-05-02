'''event.py'''

import json
import logging
from random import randint, seed
from traveller_api.ct.lbb3.worldgen.planet import System
from traveller_api.ct.lbb3.encounter.animal import TERRAIN_TYPES_DM

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

EVENTS_CLEAR_TABLE = []
EVENTS_ROUGH_TABLE = []
EVENTS_MOUNTAIN_TABLE = []
EVENTS_FOREST_TABLE = []
EVENTS_RIVER_TABLE = [
    'Bad water. The water is contaminated with heavy metal concentrations' +\
        'Bathing in, or drinking, the water will cause illness fof 1D ' +\
        'days. Roll END 8+ to avoid',
    'Poison pouncer. A character is bitten by a poisonous creature. The ' +\
        'bite causes unconsciousness almost immediately and death in 24 ' +\
        'hours unless treated. Antidote is available in locally-sourced ' +\
        'medkits',
    'Swimming eaters. An unlimited number of aggressive eaters lurk ' +\
        'beneath the surface and will attack on sight. \n' + \
        '1 kg 2/0 none 2 teest A0 F0 S1',
    'Accidental bridge. The river is spanned by a falled tree. Make a 6+ ' +\
        'DEX roll to avoid 2D injury if crossing',
    'Rapids. The river closes in to a narrow channel with no path on the ' +\
        'banks. The adventurers must proceed in boats or rafts',
    'River ends. The river goes underground.',
    'River high. The river is swollen after recent precipitaion. Travel ' +\
        'along or across the river is treacherous',
    'Flash flood. A wall of water sweeps down the river. Roll 10+ to avoid ' +\
        'land vehicles being overturned. Individuals roll DEX 10+ to avoid ' +\
        '3D injury'
]
EVENTS_SWAMP_TABLE = []
EVENTS_DESERT_TABLE = []
EVENTS_BEACH_TABLE = []
EVENTS_OCEAN_SURFACE_TABLE = []
EVENTS_OCEAN_DEEPS_TABLE = []
EVENTS_RUINS_TABLE = []
EVENTS_CAVE_TABLE = []
EVENTS_VACUUM_TABLE = [
    'Dust pool. Fine dust conceals a deep pit. Roll 6+ to avoid or 2D damage',
    'Stellar flare. Communications impossible without touching helmets',
    'Spongy soil. Walking speed reduced by 50%',
    'Ice field. Frozen water concealed by dust. ' +\
        'Make 6+ DEX roll to avoid slip (1D damage)',
    'Rill. A deep crevasse blocks the way. Add 2D hours to travel time',
    'Seismic event. See LBB3, page 31',
    'Gas vent. A crevice is venting a grey gas. It will etch to opacity ' +\
        'a vacc suit faceplate and in 5 rounds breach the suit',
    'Stellar flare. High radiation danger over an extended period, ' +\
        'inflicting 1D hits after 5 days',
    'Meteor shower. See LBB3, page 31',
    'Tracks. ATV tracks cross the adventurers\' path',
]


class Event(object):
    '''Event class'''

    def __init__(self, terrain, uwp=None, strict=True):
        self.terrain = None
        self.planet = None
        self.event = ''
        if strict is True:
            self._strict = True
        else:
            self._strict = False

        LOGGER.debug('terrain_type = %s', terrain)
        LOGGER.debug('uwp = %s', uwp)
        try:
            assert terrain in TERRAIN_TYPES_DM
            self.terrain = terrain
        except AssertionError:
            raise ValueError('Invalid terrain type {}'.format(terrain))
        if uwp is not None:
            try:
                self.planet = System(uwp=uwp)
            except TypeError:
                raise ValueError('Invalid UWP {}'.format(uwp))

        seed()
        self.generate()

    def generate(self):
        '''Generate event based on self.terrain'''

        '''
        Clear, Prairie
        Rough, Broken, Crater
        Mountain
        Forest, Jungle
        River
        Swamp, Marsh
        Desert
        Beach
        Surface
        Shallows, Depths, Bottom, Sea Cave, Sargasso
        Ruins
        Cave, Chasm
        '''
        if self.terrain in ['Clear', 'Prairie']:
            self.event = self._random_list_item(EVENTS_CLEAR_TABLE)
        if self.terrain in ['Rough', 'Broken', 'Crater']:
            self.event = self._random_list_item(EVENTS_ROUGH_TABLE)
        if self.terrain == 'Mountain':
            self.event = self._random_list_item(EVENTS_MOUNTAIN_TABLE)
        if self.terrain in ['Forest', 'Jungle']:
            self.event = self._random_list_item(EVENTS_FOREST_TABLE)
        if self.terrain == 'River':
            self.event = self._random_list_item(EVENTS_RIVER_TABLE)
        if self.terrain in ['Swamp', 'Marsh']:
            self.event = self._random_list_item(EVENTS_SWAMP_TABLE)
        if self.terrain == 'Desert':
            self.event = self._random_list_item(EVENTS_DESERT_TABLE)
        if self.terrain == 'Beach':
            self.event = self._random_list_item(EVENTS_BEACH_TABLE)
        if self.terrain == 'Surface':
            self.event = self._random_list_item(EVENTS_OCEAN_SURFACE_TABLE)
        if self.terrain in [
                'Shallows', 'Depths', 'Bottom',
                'Sea Cave', 'Sargasso'
            ]:
            self.event = self._random_list_item(EVENTS_OCEAN_DEEPS_TABLE)
        if self.terrain == 'Ruins':
            self.event = self._random_list_item(EVENTS_RUINS_TABLE)
        if self.event in ['Cave', 'Chasm']:
            self.event = self._random_list_item(EVENTS_CAVE_TABLE)

        if self.planet is not None:
            if (
                    int(self.planet.atmosphere) == 0 and
                    int(self.planet.size) != 0
            ):
                self.event = self._random_list_item(EVENTS_VACUUM_TABLE)

    def _random_list_item(self, _list):
        '''Return random item from list'''
        try:
            return _list[0, randint(0, len(_list) - 1)]
        except ValueError:
            if self._strict:
                raise ValueError('Insufficient data in table')
            else:
                return 'Referee-supplied event'

    def __str__(self):
        return self.event

    def dict(self):
        '''dict() representation'''
        doc = {
            'terrain': self.terrain,
            'quantity': None,
            'type': self.event,
            'weight': None,
            'hits': None,
            'wounds': None,
            'weapons': None,
            'armor': None,
            'behaviour': None
        }
        return doc

    def json(self):
        '''JSON representation'''
        return json.dumps(self.dict())
