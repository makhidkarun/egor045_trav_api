'''animal.py'''

import json
import logging
from traveller_api.ct.util import Die
from traveller_api.ct.lbb3.worldgen.planet import System

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)

D6 = Die(6)

TERRAIN_TYPES_DM = {
    'Clear': {'Terrain': 'other', 'Type DM': +3, 'Size DM': 0},
    'Prairie': {'Terrain': 'other', 'Type DM': +4, 'Size DM': 0},
    'Rough': {'Terrain': 'other', 'Type DM': 0, 'Size DM': 0},
    'Broken': {'Terrain': 'other', 'Type DM': -3, 'Size DM': -3},
    'Mountain': {'Terrain': 'other', 'Type DM': 0, 'Size DM': 0},
    'Forest': {'Terrain': 'other', 'Type DM': -4, 'Size DM': -4},
    'Jungle': {'Terrain': 'other', 'Type DM': -3, 'Size DM': -2},
    'River': {'Terrain': 'river', 'Type DM': +1, 'Size DM': +1},
    'Swamp': {'Terrain': 'swamp', 'Type DM': -2, 'Size DM': +4},
    'Marsh': {'Terrain': 'marsh', 'Type DM': 0, 'Size DM': -1},
    'Desert': {'Terrain': 'other', 'Type DM': +3, 'Size DM': -3},
    'Beach': {'Terrain': 'beach', 'Type DM': +3, 'Size DM': +2},
    'Surface': {'Terrain': 'sea', 'Type DM': +2, 'Size DM': +3},
    'Shallows': {'Terrain': 'sea', 'Type DM': +2, 'Size DM': +2},
    'Depths': {'Terrain': 'sea', 'Type DM': +2, 'Size DM': +4},
    'Bottom': {'Terrain': 'sea', 'Type DM': -4, 'Size DM': 0},
    'Sea Cave': {'Terrain': 'sea', 'Type DM': -2, 'Size DM': 0},
    'Sargasso': {'Terrain': 'sea', 'Type DM': -4, 'Size DM': -2},
    'Ruins': {'Terrain': 'other', 'Type DM': -3, 'Size DM': 0},
    'Cave': {'Terrain': 'other', 'Type DM': -4, 'Size DM': +1},
    'Chasm': {'Terrain': 'other', 'Type DM': -1, 'Size DM': -3},
    'Crater': {'Terrain': 'other', 'Type DM': 0, 'Size DM': -1}
}

# ANIMAL_TYPES_TABLE: qty indicates number of dice for # animals (0 => single)
ANIMAL_TYPES_TABLE = [
    {   # 0
        'Herbivore': {'type': 'Filter', 'qty': 1},
        'Omnivore': {'type': 'Gatherer', 'qty': 0},
        'Carnivore': {'type': 'Siren', 'qty': 0},
        'Scavenger': {'type': 'Carrion-eater', 'qty': 1}
    },
    {   # 1
        'Herbivore': {'type': 'Filter', 'qty': 0},
        'Omnivore': {'type': 'Gatherer', 'qty': 0},
        'Carnivore': {'type': 'Pouncer', 'qty': 0},
        'Scavenger': {'type': 'Carrion-eater', 'qty': 2}
    },
    {   # 2
        'Herbivore': {'type': 'Filter', 'qty': 0},
        'Omnivore': {'type': 'Eater', 'qty': 0},
        'Carnivore': {'type': 'Siren', 'qty': 0},
        'Scavenger': {'type': 'Reducer', 'qty': 1}
    },
    {   # 3
        'Herbivore': {'type': 'Intermittent', 'qty': 0},
        'Omnivore': {'type': 'Gatherer', 'qty': 0},
        'Carnivore': {'type': 'Pouncer', 'qty': 0},
        'Scavenger': {'type': 'Hijacker', 'qty': 1}
    },
    {   # 4
        'Herbivore': {'type': 'Intermittent', 'qty': 0},
        'Omnivore': {'type': 'Eater', 'qty': 2},
        'Carnivore': {'type': 'Killer', 'qty': 1},
        'Scavenger': {'type': 'Carrion-eater', 'qty': 2}
    },
    {   # 5
        'Herbivore': {'type': 'Intermittent', 'qty': 1},
        'Omnivore': {'type': 'Gatherer', 'qty': 0},
        'Carnivore': {'type': 'Trapper', 'qty': 0},
        'Scavenger': {'type': 'Intimidator', 'qty': 1}
    },
    {   # 6
        'Herbivore': {'type': 'Intermittent', 'qty': 0},
        'Omnivore': {'type': 'Hunter', 'qty': 0},
        'Carnivore': {'type': 'Pouncer', 'qty': 0},
        'Scavenger': {'type': 'Reducer', 'qty': 0}
    },
    {   # 7
        'Herbivore': {'type': 'Filter', 'qty': 0},
        'Omnivore': {'type': 'Hunter', 'qty': 1},
        'Carnivore': {'type': 'Chaser', 'qty': 0},
        'Scavenger': {'type': 'Carrion-eater', 'qty': 1}
    },
    {   # 8
        'Herbivore': {'type': 'Grazer', 'qty': 1},
        'Omnivore': {'type': 'Hunter', 'qty': 0},
        'Carnivore': {'type': 'Chaser', 'qty': 3},
        'Scavenger': {'type': 'Reducer', 'qty': 3}
    },
    {   # 9
        'Herbivore': {'type': 'Grazer', 'qty': 2},
        'Omnivore': {'type': 'Gatherer', 'qty': 0},
        'Carnivore': {'type': 'Chaser', 'qty': 0},
        'Scavenger': {'type': 'Hijacker', 'qty': 0}
    },
    {   # 10
        'Herbivore': {'type': 'Grazer', 'qty': 3},
        'Omnivore': {'type': 'Eater', 'qty': 1},
        'Carnivore': {'type': 'Killer', 'qty': 0},
        'Scavenger': {'type': 'Intimidator', 'qty': 2}
    },
    {   # 11
        'Herbivore': {'type': 'Grazer', 'qty': 2},
        'Omnivore': {'type': 'Hunter', 'qty': 1},
        'Carnivore': {'type': 'Chaser', 'qty': 2},
        'Scavenger': {'type': 'Reducer', 'qty': 1}
    },
    {   # 12
        'Herbivore': {'type': 'Grazer', 'qty': 4},
        'Omnivore': {'type': 'Gatherer', 'qty': 0},
        'Carnivore': {'type': 'Siren', 'qty': 0},
        'Scavenger': {'type': 'Hijacker', 'qty': 0}
    },
    {   # 13
        'Herbivore': {'type': 'Grazer', 'qty': 5},
        'Omnivore': {'type': 'Gatherer', 'qty': 0},
        'Carnivore': {'type': 'Chaser', 'qty': 1},
        'Scavenger': {'type': 'Intimidator', 'qty': 1}
    }
]

# ANIMAL_ATTRIBUTE_TABLE: terrain_type: (locomotion, size DM)
ANIMAL_ATTRIBUTE_TABLE = [
    {   # 2
        'beach': ('Swimming', 1),
        'marsh': ('Swimming', -6),
        'river': ('Swimming', 1),
        'sea': ('Swimming', 2),
        'swamp': ('Swimming', -3),
        'other': ('', 0)
    },
    {   # 3
        'beach': ('Amphibian', 2),
        'marsh': ('Amphibian', 2),
        'river': ('Amphibian', 1),
        'sea': ('Swimming', 2),
        'swamp': ('Amphibian', 1),
        'other': ('', 0)
    },
    {   # 4
        'beach': ('Amphibian', 2),
        'marsh': ('Amphibian', 1),
        'river': ('', 0),
        'sea': ('Swimming', 2),
        'swamp': ('', 0),
        'other': ('', 0)
    },
    {   # 5
        'beach': ('', 0),
        'marsh': ('', 0),
        'river': ('', 0),
        'sea': ('Amphibian', 2),
        'swamp': ('', 0),
        'other': ('', 0)
    },
    {   # 6
        'beach': ('', 0),
        'marsh': ('', 0),
        'river': ('', 0),
        'sea': ('Amphibian', 0),
        'swamp': ('', 0),
        'other': ('', 0)
    },
    {   # 7
        'beach': ('', 0),
        'marsh': ('', 0),
        'river': ('', 0),
        'sea': ('Swimming', 1),
        'swamp': ('', 0),
        'other': ('', 0)
    },
    {   # 8
        'beach': ('', 0),
        'marsh': ('', 0),
        'river': ('', 0),
        'sea': ('Swimming', -1),
        'swamp': ('', 0),
        'other': ('', 0)
    },
    {   # 9
        'beach': ('', 0),
        'marsh': ('', 0),
        'river': ('', 0),
        'sea': ('Triphibian', -7),
        'swamp': ('', 0),
        'other': ('', 0)
    },
    {   # 10
        'beach': ('', 0),
        'marsh': ('', 0),
        'river': ('', 0),
        'sea': ('Triphibian', -6),
        'swamp': ('', 0),
        'other': ('Flying', -6)
    },
    {   # 11
        'beach': ('Flying', -6),
        'marsh': ('Flying', -6),
        'river': ('Flying', -6),
        'sea': ('Flying', -6),
        'swamp': ('Flying', -6),
        'other': ('Flying', -5)
    },
    {   # 12
        'beach': ('Flying', -5),
        'marsh': ('Flying', -5),
        'river': ('Flying', -5),
        'sea': ('Flying', -5),
        'swamp': ('Flying', -5),
        'other': ('Flying', -3)
    },
]

# SIZE_WEAPONRY_TABLE: {'weight', 'hits', 'wounds', 'weapons', 'armor'}
SIZE_WEAPONRY_TABLE = [
    {'weight': 1, 'hits': (1, 0), 'wounds': '-2D',
     'weapons': 'hooves and horns', 'armor': '+6'},
    {'weight': 3, 'hits': (1, 1), 'wounds': '-2D',
     'weapons': 'horns', 'armor': 'none'},
    {'weight': 6, 'hits': (1, 2), 'wounds': '-1D',
     'weapons': 'hooves and teeth', 'armor': 'none'},
    {'weight': 12, 'hits': (2, 2), 'wounds': '',
     'weapons': 'hooves', 'armor': 'jack'},
    {'weight': 25, 'hits': (3, 2), 'wounds': '',
     'weapons': 'horns and teeth', 'armor': 'none'},
    {'weight': 50, 'hits': (4, 2), 'wounds': '',
     'weapons': 'thrasher', 'armor': 'none'},
    {'weight': 100, 'hits': (5, 2), 'wounds': '',
     'weapons': 'claws and teeth', 'armor': 'none'},
    {'weight': 200, 'hits': (5, 3), 'wounds': '+1D',
     'weapons': 'teeth', 'armor': 'none'},
    {'weight': 400, 'hits': (6, 3), 'wounds': '+2D',
     'weapons': 'claws', 'armor': 'none'},
    {'weight': 800, 'hits': (7, 3), 'wounds': '+3D',
     'weapons': 'claws', 'armor': 'jack'},
    {'weight': 1600, 'hits': (8, 3), 'wounds': '+4D',
     'weapons': 'thrasher', 'armor': 'none'},
    {'weight': 3200, 'hits': (8, 4), 'wounds': '+5D',
     'weapons': 'claws and teeth', 'armor': '+6'},
    {'weight': '+6', 'hits': '+6', 'wounds': '+6',
     'weapons': '+6', 'armor': '+6'},
    {'weight': 6000, 'hits': (9, 4), 'wounds': 'x2',
     'weapons': 'stinger', 'armor': 'cloth+1'},
    {'weight': 12000, 'hits': (10, 5), 'wounds': 'x2',
     'weapons': 'claws+1 and teeth+1', 'armor': 'mesh'},
    {'weight': 24000, 'hits': (12, 6), 'wounds': 'x3',
     'weapons': 'teeth+1', 'armor': 'cloth'},
    {'weight': 30000, 'hits': (14, 7), 'wounds': 'x4',
     'weapons': 'as blade', 'armor': 'battle+4'},
    {'weight': 36000, 'hits': (15, 7), 'wounds': 'x4',
     'weapons': 'as pike', 'armor': 'reflec'},
    {'weight': 40000, 'hits': (16, 8), 'wounds': 'x5',
     'weapons': 'as broadsword', 'armor': 'ablat'},
    {'weight': 44000, 'hits': (17, 9), 'wounds': 'x6',
     'weapons': 'as body pistol', 'armor': 'battle'}
]


WEAPONS_TABLE = {
    'hands': 1, 'claws': 1, 'teeth': 2, 'horns': 2,
    'hooves': 2, 'stinger': 3, 'thrasher': 2, 'club': 2,
    'as blade': 2, 'as pike': 3, 'as broadsword': 4,
    'as body pistol': 3,
    'hooves and horns': 2, 'hooves and teeth': 2,
    'claws and teeth': 2, 'horns and teeth': 2
}


SUPERTYPE_DM_TABLE = {
    'Carnivore': {'weaponry': +8, 'armor': -1},
    'Omnivore': {'weaponry': +4, 'armor': 0},
    'Herbivore': {'weaponry': -3, 'armor': +2},
    'Scavenger': {'weaponry': 0, 'armor': +1}
}


class Hits(object):
    '''Hits object'''

    def __init__(self, size_roll=None):
        self.unconscious = 0
        self.dead = 0

        if size_roll is not None:
            self.generate(size_roll)

    def generate(self, size_roll=None):
        '''Generate hits'''
        if size_roll:
            size_entry = SIZE_WEAPONRY_TABLE[size_roll - 1]
            LOGGER.debug(
                'table[%d] = %s',
                size_roll, size_entry
            )
            LOGGER.debug(
                'hits = %s/%s',
                size_entry['hits'][0], size_entry['hits'][1]
            )
            self.unconscious = D6.roll(
                size_entry['hits'][0]
            )
            self.dead = D6.roll(
                size_entry['hits'][1]
            )

    def __str__(self):
        return '{}/{}'.format(self.unconscious, self.dead)

    def dict(self):
        '''dict() representation'''
        return {
            'unconscious': self.unconscious,
            'dead': self.dead
        }

    def json(self):
        '''JSON representation'''
        return json.dumps(self.dict(), sort_keys=True)


class Animal(object):
    '''LBB3 animal base class'''

    def __init__(self, terrain_type, uwp=None):
        self.supertype = None
        self.quantity = 1
        self.type = None
        self.weight = 0
        self.hits = Hits()
        self.wounds = None
        self.weapons = None
        self.armor = None
        self.locomotion = ''
        self.planet = None
        self.terrain = None
        self.behaviour = ''

        LOGGER.debug('terrain_type = %s', terrain_type)
        LOGGER.debug('uwp = %s', uwp)
        LOGGER.debug('type(uwp) = %s', type(uwp))
        try:
            assert terrain_type in TERRAIN_TYPES_DM
            self.terrain = terrain_type
        except AssertionError:
            raise ValueError('Invalid terrain type {}'.format(terrain_type))
        if uwp is not None:
            try:
                self.planet = System(uwp=uwp)
            except TypeError:
                raise ValueError('Invalid UWP {}'.format(uwp))

        # self.generate(terrain_type)

    def __str__(self):
        return '{} {} {} kg {} {} {} {} {}'.format(
            self.quantity,
            self.type,
            self.weight,
            self.hits,
            self.armor,
            self.wounds,
            self.weapons,
            self.behaviour
        )

    def dict(self):
        '''dict() representation'''
        doc = {
            'terrain': self.terrain,
            'quantity': self.quantity,
            'type': self.type,
            'weight': self.weight,
            'hits': self.hits.dict(),
            'wounds': self.wounds,
            'weapons': self.weapons,
            'armor': self.armor,
            'behaviour': self.behaviour
        }
        return doc

    def json(self):
        '''JSON representation'''
        return json.dumps(self.dict(), sort_keys=True)

    def generate(self):
        '''Generate animal'''

        self._determine_type()
        self._determine_size_etc()
        self._determine_weapons()
        self._determine_armor()
        self._determine_behaviour()

    def _determine_type(self):
        # Determine type; use type DM from TERRAIN_TYPE_TABLE
        LOGGER.debug(
            'terrain type for %s = %s',
            self.terrain,
            TERRAIN_TYPES_DM[self.terrain]['Terrain']
        )
        LOGGER.debug(
            'DMs for %s = type %s size %s',
            TERRAIN_TYPES_DM[self.terrain]['Terrain'],
            TERRAIN_TYPES_DM[self.terrain]['Type DM'],
            TERRAIN_TYPES_DM[self.terrain]['Size DM']
        )
        die_roll = D6.roll(
            dice=2,
            modifier=TERRAIN_TYPES_DM[self.terrain]['Type DM'],
            floor=0, ceiling=13
        )
        type_entry = ANIMAL_TYPES_TABLE[die_roll][self.supertype]
        self.type = type_entry['type']
        if type_entry['qty'] > 1:
            self.quantity = D6.roll(type_entry['qty'])
            self.type += 's'

    def _determine_size_etc(self):
        '''Determine size-related characteristics'''
        (locomotion, size_dm) = self._determine_special_attributes()
        # Update type
        if locomotion != '':
            self.type = '{} {}'.format(locomotion, self.type)

        # Determine size
        die_roll = D6.roll(
            dice=2,
            modifier=TERRAIN_TYPES_DM[self.terrain]['Size DM'] + size_dm -1,
            floor=1, ceiling=20
        )
        size_entry = SIZE_WEAPONRY_TABLE[die_roll]
        while size_entry['weight'] == '+6':
            die_roll = D6.roll(
                dice=2,
                modifier=TERRAIN_TYPES_DM[self.terrain]['Size DM'] + size_dm + 5,
                floor=1, ceiling=20
            )
            size_entry = SIZE_WEAPONRY_TABLE[die_roll]
        self.weight = size_entry['weight']
        self.hits = Hits(die_roll)
        self.wounds = size_entry['wounds']

    def _determine_weapons(self):
        '''Determine weapons'''
        weapons_dm = SUPERTYPE_DM_TABLE[self.supertype]['weaponry']
        die_roll = D6.roll(
            2,
            weapons_dm -1,
            floor=1, ceiling=20
        )
        size_entry = SIZE_WEAPONRY_TABLE[die_roll]
        while size_entry['weapons'] == '+6':
            die_roll = D6.roll(
                2,
                weapons_dm + 5
            )
            size_entry = SIZE_WEAPONRY_TABLE[die_roll]
        self.weapons = size_entry['weapons']
        '''
        Damage
        - self.wounds holds modifier (None, -nD, +nD, xn)
        - Determine actual wound value from WEAPONS_TABLE, modify
          with self.wounds
        '''
        weapon = self.weapons.replace('+1', '')
        LOGGER.debug('weapon = %s', weapon)
        damage = D6.roll(WEAPONS_TABLE[weapon])
        if self.wounds.startswith('x'):
            damage = damage * int(self.wounds[1])
        elif self.wounds.startswith('+'):
            damage += D6.roll(int(self.wounds[1]))
        elif self.wounds.startswith('-'):
            damage -= D6.roll(int(self.wounds[1]))
        damage = max(damage, 1)     # Do at least 1 point of damage
        self.wounds = damage

    def _determine_armor(self):
        '''Determine armor'''
        die_roll = D6.roll(
            2,
            SUPERTYPE_DM_TABLE[self.supertype]['armor'] - 1,
            floor=1, ceiling=20
        )
        size_entry = SIZE_WEAPONRY_TABLE[die_roll]['armor']
        while size_entry == '+6':
            die_roll = D6.roll(
                2,
                SUPERTYPE_DM_TABLE[self.supertype]['armor'] + 5,
                floor=1, ceiling=20
            )
            size_entry = SIZE_WEAPONRY_TABLE[die_roll]['armor']
        self.armor = size_entry
        if self.type.startswith('Flying') or \
                self.type.startswith('Triphibian'):
            self.armor = 'none'

    def _determine_behaviour(self):
        '''Determine behaviour - dummy (handled in subclasses)'''
        pass

    def _determine_special_attributes(self):
        '''Determine special attributes, size DM'''
        LOGGER.debug('planet = %s', self.planet)
        terrain_lookup = TERRAIN_TYPES_DM[self.terrain]['Terrain']
        die_mod = 0
        if self.planet is not None:
            if int(self.planet.size) >= 9:
                die_mod -= 1
            elif int(self.planet.size) >= 4 and int(self.planet.size) <= 5:
                die_mod += 1
            elif int(self.planet.size) <= 3:
                die_mod += 2
            if int(self.planet.atmosphere) >= 8:
                die_mod += 1
            elif int(self.planet.atmosphere) <= 5:
                die_mod -= 1
        return ANIMAL_ATTRIBUTE_TABLE[
            D6.roll(2, die_mod, floor=2, ceiling=12) -2
        ][terrain_lookup]


class Herbivore(Animal):
    '''Herbivore'''

    def __init__(self, terrain_type, uwp=None):
        super().__init__(terrain_type, uwp)
        self.supertype = 'Herbivore'
        self.generate()

    def _determine_behaviour(self):
        '''Determine behaviour'''
        if 'Filter' in self.type:
            attack = 0
            flee = D6.roll(1, 2)
            speed = D6.roll(1, -5, floor=0)
        elif 'Intermittent' in self.type:
            attack = D6.roll(1, 3)
            flee = D6.roll(1, 3)
            speed = D6.roll(1, -2, floor=1)
        elif 'Grazer' in self.type:
            attack = D6.roll(1, 2)
            flee = D6.roll(1)
            speed = D6.roll(1, -2, floor=2)

        self.behaviour = 'F{} A{} S{}'.format(
            flee, attack, speed
        )


class Omnivore(Animal):
    '''Omnivore'''

    def __init__(self, terrain_type, uwp=None):
        super().__init__(terrain_type, uwp)
        self.supertype = 'Omnivore'
        self.generate()

    def _determine_behaviour(self):
        '''Determine behaviour'''
        if 'Gatherer' in self.type:
            attack = D6.roll(1, +3)
            flee = D6.roll(1, +2)
            speed = D6.roll(1, -3, floor=1)
        elif 'Hunter' in self.type:
            attack = D6.roll(1)
            flee = D6.roll(1, +2)
            speed = D6.roll(1, -4, floor=1)
        elif 'Eater' in self.type:
            attack = D6.roll(1)
            flee = D6.roll(1, +3)
            speed = D6.roll(1, -3, floor=1)

        self.behaviour = 'A{} F{} S{}'.format(
            attack, flee, speed
        )


class Carnivore(Animal):
    '''Carnivore'''

    def __init__(self, terrain_type, uwp=None):
        super().__init__(terrain_type, uwp)
        self.supertype = 'Carnivore'
        self.generate()

    def _determine_behaviour(self):
        '''Determine behaviour'''
        if 'Pouncer' in self.type:
            attack = 0
            flee = 0
            speed = D6.roll(1, -2, floor=1)
        elif 'Chaser' in self.type:
            attack = 0
            flee = D6.roll(1, +3)
            speed = D6.roll(1, -2, floor=1)
        elif 'Trapper' in self.type:
            attack = 0
            flee = D6.roll(1, +2)
            speed = D6.roll(1, -5, floor=0)
        elif 'Siren' in self.type:
            attack = 0
            flee = D6.roll(1, +3)
            speed = D6.roll(1, -4, floor=0)
        elif 'Killer' in self.type:
            attack = D6.roll(1)
            flee = D6.roll(1, +3)
            speed = D6.roll(1, -3, floor=1)

        self.behaviour = 'A{} F{} S{}'.format(
            attack, flee, speed
        )


class Scavenger(Animal):
    '''Scavenger'''

    def __init__(self, terrain_type, uwp=None):

        super().__init__(terrain_type, uwp)
        self.supertype = 'Scavenger'
        self.generate()

    def _determine_behaviour(self):
        '''Determine behaviour'''
        if 'Hijacker' in self.type:
            attack = D6.roll(1, +1)
            flee = D6.roll(1, +2)
            speed = D6.roll(1, -4, floor=1)
        elif 'Intimidator' in self.type:
            attack = D6.roll(1, +2)
            flee = D6.roll(1, +1)
            speed = D6.roll(1, -2, floor=1)
        elif 'Carrion-eater' in self.type:
            attack = D6.roll(1, +3)
            flee = D6.roll(1, +2)
            speed = D6.roll(1, -3, floor=0)
        elif 'Reducer' in self.type:
            attack = D6.roll(1, +3)
            flee = D6.roll(1, +2)
            speed = D6.roll(1, -3, floor=0)

        self.behaviour = 'A{} F{} S{}'.format(
            attack, flee, speed
        )
