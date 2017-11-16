'''planet.py'''

import logging
import re
from random import seed, randint
from ehex.ehex import ehex

LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.ERROR)


class Planet(object):
    '''Planet class'''
    def __init__(self, uwp, orbit=None, star=None):
        seed()
        self.uwp = None
        self.starport = None
        self.size = None
        self.atmosphere = None
        self.hydrographics = None
        self.population = None
        self.government = None
        self.lawlevel = None
        self.techlevel = None
        self.trade_classifications = []
        self.cloudiness = None
        self.albedo = {}
        self.temperature = {}
        self.orbit = orbit
        self.star = star

        for field in ['min', 'max']:
            self.albedo[field] = None
            self.temperature[field] = None

        self.process_uwp(uwp)
        self.determine_trade_classifications()
        self.determine_cloudiness()
        self.determine_albedo()
        self.determine_temperature()

    def process_uwp(self, uwp):
        '''Process UWP, populate variables'''
        re_uwp = r'([A-HYX])([0-9AS])([0-9A-F])([0-9A])([0-9A])' +\
            r'([0-9A-F])([0-9A-HJ-NP-Z)])\-([0-9A-HJ-NP-Z)])'
        if uwp:
            mtch = re.match(re_uwp, str(uwp))
            if mtch:
                self.uwp = uwp
                self.starport = mtch.group(1)
                self.size = ehex(mtch.group(2))
                self.atmosphere = ehex(mtch.group(3))
                self.hydrographics = ehex(mtch.group(4))
                self.population = ehex(mtch.group(5))
                self.government = ehex(mtch.group(6))
                self.lawlevel = ehex(mtch.group(7))
                self.techlevel = ehex(mtch.group(8))

    def determine_trade_classifications(self):
        '''Determine trade classifications'''
        LOGGER.debug('uwp = %s', self.uwp)
        if self.uwp:
            trade_classifications = []
            # Agricultural - Ag
            if (str(self.atmosphere) in '56789' and
                    str(self.hydrographics) in '45678' and
                    str(self.population) in '567'):
                LOGGER.debug('Adding trade classification Ag')
                trade_classifications.append('Ag')
            # Non-agricultural - Na
            if (str(self.atmosphere) in '0123' and
                    str(self.hydrographics) in '0123' and
                    self.population >= '6'):
                LOGGER.debug('Adding trade classification Na')
                trade_classifications.append('Na')
            # Industrial - In
            if (str(self.atmosphere) in '0123479' and
                    self.population >= '9'):
                LOGGER.debug('Adding trade classification In')
                trade_classifications.append('In')
            # Non-industrial - Ni
            if self.population <= '6':
                LOGGER.debug('Adding trade classification Ni')
                trade_classifications.append('Ni')
            # Rich - Ri
            if (str(self.atmosphere) in '68' and
                    str(self.population) in '678' and
                    str(self.government) in '456789'):
                LOGGER.debug('Adding trade classification Ri')
                trade_classifications.append('Ri')
            # Poor - Po
            if (str(self.atmosphere) in '2345' and
                    str(self.hydrographics) in '0123'):
                LOGGER.debug('Adding trade classification Po')
                trade_classifications.append('Po')
            # Water world - Wa
            if self.hydrographics == 'A':
                LOGGER.debug('Adding trade classification Wa')
                trade_classifications.append('Wa')
            # Desert world - De
            if (self.hydrographics == '0' and
                    self.atmosphere >= '2'):
                LOGGER.debug('Adding trade classification De')
                trade_classifications.append('De')
            # Vacuum world - Va
            if self.atmosphere == '0':
                LOGGER.debug('Adding trade classification Va')
                trade_classifications.append('Va')
            # Asteroid belt - As
            if self.size == 0:
                LOGGER.debug('Adding trade classification As')
                trade_classifications.append('As')
            # Ice-capped - Ic
            if (str(self.atmosphere) in '01' and
                    str(self.hydrographics) in '123456789A'):
                LOGGER.debug('Adding trade classification Ic')
                trade_classifications.append('Ic')

            trade_classifications.sort()
            self.trade_classifications = trade_classifications

    def determine_cloudiness(self):
        '''Determine cloudiness'''
        if self.uwp:
            if str(self.hydrographics) in '01':
                self.cloudiness = 0.0
            elif str(self.hydrographics) in '23':
                self.cloudiness = 0.1
            elif str(self.hydrographics) == '4':
                self.cloudiness = 0.2
            elif str(self.hydrographics) == '5':
                self.cloudiness = 0.3
            elif str(self.hydrographics) == '6':
                self.cloudiness = 0.4
            elif str(self.hydrographics) == '7':
                self.cloudiness = 0.5
            elif str(self.hydrographics) == '8':
                self.cloudiness = 0.6
            elif str(self.hydrographics) in '9A':
                self.cloudiness = 0.7
            # Atmosphere effects
            if self.atmosphere >= 'A':
                self.cloudiness = min(
                    1.0,
                    self.cloudiness + 0.4)
            if self.atmosphere <= '3':
                LOGGER.debug(
                    'Atm 3-: setting cloudiness to min(0.2, %s)',
                    self.cloudiness)
                self.cloudiness = min(0.2, self.cloudiness)
                LOGGER.debug('cloudiness = %s', self.cloudiness)
            if self.atmosphere == 'E':
                self.cloudiness = self.cloudiness / 2.0
            LOGGER.debug('cloudiness = %s', self.cloudiness)

    def determine_albedo(self):
        '''Determine albedo'''
        if self.uwp:
            # Desert (De) => hyd == 0 => no clouds
            if 'De' in self.trade_classifications:
                self.albedo['min'] = 0.2
                self.albedo['max'] = 0.2
            # Ice-capped (Ic) => hyd = dirty ice, remainder is rock
            # Ignore clouds - atm  == 0 or 1
            elif 'Ic' in self.trade_classifications:
                # Ice component
                albedo = (int(self.hydrographics) / 100.0) * 0.55
                # Rock component
                albedo += (1.0 - int(self.hydrographics) / 100.0) * 0.2
                self.albedo['min'] = round(albedo, 3)
                self.albedo['max'] = round(albedo, 3)
            else:
                '''
                Other worlds - use min-max approach
                Cloudiness % = albedo for clouds = 0.4 - 0.8
                Ice cap % = 5% - 10%, albedo = 0.85
                Water = hydrograpics, albedo = 0.02
                Land = 1 - hydrographics %, albedo = 0.1 - 0.2

                Minimum albedo =
                    %cloud * 0.4 +
                    (1 - %cloud) * (
                        %ice * 0.85 +
                        (1 - %ice) * (
                            %water * 0.02 +
                            (1 - %water) * 0.1
                        )
                    )
                '''
                self.albedo['min'] = round(
                    self.cloudiness * 0.4 + (1 - self.cloudiness) * (
                        0.05 * 0.85 +
                        0.95 * (
                            int(self.hydrographics) / 100.0 * 0.02 +
                            (1 - int(self.hydrographics) / 100.0) * 0.1
                        )),
                    3)
                '''
                Maximum albedo =
                    %cloud * 0.8 +
                    (1 - %cloud) * (
                        %ice * 0.85 +
                        (1 - %ice) * (
                            %water * 0.02 +
                            (1 - %water) * 0.2
                        )
                    )
                '''
                self.albedo['max'] = round(
                    self.cloudiness * 0.8 + (1 - self.cloudiness) * (
                        0.10 * 0.85 +
                        0.90 * (
                            int(self.hydrographics) / 100 * 0.02 +
                            (1 - int(self.hydrographics) / 100) * 0.2
                        )),
                    3)
            LOGGER.debug(
                'Albedo (min, max) = (%s, %s)',
                self.albedo['min'],
                self.albedo['max'])

    def determine_temperature(self):
        '''Determine temperature'''
        if self.uwp and self.orbit and self.star:
            greenhouse = self._determine_greenhouse_effect()
            LOGGER.debug('Greenhouse effect = %s', greenhouse)
            self.temperature['max'] = round(
                374.025 * greenhouse *
                (1 - self.albedo['min']) *
                self.star.luminosity ** 0.25 / self.orbit.au ** 0.5,
                3)
            self.temperature['min'] = round(
                374.025 * greenhouse *
                (1 - self.albedo['max']) *
                self.star.luminosity ** 0.25 / self.orbit.au ** 0.5,
                3)
            LOGGER.debug(
                'temperature = (%s, %s)',
                self.temperature['min'],
                self.temperature['max'])

    def _determine_greenhouse_effect(self):
        '''Determine greenhouse effect'''
        if str(self.atmosphere) in '0123F':
            return 1.0
        if str(self.atmosphere) in '45':
            return 1.05
        if str(self.atmosphere) in '67E':
            return 1.1
        if str(self.atmosphere) in '89D':
            return 1.15
        if str(self.atmosphere) == 'A':
            return 1.0 + (randint(1, 6) + 1) / 10.0
        if str(self.atmosphere) in 'BC':
            return 1.0 + (randint(1, 6) + randint(1, 6)) / 10.0
