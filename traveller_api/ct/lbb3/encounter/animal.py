'''animal.py'''

import json
import logging
from traveller_api.ct.util import Die
from traveller_api.ct.lbb3.worldgen.planet import System
from traveller_api.ct.lbb3.encounter.tables import TERRAIN_TYPES_DM
from traveller_api.ct.lbb3.encounter.tables import ANIMAL_ATTRIBUTE_TABLE
from traveller_api.ct.lbb3.encounter.tables import ANIMAL_TYPES_TABLE
from traveller_api.ct.lbb3.encounter.tables import SIZE_WEAPONRY_TABLE
from traveller_api.ct.lbb3.encounter.tables import SUPERTYPE_DM_TABLE
from traveller_api.ct.lbb3.encounter.tables import WEAPONS_TABLE

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

D6 = Die(6)


class Hits(object):
    '''Hits object'''

    def __init__(self, size_roll=None):
        self.unconscious = 0
        self.dead = 0

        LOGGER.debug('size_roll = %s', size_roll)
        if size_roll is not None:
            self.generate(size_roll)

    def generate(self, size_roll=None):
        '''Generate hits'''
        if size_roll:
            # table entry = size_roll - 1 (size die roll 1..20, table rows 0..19)
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
            modifier=TERRAIN_TYPES_DM[self.terrain]['Size DM'] + size_dm,
            floor=1, ceiling=20
        )
        size_entry = SIZE_WEAPONRY_TABLE[die_roll - 1]
        while size_entry['weight'] == '+6':
            die_roll = D6.roll(
                dice=2,
                modifier=TERRAIN_TYPES_DM[self.terrain]['Size DM'] + size_dm + 6,
                floor=1, ceiling=20
            )
            size_entry = SIZE_WEAPONRY_TABLE[die_roll - 1]
        LOGGER.debug('size_entry = %s', size_entry)
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
                weapons_dm + 5,
                floor=1, ceiling=20
            )
            LOGGER.debug('die_roll = %d', die_roll)
            size_entry = SIZE_WEAPONRY_TABLE[die_roll - 1]
        LOGGER.debug('size_entry = %s', size_entry)
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
        raise NotImplementedError('Not implemented in base class')

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
