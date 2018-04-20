'''planet.py'''

# pragma pylint: disable=W0221, C0103

import json
import logging
from ehex import ehex
from traveller_api.ct.planet import Planet
from traveller_api.ct.util import Die

D6 = Die(6)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

class EhexSize(ehex):
    '''Extend ehex to account for size S (=0)'''
    def __init__(self, value=0):
        self.is_s = False
        super().__init__(value)
        if self._value == 26:   # S
            self.is_s = True
            self._value = 0

    def __str__(self):
        if self.is_s is True:
            return 'S'
        else:
            return self.valid[self._value]

    def __repr__(self):
        if self.is_s is True:
            return 'S'
        else:
            return self.valid[self._value]

    def __eq__(self, other):
        if isinstance(other, str):
            return self.valid[self._value] == other or (self.is_s and other == 'S')
        elif isinstance(other, int):
            return self._value == other
        elif isinstance(other, ehex):
            return self._value == int(other)
        else:
            raise TypeError(
                '%s %s should be ehex, int or str' % (type(other), other))

    def __ne__(self, other):
        if isinstance(other, str):
            return self.valid[self._value] != other or (self.is_s and other != 'S')
        elif isinstance(other, int):
            return self._value != other
        elif isinstance(other, ehex):
            return self._value != int(other)
        else:
            raise TypeError(
                '%s %s should be ehex, int or str' % (type(other), other))

    def __lt__(self, other):
        if isinstance(other, str):
            return self.valid[self._value] < other or (self.is_s and other < 'S')
        elif isinstance(other, int):
            return self._value < other
        elif isinstance(other, ehex):
            return self._value < int(other)
        else:
            raise TypeError(
                '%s %s should be ehex, int or str' % (type(other), other))

    def __gt__(self, other):
        if isinstance(other, str):
            return self.valid[self._value] > other or (self.is_s and other > 'S')
        elif isinstance(other, int):
            return self._value > other
        elif isinstance(other, ehex):
            return self._value > int(other)
        else:
            raise TypeError(
                '%s %s should be ehex, int or str' % (type(other), other))

    def __le__(self, other):
        if isinstance(other, str):
            return self.valid[self._value] <= other or (self.is_s and other <= 'S')
        elif isinstance(other, int):
            return self._value <= other
        elif isinstance(other, ehex):
            return self._value <= int(other)
        else:
            raise TypeError(
                '%s %s should be ehex, int or str' % (type(other), other))

    def __ge__(self, other):
        if isinstance(other, str):
            return self.valid[self._value] >= other or (self.is_s and other >= 'S')
        elif isinstance(other, int):
            return self._value >= other
        elif isinstance(other, ehex):
            return self._value >= int(other)
        else:
            raise TypeError(
                '%s %s should be ehex, int or str' % (type(other), other))


class LBB6Planet(Planet):
    '''LBB6 planet - extends basic CT planet'''

    def __init__(self, name='', uwp=None):
        super().__init__(name=name, uwp=uwp)
        # Extra properties
        self.is_mainworld = True
        self.star = None
        self.orbit = None

    def generate(self, is_mainworld=True, star=None, orbit=None):
        '''Generate, including star/orbit'''
        self.is_mainworld = is_mainworld
        self.star = star
        self.orbit = orbit
        self._generate_size()
        self._generate_atmosphere()
        self._generate_hydrographics()
        self.population = ehex(D6.roll(2, -2))
        self.government = ehex(D6.roll(2, int(self.population) - 7, 0, 13))
        self.lawlevel = ehex(D6.roll(2, int(self.government) - 7, 0, 9))
        self.starport = self._generate_starport()
        self._generate_techlevel()
        self._determine_trade_codes()
        self._determine_env_trade_codes()

    def _generate_starport(self):
        '''Generate starport'''
        if self.is_mainworld is True:
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
        else:
            die_mod = 0
            if int(self.population) >= 6:
                die_mod += 2
            if int(self.population) == 1:
                die_mod -= 2
            if int(self.population) == 0:
                die_mod -= 3
            roll = D6.roll(1, die_mod)
            if roll <= 2:
                starport = 'Y'
            elif roll == 3:
                starport = 'H'
            elif roll >= 4 and roll <= 5:
                starport = 'G'
            else:
                starport = 'F'
        return starport

    def _generate_size(self):
        '''LBB6 size'''
        die_mod = -2
        if self.orbit is not None:
            if self.orbit.orbit_no == 0:
                die_mod -= 5
            if self.orbit.orbit_no == 1:
                die_mod -= 4
        if self.star is not None:
            if self.star.type == 'M':
                die_mod -= 2
        self.size = EhexSize(D6.roll(2, die_mod, ceiling=12))
        if int(self.size) == 0 and self.is_mainworld is False:
            self.size = EhexSize('S')

    def _generate_atmosphere(self):
        '''
        Generate atmosphere
        2D-7 + size
        Inner zone: DM -2
        Outer zone: DM -2
        Size 0 or S: atm = 0
        Outer zone +2: roll 12 for A (0 otherwise)
        '''
        if int(self.size) == 0:     # 0 or S
            self.atmosphere = ehex(0)
            return
        die_mod = 0
        if self.star is not None and self.orbit is not None:
            if self.orbit.orbit_no < self.star.hz_orbit:
                die_mod -= 2
            if self.orbit.orbit_no > self.star.hz_orbit:
                die_mod -= 2
            if self.orbit.orbit_no - self.star.hz_orbit >= 2:
                if D6.roll(2) == 12:
                    self.atmosphere = ehex('A')
                else:
                    self.atmosphere = ehex(0)
                return
        self.atmosphere = D6.roll(2, die_mod, ceiling=12)

    def _generate_hydrographics(self):
        '''
        LBB6 hydrographics
        2D-7 + size
        * Inner zone: hyd = 0
        * Outer zone: DM -4
        * Size 1- or S: hyd = 0
        * Atmosphere 1- or A+: DM -4
        '''
        # Orbit-related
        die_mod = 0
        if self.star is not None and self.orbit is not None:
            if self.orbit.orbit_no < self.star.hz_orbit:
                self.hydrographics = ehex(0)
                return
            if self.orbit.orbit_no > self.star.hz_orbit:
                die_mod -= 4

        # Size-related
        if int(self.size) <= 1:
            self.hydrographics = ehex(0)
            return

        # Atmosphere-related
        if str(self.atmosphere) in '01ABCDEF':
            die_mod -= 4

        self.hydrographics = ehex(
            D6.roll(2, int(self.size) - 7 + die_mod, 0, 10)
        )

    def json(self):
        '''Return JSON representation'''
        doc = {
            'name': self.name,
            'uwp': str(self),
            'trade_codes': self.trade_codes,
            'is_mainworld': self.is_mainworld,
            'star': str(self.star),
            'orbit': str(self.orbit)
        }
        return json.dumps(doc, sort_keys=True)

    def _determine_env_trade_codes(self):
        '''Generate environmental trade codes Wa, De, Va, As, Ic'''
        # Wa
        if str(self.hydrographics) == 'A':
            self.trade_codes.append('Wa')
        # De
        if str(self.hydrographics) == '0' and \
                int(self.atmosphere) <= 2:
            self.trade_codes.append('De')
        # Va
        if int(self.atmosphere) == 0:
            self.trade_codes.append('Va')
        # As
        if int(self.size) == 0 and self.is_mainworld:
            self.trade_codes.append('As')
        # Ic
        if int(self.atmosphere) <= 1 and int(self.hydrographics) >= 1:
            self.trade_codes.append('Ic')
