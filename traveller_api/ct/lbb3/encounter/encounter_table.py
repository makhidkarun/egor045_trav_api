'''encounter_table.py'''

import json
import logging
from collections import OrderedDict
from textwrap import wrap
from traveller_api.ct.lbb3.worldgen.planet import System
from traveller_api.ct.lbb3.encounter.animal import Carnivore
from traveller_api.ct.lbb3.encounter.animal import Herbivore
from traveller_api.ct.lbb3.encounter.animal import Omnivore
from traveller_api.ct.lbb3.encounter.animal import Scavenger
from traveller_api.ct.lbb3.encounter.event import Event
from traveller_api.ct.lbb3.encounter.tables import TERRAIN_TYPES_DM

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)


class EncounterTableBase(object):
    '''EncounterTable base class'''

    def __init__(self, terrain, uwp=None):
        self.terrain = None
        self.rows = OrderedDict()
        self.__size = 0
        self.planet = None

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

    def generate(self):
        '''Dummy method'''
        pass

    def __str__(self):
        if self.planet is None:
            uwp = ''
        else:
            uwp = str(self.planet)
        doc = []
        doc.append('{} Terrain {}'.format(self.terrain, uwp))
        doc.append('{:3} {:28} {:6} {:5} {:8}  {}'.format(
            'Die', 'Animal Type', 'Weight', 'Hits', 'Armor', 'Wounds & Weapons'))
        for _ in self.rows:
            if isinstance(self.rows[_], Event):
                doc.append(
                    ' {:2d} {}'.format(
                        int(_),
                        '\n    '.join(wrap(str(self.rows[_]), width=84))
                    )
                )
            else:
                LOGGER.debug('quantity = %s', self.rows[_].quantity)
                # ' {:2d} {:2d} {:23} {:5d} kg {:5} {:8} {:3d} {:13} {:8}'
                doc.append(
                    ' {:2d} {:2d} {:23} {:5} kg {:5} {:8} {:3} {:19} {:8}'.\
                        format(
                            int(_),
                            self.rows[_].quantity,
                            self.rows[_].type,
                            self.rows[_].weight,
                            str(self.rows[_].hits),
                            self.rows[_].armor,
                            self.rows[_].wounds,
                            self.rows[_].weapons,
                            self.rows[_].behaviour
                        )
                )
        return '\n'.join(doc)

    def dict(self):
        '''dict() representation'''
        doc = {
            'uwp': None,
            'terrain': str(self.terrain),
            'rows': []
        }
        for _ in self.rows:
            doc['rows'].append(
                (_, self.rows[_].dict())
            )
        if self.planet is not None:
            doc['uwp'] = str(self.planet)
        return doc

    def json(self):
        '''JSON representation'''
        return json.dumps(self.dict(), sort_keys=True)


class EncounterTable1D(EncounterTableBase):
    '''D6 encounter table'''

    def __init__(self, terrain, uwp=None):
        super().__init__(terrain, uwp)
        self.__size = 6
        self.generate()

    def generate(self):
        '''
        Add 6 rows
        - Scavenger
        - Herbivore x 3
        - Omnivore
        - Carnivore
        '''
        if self.planet is None:
            uwp = None
        else:
            uwp = str(self.planet)
        self.rows['1'] = Scavenger(self.terrain, uwp)
        self.rows['2'] = Herbivore(self.terrain, uwp)
        self.rows['3'] = Herbivore(self.terrain, uwp)
        self.rows['4'] = Herbivore(self.terrain, uwp)
        self.rows['5'] = Omnivore(self.terrain, uwp)
        self.rows['6'] = Carnivore(self.terrain, uwp)


class EncounterTable2D(EncounterTableBase):
    '''2D6 encounter table'''

    def __init__(self, terrain, uwp=None):
        super().__init__(terrain, uwp)
        self.__size = 6
        self.generate()

    def generate(self):
        '''Add 11 rows'''
        if self.planet is None:
            uwp = None
        else:
            uwp = str(self.planet)
        self.rows['2'] = Scavenger(self.terrain, uwp)
        self.rows['3'] = Omnivore(self.terrain, uwp)
        self.rows['4'] = Scavenger(self.terrain, uwp)
        self.rows['5'] = Omnivore(self.terrain, uwp)
        self.rows['6'] = Herbivore(self.terrain, uwp)
        self.rows['7'] = Herbivore(self.terrain, uwp)
        self.rows['8'] = Herbivore(self.terrain, uwp)
        self.rows['9'] = Carnivore(self.terrain, uwp)
        self.rows['10'] = Event(self.terrain, uwp, strict=False)
        self.rows['11'] = Carnivore(self.terrain, uwp)
        self.rows['12'] = Carnivore(self.terrain, uwp)
