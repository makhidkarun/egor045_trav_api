'''planet.py'''

# pragma pylint: disable=W0221, C0103

import json
import logging
import re
from ehex import ehex
from traveller_api.ct.planet import Planet
from traveller_api.ct.util import Die
from traveller_api.util import MinMax

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

    valid_uwp = re.compile(
        r'^([A-GXY])([0-9AS])([0-9A-F])' +
        r'([0-9A])([0-9A])([0-9A-D])([0-9A-Z])\-?([0-9A-Z])$')


    def __init__(self, name='', uwp=None):
        super().__init__(name=name, uwp=uwp)
        # Extra properties
        self.uwp_provided = False
        if uwp is not None:
            self.uwp_provided = True
        LOGGER.debug('uwp_provided = %s', self.uwp_provided)
        self.is_mainworld = True
        self.star = None
        self.orbit = None
        self.cloudiness = None
        self.greenhouse = MinMax(0, 0)
        self.albedo = MinMax(0, 0)
        self.temperature = MinMax(0, 0)

    def generate(self, is_mainworld=True, star=None, orbit=None):
        '''Generate, including star/orbit'''
        self.is_mainworld = is_mainworld
        self.star = star
        self.orbit = orbit
        if self.uwp_provided is False:
            LOGGER.debug('uwp provided')
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
        self.determine_greenhouse()
        self.determine_cloudiness()
        self.determine_albedo()
        self.determine_temperature_range()

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
            'star': None,
            'orbit': None,
            'temperature_factors': {
                'cloudiness': self.cloudiness,
                'albedo': self.albedo.dict(),
                'greenhouse': self.greenhouse.dict()
            },
            'temperature': self.temperature.dict()
        }
        if self.star is not None:
            doc['star'] = str(self.star)
        if self.orbit is not None:
            doc['orbit'] = str(self.orbit)
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

    def determine_cloudiness(self):
        '''Determine cloudiness (dep hydrographics, atmosphere)'''
        if str(self.hydrographics) in '01':
            self.cloudiness = 0.0
        elif str(self.hydrographics) in '23':
            self.cloudiness = 0.1
        elif str(self.hydrographics) in '9A':
            self.cloudiness = 0.7
        else:
            self.cloudiness = float((int(self.hydrographics) - 2) / 10.0)

        # Atmosphere effects
        if int(self.atmosphere) <= 3:
            self.cloudiness = min(0.2, self.cloudiness)
        if str(self.atmosphere) in 'ABCDEF':
            self.cloudiness += 0.4
            self.cloudiness = min(self.cloudiness, 1.0)
        if str(self.atmosphere) == 'E':
            self.cloudiness = self.cloudiness / 2
        self.cloudiness = round(self.cloudiness, 1)

    def determine_albedo(self):
        '''Determine albedo range'''
        desert_coverage = self._albedo_determine_desert_coverage()
        veg_coverage = 1.0 - desert_coverage
        ice_coverage = self._determine_albedo_ice_coverage()
        LOGGER.debug(
            'desert_coverage = %s veg_coverage = %s ice_coverage = %s',
            desert_coverage, veg_coverage, ice_coverage
        )
        (
            net_land_coverage,
            net_hydro_coverage
        ) = self._determine_net_land_hydro_coverage(ice_coverage)

        LOGGER.debug(
            'net_land_coverage = %s net_hydro_coverage = %s',
            net_land_coverage, net_hydro_coverage
        )

        if self.star is not None and self.orbit is not None:
            if self.orbit.orbit_no > self.star.hz_orbit:
                net_hydro_coverage = 0.0
        non_cloud_albedo = (
            (
                desert_coverage * 0.2 +
                veg_coverage * 0.1
            ) * net_land_coverage +
            net_hydro_coverage * 0.02 +
            ice_coverage * 0.85) * (1.0 - self.cloudiness)

        LOGGER.debug('non_cloud_albedo = %s', non_cloud_albedo)

        self.albedo = MinMax(
            round(self.cloudiness * 0.4 + non_cloud_albedo, 3),
            round(self.cloudiness * 0.8 + non_cloud_albedo, 3)
        )

    def _determine_net_land_hydro_coverage(self, ice_coverage):
        '''
        land_coverage = (1-Hyd)-ice/2
        hydro_coverage = Hyd-ice/2
        '''
        net_land_coverage = float(((10.0 - int(self.hydrographics)) /10.0)) - ice_coverage / 2.0
        net_hydro_coverage = float(int(self.hydrographics) / 10.0) - ice_coverage / 2.0
        return (net_land_coverage, net_hydro_coverage)

    def _determine_albedo_ice_coverage(self):
        '''
        Determine ice cap coverage
        Hyd == 0: no ice cap
        Inner zone: no ice cap
        Habitable zone: ice cap = 10%
        Outer zone: ice cap = hydrographics

        Default (no orbit/star): ice cap = 10%
        '''
        if self.star is not None and self.orbit is not None:
            if self.orbit.orbit_no < self.star.hz_orbit:
                ice_coverage = 0.0
            if self.orbit.orbit_no == self.star.hz_orbit:
                ice_coverage = 0.1
            if self.orbit.orbit_no > self.star.hz_orbit:
                ice_coverage = float(int(self.hydrographics) / 10.0)
        else:
            ice_coverage = 0.1
        # Desert
        if int(self.hydrographics) == 0:
            ice_coverage = 0.0

        return ice_coverage

    def _albedo_determine_desert_coverage(self):
        '''
        Split between desert and forest/field ( == veg)
        Atmosphere <= 2: all desert
        Hyd = 0: all desert (duh)
        Desert percentage reduces as hyd increases
        Desert percentage gets boost as atmosphere is thinner
        '''
        # Assume linear relationship between hydrographics and vegetation
        desert_coverage = float((10 - int(self.hydrographics)) / 10)

        # Vacuum or trace atmosphere => no vegetation
        if str(self.atmosphere) in '01':
            desert_coverage = 1.0
        # Very thin
        if str(self.atmosphere) in '23':
            desert_coverage += 0.1
        if str(self.atmosphere) in '45':
            desert_coverage += 0.05
        if str(self.atmosphere) in '89':
            desert_coverage -= 0.05
        if str(self.hydrographics) == '0':
            desert_coverage = 1.0
        desert_coverage = max(0.0, desert_coverage)
        desert_coverage = min(1.0, desert_coverage)

        return round(desert_coverage, 2)

    def determine_greenhouse(self):
        '''Determine greenhouse effect'''
        if str(self.atmosphere) in '0123F':
            self.greenhouse = MinMax(1.0, 1.0)
        elif str(self.atmosphere) in '45':
            self.greenhouse = MinMax(1.05, 1.05)
        elif str(self.atmosphere) in '67E':
            self.greenhouse = MinMax(1.1, 1.1)
        elif str(self.atmosphere) in '89D':
            self.greenhouse = MinMax(1.15, 1.15)
        elif str(self.atmosphere) == 'A':
            self.greenhouse = MinMax(1.2, 1.7)
        elif str(self.atmosphere) in 'BC':
            self.greenhouse = MinMax(1.2, 2.2)

    def determine_temperature_range(self):
        '''
        Determine temperature range

        Note: take greenhouse.min()/albedo.max() and
        greenhouse.max()/albedo.min(); temperature decreases with
        increasing greenhouse and decreases with increasing albedo
        '''
        if self.star is not None and self.orbit is not None:
            self.temperature = MinMax(
                self._temperature_formula(
                    self.star.luminosity,
                    self.albedo.min(),
                    self.orbit.au,
                    self.greenhouse.max()
                ),
                self._temperature_formula(
                    self.star.luminosity,
                    self.albedo.max(),
                    self.orbit.au,
                    self.greenhouse.min()
                )
            )

    @staticmethod
    def _temperature_formula(
            luminosity,
            albedo,
            distance,
            greenhouse
        ):
        '''Temperature formula'''
        LOGGER.debug(
            'lum %s albedo %s dist %s greenhouse %s',
            luminosity, albedo, distance, greenhouse
        )
        temp = round(
            374.025 * greenhouse *
            (1.0 - albedo) *
            (luminosity ** 0.25) /
            (distance ** 0.5),
            0
        )
        LOGGER.debug('temp = %d', temp)
        return temp
