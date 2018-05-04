'''event.py'''

import json
import logging
from random import randint, seed
from traveller_api.ct.lbb3.worldgen.planet import System
from traveller_api.ct.lbb3.encounter.tables import TERRAIN_TYPES_DM

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

EVENTS_CLEAR_TABLE = [
    'Chameleon filter. The lead character is surprised at close range by a ' +\
    'camouflaged filter (100kg, 22/2 cloth+1 6 teeth+1 A0 F0 S0). It has ' +\
    'surprise and attacks.',
    'Lengthy storm. A rainstorm with near-zero visibility and 100km/h winds ' +\
    'occurs. Travel is impossible, either in the air or on the ground. ' +\
    'Duration 1D days.',
    'Hallucinogenic spores. Floral pollen breathed without filters cause ' +\
    'hallucinations (of animal attacks or unreal situations). Duration of ' +\
    'the hallucinations is 20 - END minutes.',
    'High "grass". The vegetation here is over 2m tall, making it difficult ' +\
    'to see more than short range. Roll for an animal encounter, taking ' +\
    'place at short range.',
    'Boulder plain. The terrain is flat, but studded by large rocks ' +\
    '(probably left by glacial action). Straight line travel becomes ' +\
    'impossible, increasing travel time by 20%.',
    'Sink hole. A large vertical shaft is encountered, with sheer sides ' +\
    'and water at the bottom. If encountered by surprise, roll 6+ DEX to ' +\
    'avoid. Vehicle drivers roll 7+ vehicle skill to avoid.',
    'Soft ground. The terrain becomes very soft; vehicles dig in and slow ' +\
    'down. Vehicle speed is reduced by 75%, foot speed by 50%.',
    'Creekbed. A minor dip reveals a dry creek. Throw 9+ to avoid getting ' +\
    'a vehicle stuck in a concealed mudhole.',
    'Light seekers. About 40 large slug-like creatures are attracted to the ' +\
    'band\'s lights, and crawl slowly towards them. They are poisonous, ' +\
    'inflicting 2D hits per touch (50kg 10/2 S1)'
]
EVENTS_ROUGH_TABLE = [
    'Broken axle. The band\'s vehicle suffers a broken axle (or similar). ' +\
    'Repairs will take at least one day, requiring at lease Mechanical-1. ' +\
    'If the skill is not available, outside help will be required.',
    'Tar pit. A natural asphalt deposit is encountered. Roll once to ' +\
    'determine the animal trapped in it, and then twice to determine ' +\
    'animals near the pit.',
    'Hot springs. A source of steaming hot water is encountered. At ' +\
    'irregular intervals the pool turns into a steam geyser. Anyone ' +\
    'caught in the geyser suffers 4D damage.',
    'Heavy metal deposits. Characters may make a 12+ roll (DMs INT, EDU)' +\
    'to notice heavy metal deposits. If exploited, they will be worth ' +\
    'MCr1 per year. If sold to a mining company, the right will be worth ' +\
    'Cr 50000.',
    'No roads. No roads or paths are apparent. Vehicles must detour; ' +\
    'Pedestrians may continue at 25% speed.',
    'Violent rainstorm. A sudden storm reduces visibility to medium range ' +\
    'or less. Roll 8+ on relevant vehicle skill to avoid an accident.',
    'Ravines and precipices. See LBB3 p 31.',
    'Trapper web. The lead character encounters a large adhesive web ' +\
    'without the trapper present. The trapper will return in 4 rounds ' +\
    '(Trapper 100kg 10/5 mesh 6 horns A9 F9 S2).',
    'Rocky ground. The terrain becomes extremely rocky. Throw 9+ to avoid ' +\
    'becoming stuck, and reduce speed by 50%.'
]
EVENTS_MOUNTAIN_TABLE = []
EVENTS_FOREST_TABLE = []
EVENTS_RIVER_TABLE = [
    'Bad water. The water is contaminated with heavy metal concentrations ' +\
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
            return _list[randint(0, len(_list) - 1)]
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
        return json.dumps(self.dict(), sort_keys=True)
