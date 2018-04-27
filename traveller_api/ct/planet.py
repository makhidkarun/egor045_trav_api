'''system.py'''

import re
import json
import logging
from ehex import ehex
from traveller_api.ct.util import Die

D6 = Die(6)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class Planet(object):
    '''
    Planet class

    This class includes a _generate_hydrographics() method
    that follows the 1977 LBB3 method (-4 DM for extreme sizes)
    '''

    valid_uwp = re.compile(
        r'^([A-EX])([0-9A-Z])([0-9A-Z])' +
        r'([0-9A-Z])([0-9A-Z])([0-9A-Z])([0-9A-Z])\-?([0-9A-Z])$')

    def __init__(self, name='', uwp=None):
        self.name = name
        self.starport = 'X'
        self.size = ehex()
        self.atmosphere = ehex()
        self.hydrographics = ehex()
        self.population = ehex()
        self.government = ehex()
        self.lawlevel = ehex()
        self.techlevel = ehex()
        self.bases = ''
        self.trade_codes = []
        self.gas_giant = False

        if uwp is not None:
            LOGGER.debug('Loading from UWP %s', uwp)
            self.load_uwp(uwp)

    def __str__(self):
        return '{}{}{}{}{}{}{}-{}'.format(
            self.starport,
            self.size,
            self.atmosphere,
            self.hydrographics,
            self.population,
            self.government,
            self.lawlevel,
            self.techlevel)

    def json(self):
        '''Return JSON representation'''
        doc = {
            'name': self.name,
            'uwp': str(self),
            'trade_codes': self.trade_codes
        }
        return json.dumps(doc)

    def load_uwp(self, uwp):
        '''Load from UWP'''
        LOGGER.debug('uwp = %s', uwp)
        mtch = self.valid_uwp.match(uwp)
        if mtch:
            self.starport = mtch.group(1)
            self.size = ehex(mtch.group(2))
            self.atmosphere = ehex(mtch.group(3))
            self.hydrographics = ehex(mtch.group(4))
            self.population = ehex(mtch.group(5))
            self.government = ehex(mtch.group(6))
            self.lawlevel = ehex(mtch.group(7))
            self.techlevel = ehex(mtch.group(8))
            self._determine_trade_codes()
        else:
            raise TypeError('Invalid UWP {}'.format(uwp))

    def generate(self):
        '''Generate random planet'''
        self.starport = self._generate_starport()
        self.size = ehex(D6.roll(2, -2))
        self._generate_atmosphere()
        self._generate_hydrographics()
        self.population = ehex(D6.roll(2, -2))
        self.government = ehex(D6.roll(2, int(self.population) - 7, 0, 13))
        self.lawlevel = ehex(D6.roll(2, int(self.government) - 7, 0, 9))
        self._generate_techlevel()
        self._determine_trade_codes()

    @staticmethod
    def _generate_starport():
        '''Generate starport'''
        starport = 'X'
        roll = D6.roll(2)
        LOGGER.debug('roll = %s', roll)

        if roll <= 4:
            starport = 'A'
        elif roll >= 5 and roll <= 6:
            starport = 'B'
        elif roll >= 7 and roll <= 8:
            starport = 'C'
        elif roll == 9:
            starport = 'D'
        elif roll >= 10 and roll <= 11:
            starport = 'E'
        return starport

    def _generate_atmosphere(self):
        '''Generate atmosphere'''
        if int(self.size) == 0:
            self.atmosphere = ehex(0)
        else:
            self.atmosphere = ehex(D6.roll(2, int(self.size) - 7, 0, 12))

    def _generate_hydrographics(self):
        '''Generate hydrographics'''
        # Size == 0 => hyd = 0
        # Size 01A => dm = -4
        if int(self.size) == 0:
            self.hydrographics = ehex(0)
        else:
            die_mod = 0
            if str(self.size) in '01A':
                die_mod = -4
            self.hydrographics = ehex(D6.roll(
                2,
                int(self.size) - 7 + die_mod,
                0,
                10))

    def _generate_techlevel(self):
        '''Generate tech level'''
        die_mod = 0
        # Starport
        if self.starport == 'A':
            die_mod += 6
        elif self.starport == 'B':
            die_mod += 4
        elif self.starport == 'C':
            die_mod += 2
        elif self.starport == 'X':
            die_mod -= 4
        # Size
        if int(self.size) <= 1:
            die_mod += 2
        elif int(self.size) <= 4 and int(self.size) >= 2:
            die_mod += 1
        # Atmosphere
        if int(self.atmosphere) <= 3 or int(self.atmosphere) >= 10:
            die_mod += 1
        # Hydrographics
        if int(self.hydrographics) == 9:
            die_mod += 1
        elif int(self.hydrographics) == 10:
            die_mod += 2
        # Population
        if int(self.population) >= 1 and int(self.government) <= 5:
            die_mod += 1
        elif int(self.population) == 9:
            die_mod += 2
        elif int(self.population) == 10:
            die_mod += 4
        # Government
        if str(self.government) in '05':
            die_mod += 1
        elif str(self.government) == 'D':
            die_mod -= 2
        self.techlevel = ehex(D6.roll(1, die_mod, 0))

    def _determine_trade_codes(self):
        '''Determine trade codes'''
        self.trade_codes = []
        # Agricultural
        if (
                str(self.atmosphere) in '456789' and
                str(self.hydrographics) in '45678' and
                str(self.population) in '567'):
            self.trade_codes.append('Ag')
        # Non-agricultural
        if (
                int(self.atmosphere) <= 3 and
                int(self.hydrographics) <= 3 and
                int(self.population) >= 6):
            self.trade_codes.append('Na')
        # Industrial
        if (
                str(self.atmosphere) in '0123479' and
                int(self.population) >= 9):
            self.trade_codes.append('In')
        # Non-industrial
        if int(self.population) <= 6:
            self.trade_codes.append('Ni')
        # Rich
        if (
                str(self.government) in '456789' and
                str(self.atmosphere) in '68' and
                str(self.population) in '678'):
            self.trade_codes.append('Ri')
        # Poor
        if (
                str(self.atmosphere) in '2345' and
                int(self.hydrographics) <= 3):
            self.trade_codes.append('Po')
        LOGGER.debug('trade codes = %s', self.trade_codes)
