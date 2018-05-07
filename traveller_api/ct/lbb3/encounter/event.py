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
EVENTS_MOUNTAIN_TABLE = [
    'Narrow trail. The road or path ahead narrows to about 1 metre ' +\
        'in width and appears to remain so for the next few ' +\
        'kilometres. The trail is impassable to vehicles.',
    'Electrical storm. Heavy winds and lightning force the party to ' +\
        'halt for 12 hours. Unless a refuge is available (throw 7+ ' +\
        'for a cave, cabin, etc), a lightning hit on electrical ' +\
        'equipment (throw 9+) will incapacitate it.',
    'Sun-influenced crystal structures. At about midday, light from ' +\
        'the sun strikes a crystalline outcrop and randomly flashes ' +\
        'energy about. Each character must make an 8+ DEX roll to ' +\
        'avoid being hit. Damage is as laser carbine, and reflec ' +\
        'protects.',
    'Avalanche. Throw 8+ for a loud noise (vehicle, conversaton, etc) ' +\
        'to precipitate an avalanche. Make an 8+ DEX roll to avoid ' +\
        '3D injury. Throw tonnage of vehicle or less to avoid ' +\
        'destruction of vehicle.',
    'Freezing weather. Temperatures go to below zero. Individuals not ' +\
        'expressly dressed for for such cold throw endurance or less ' +\
        'each hour to avoid suffering 2 points of damage. Continue ' +\
        'until shelter is reached.',
    'Natural bridge. A large crevasse blocks progress, and is spanned ' +\
        'by a large natural arch. Throw vehicle tonnage or greater to ' +\
        'successfully cross.',
    'Falling rocks. Rocks have been dislodged overhead and begin ' +\
        'falling. 2D rocks fall, each throwing 10+ to hit a vehicle ' +\
        'or individual (inflicting 2D hts).',
    'Cave. A deep mountain cave is encountered, with a shallow stream ' +\
        'and two wide banks exiting. Concealed behind a large rock ' +\
        'is an interior extension leading deeper into the mountain.',
    'Crevasse. A deep crevasse (100m across) is encountered, ' +\
        'blockng further progress.'
]
EVENTS_FOREST_TABLE = [
    'Poison pouncer. This carnivore lies in wait for worthy prey, and ' +\
        'attacks with surprise at close or short range. Its first bite ' +\
        'does double damage. (50kg 10/10 jack 11 teeth+1 A0 F9 S3)',
    'Webs. If the event achieves surprise, the lead character or vehicle ' +\
        'is trapped in a large web strung between trees.',
    'Venemous arthropods. While stopped, several poisonous creatures ' +\
        'insert themselves in likely places (boots, packs, etc) and ' +\
        'attack when a character then encounters them. Make a 6+ DEX ' +\
        'roll to avoid being bitten for 3D damage.',
    'Soft ground. This area will not support gound vehicles, forcing a ' +\
        'detour and delay of at least one day. Individuals on foot can ' +\
        'proceed at half speed.',
    'Forest fire. The forest is burning, with the flame front heading for ' +\
        'the adventurers. All animals in the table run blindly towards the ' +\
        'group. Each animal will attack if blocked.',
    'Dense underbrush. Continued passage through this portion of the ' +\
        'forest is obstructed by very dense undergrowth. it can be cut ' +\
        'through with ' +\
        'cutlasses or blades at one-quarter speed. Vehicles cannot force ' +\
        'their way through.',
    'Tanglewood. The entire floor of the forest is covered with a low ' +\
        'network of sticky flexible roots. Running is impossible, ' +\
        'walking is difficult. Reduce speed to one quarter.',
    'Jungle drums. Distant drums are heard in a varying rhythm. If they ' +\
        'are sought out, they are determined to be caused by a natural ' +\
        'phenomenon produced by a large grove of hollow trees.',
    'Monsoon. A storm begins with steady rain and gentle winds, ' +\
        'increasing to violent wind and heavy rain on the second day. ' +\
        'It reduces visibility completely and forces a halt. It ends ' +\
        'after three days.',
    'Giant camouflaged filter. The travellers are surprised by a giant ' +\
        'filter at close range (16000kg 90/20 mesh 19 teeth A0 F0 S0)'
]
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
EVENTS_SWAMP_TABLE = [
    'Path ends. The swamp has turned to bayou and no further progress ' +\
        'is possible by land. Further movement must be by water, either ' +\
        'swimming or by boat or raft. Water depth averages 3m.',
    'Marsh gas. Gas released from the swamp glows in the dark, and may ' +\
        'give the appaearance of a ship landing nearby, or of camp fires ' +\
        'in the distance. It is nearly impossible to find the source of ' +\
        'the gas. Marsh gas is inflammable.',
    'Dense fog. Mist and fog obscure vision, reducing visibility to ' +\
        'medium range or less. Progress is reduced to half normal ' +\
        'speed.',
    'Quicksand. Shallow water conceals a patch of quicksand. Anyone ' +\
        'trapped in it mus roll 15+ per combat round to be pulled under. ' +\
        'DMs: -1 per round trapped, +1 per companion assisting. Escape ' +\
        'after 2D combat rounds.',
    'Noxious gases. The area is filled with foul-smelling fumes, as if ' +\
        'from rotting carrion. Investigation will reveal a patch of ' +\
        'poison water and ground. Tests will reveal a high level of ' +\
        'mercury contamination.',
    'Bog. The soil in the swamp is moist and soft. Ordinary wheeled ' +\
        'vehicles are completely stopped; ATVs are reduced to very ' +\
        'slow speed. Individuals are reduced to one-quarter speed.',
]
EVENTS_DESERT_TABLE = [
    'Oasis. A small water-hole is encountered. Throw 10+ for it to be ' +\
        'a mirage when approached. If it is real, throw 9+ for the water ' +\
        'to be poisonous, with appropriate clues.',
    'Drum sand. This terrain feature echoes footsteps and vehicle' +\
        ' noise to attract local predators, especially this: (64000kg ' +\
        '85/30 battle 20 thrasher A3 F9 S2)',
    'Very broken and rough ground. Impassable to vehicles of any type, and ' +\
        'passable to those on foot only at one quarte speed.',
    'Mirage. An oasis appears on the horizon, but dissolves into nothing ' +\
        'as it is approached. This continues until nightfall.',
    'Trapper. A conical pit dug in sand has a brittle rim. Anyone standing ' +\
        'on the rim will tumple in. The walls are loose sand, and prevent ' +\
        'escape without help or lots of time. There is no trapper ' +\
        'present.',
    'Violent sandstorm. Extreme winds whip abrasive sand particles at ' +\
        'grinding force. Progress is impossible for at least a day. ' +\
        'Individuals will be buried, and vehicle windscreens abraded ' +\
        'to translucency.',
    'Sand sea. This area is composed of soft sand and dunes. Walking is ' +\
        'at one quarter speed. Vehicle speed is reduced to 20 km/h.',
    'Oasis. Vegetation is clustered around a pool of fresh water. Roll ' +\
        'for an animal encounter.'
]
EVENTS_BEACH_TABLE = [
    'Poison Intermittent. A small animal with a shiny metallic shell ' +\
        'is noticed on the beach. Any wound it inflicts will not heal ' +\
        'for at least 90 days.',
    'Undertow. Individuals in the water will find themselves being ' +\
        'dragged out to sea at S1.',
    'Beached animal. A huge sea creature has been washed up on the beach. ' +\
        'Roll twice on the table to select scavengers and carnivores ' +\
        'eating the carcass.'
]
EVENTS_OCEAN_SURFACE_TABLE = [
    'Storm. Heavy seas and violent winds toss any vehicle present. ' +\
        'Make am 8+ vehicle skill check to avoid a small vehicle ' +\
        'being overturned, or a large vehicle being damaged.',
    'Floating carcass. A large sea creature has died and is floating ' +\
        'at or near the surface. Roll twice for carnivores and ' +\
        'scavengers preying on the body.'
]
EVENTS_OCEAN_DEEPS_TABLE = [
    'Giant hunter. A very large sea creature attacks any vehicle it ' +\
        'encounters. (24000kg 58/16 battle 18 thrasher A0 F0 S2)',
    'Thermocline. A termperature inversion affects the vehicle\'s sensors. ' +\
        'Roll for an animal encounter at short range.',
    'Thermal vent. A uprush of hot water from a volcanic vent is ' +\
        'encountered. Make an 6+ vehicle skill roll to avoid losing control.',
    'Deep sea carcass. A large sea creature has died and is slowly ' +\
        'dropping to the sea bottom. Roll twice for carnivores and ' +\
        'scavengers preying on the body.'
]
EVENTS_RUINS_TABLE = [
    'Referee-supplied event.'
]
EVENTS_CAVE_TABLE = [
    'Referee-supplied event.'
]
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
