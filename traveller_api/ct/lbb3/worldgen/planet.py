'''planet.py'''

import re
import json
import logging
from ehex import ehex
from ...util import Die     # noqa

D6 = Die(6)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class System(object):
    '''System class'''

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
            'bases': self.bases,
            'trade_codes': self.trade_codes,
            'gas_giant': self.gas_giant
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
            self._generate_bases()
            self._determine_gas_giant()
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
        self._generate_bases()
        self._determine_gas_giant()
        self._determine_trade_codes()

    @staticmethod
    def _generate_starport():
        '''Generate starport'''
        starport = 'X'
        roll = D6.roll(2)

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
        # Atm 01ABC => dm = -4
        if int(self.size) == 0:
            self.hydrographics = ehex(0)
        else:
            die_mod = 0
            if str(self.atmosphere) in '01ABC':
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

    def _generate_bases(self):
        '''Generate bases'''
        # Naval base
        if self.starport in 'AB':
            if D6.roll(2) >= 8:
                self.bases += 'N'
        # Scout base
        if self.starport in 'ABCD':
            die_mod = 0
            if self.starport == 'C':
                die_mod -= 1
            elif self.starport == 'D':
                die_mod -= 2
            elif self.starport == 'A':
                die_mod -= 3
            if D6.roll(2, die_mod) >= 7:
                self.bases += 'S'

    def _determine_gas_giant(self):
        '''Determine gas giant'''
        if D6.roll(2) <= 9:
            self.gas_giant = True

    def _determine_trade_codes(self):
        '''Determine trade codes'''
        self.trade_codes = []
        self._determine_trade_codes_economic()
        self._determine_trade_codes_env()
        LOGGER.debug('trade codes = %s', self.trade_codes)

    def _determine_trade_codes_economic(self):
        '''Determine economic trade codes'''
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

    def _determine_trade_codes_env(self):   # noqa
        '''Determine environment trade codes'''
        # Wa
        if int(self.hydrographics) == 10:
            self.trade_codes.append('Wa')
        # De
        if int(self.hydrographics) == 0:
            self.trade_codes.append('De')
        # Va
        if int(self.atmosphere) == 0:
            self.trade_codes.append('Va')
        # As
        if int(self.size) == 0:
            self.trade_codes.append('As')
        # Ic
        if int(self.atmosphere) <= 1 and int(self.hydrographics) >= 1:
            self.trade_codes.append('Ic')
