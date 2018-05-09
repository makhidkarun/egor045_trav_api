'''system.py'''

import logging
from random import randint
from traveller_api.ct.util import Die
from traveller_api.ct.lbb6.planet import LBB6Planet
from traveller_api.ct.lbb6.orbit import Orbit
from traveller_api.ct.lbb6.star import Star

D6 = Die(6)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

STAR_TYPES = [
    'B', 'B', 'A', 'M', 'M', 'M', 'M',
    'M', 'K', 'G', 'F', 'F', 'D'
]
STAR_SIZES = [
    'Ia', 'Ib', 'II', 'III', 'IV', 'V', 'V',
    'V', 'V', 'V', 'V', 'VI', 'D'
]
COMPANION_STAR_TYPES = [
    '-', 'B', 'A', 'F', 'F', 'G', 'G',
    'K', 'K', 'M', 'M', 'M', 'M'
]
COMPANION_STAR_SIZES = [
    'Ia', 'Ib', 'II', 'III', 'IV', 'D', 'D',
    'V', 'V', 'VI', 'D', 'D', 'D'
]
GAS_GIANT_QTY = [0, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5]
PLANETOID_QTY = [3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1]

class LBB6ExpandedSystem(object):
    '''LBB6 expanded system'''

    def __init__(self, name=''):
        self.name = name
        self.star = None
        self.companions = []
        self.worlds = []


class LBB6ExpandedStar(Star):
    '''Extend Star to include orbits etc'''

    def __init__(self, mainworld, code=None):
        self.orbits = []
        self.size_roll = None
        self.type_roll = None
        if code is None:
            code = self.generate(mainworld)
        super().__init__(code)

    def generate(self, mainworld):
        '''Generate code'''
        # DM for habitable worlds
        die_mod = 0
        try:
            if (
                    int(mainworld.atmosphere) in range(4, 10) or
                    int(mainworld.population) >= 8
                ):
                die_mod += 4
        except AttributeError:
            raise ValueError('Invalid mainworld (must be Planet)')
        self.type_roll = D6.roll(2, die_mod, floor=0, ceiling=12)
        self.size_roll = D6.roll(2, die_mod, floor=0, ceiling=12)

        star_size = STAR_SIZES[self.size_roll]
        star_type = STAR_TYPES[self.type_roll]
        star_decimal = randint(0, 9)

        if star_size == 'D':
            code = '{}D'.format(star_size)
        else:
            code = '{}{} {}'.format(star_type, star_decimal, star_size)
        return code
