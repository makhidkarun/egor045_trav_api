'''orbit.py'''

# pragma pylint: disable=C0103

import json
import logging
import os
import requests
from traveller_api import DB
from traveller_api.ct.lbb6.db import Schemas
# from ... import Config

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.ERROR)


class Orbit(object):
    '''Orbit class'''

    def __init__(self, orbit_no, star=None):
        self.orbit_no = None
        self.au = None
        self.mkm = None
        self.period = None
        self.angular_diameter = None
        self.star = star
        self.notes = []

        sqlite_file = '{}/{}'.format(
            os.path.dirname(os.path.realpath(__file__)),
            'star.sqlite'
        )
        self.database = DB(sqlite_file)
        self.session = self.database.session()

        try:
            orbit_no = int(orbit_no)
            assert orbit_no in range(0, 20)
        except:
            raise ValueError('Invalid orbit_no {}'.format(orbit_no))

        self.get_details(orbit_no)
        if self.star is not None:
            self.determine_period()
            self.determine_angular_diameter()
            self.determine_interior_orbits()

    def get_details(self, orbit_no):
        '''Get orbital radius (Mkm, AU)'''
        details = self.session.query(Schemas.OrbitTable).\
            filter_by(indx=orbit_no).\
            first()
        if details:
            self.orbit_no = orbit_no
            self.au = details.au
            self.mkm = details.mkm
        else:
            raise ValueError('Unknown orbit {}'.format(orbit_no))

    def determine_period(self):
        '''Determine orbital period'''
        if self.star is not None:
            self.period = round((self.au ** 3 / self.star.mass) ** 0.5, 3)
            LOGGER.debug('period = %s', self.period)

    def determine_angular_diameter(self):
        '''Determine angular diameter'''
        if self.star is not None:
            stellar_diameter = self.star.radius * 1.3914
            req_string = 'http://api.trav.phraction.org/misc/angdia'
            req_string += '?distance={}&diameter={}'.format(
                self.mkm,
                stellar_diameter
            )
            try:
                resp = requests.get(req_string)
                if resp.status_code == 200:
                    self.angular_diameter = resp.json()['ang_dia_deg']
                else:
                    self.notes.append(
                        'Call to http://api.trav.phraction.org/misc/angdia' +\
                        ' returned {}'.format(resp.status_code))
                    LOGGER.error(
                        'Call to API endpoint returned %s', resp.status_code)
            except requests.ConnectionError:
                LOGGER.debug('Unable to connect to API server')
                self.notes.append(
                    'Unable to connect to API endpoint http://api.trav.phraction.org')

    def json(self):
        '''JSON representation'''
        doc = {
            'orbit_no': self.orbit_no,
            'au': self.au,
            'mkm': self.mkm,
            'period': self.period,
            'angular_diameter': self.angular_diameter,
            'notes': self.notes
        }
        if self.star is None:
            doc['star'] = self.star
        else:
            doc['star'] = str(self.star)
        return json.dumps(doc, sort_keys=True)

    def determine_interior_orbits(self):
        '''Determine internal orbits'''
        if self.star is not None:
            # Interior orbit
            if self.star.int_orbit is not None and\
                    self.orbit_no <= self.star.int_orbit:
                self.notes.append(
                    'Orbit {} is within {} star; minimum orbit is {}'.format(
                        self.orbit_no, str(self.star), self.star.min_orbit
                    )
                )
            # Minimum orbit
            elif self.orbit_no < self.star.min_orbit:
                self.notes.append(
                    'Orbit {} is unavailable to {} star; minimum orbit is {}'.format(
                        self.orbit_no, str(self.star), self.star.min_orbit
                    )
                )

    def __str__(self):
        return 'Orbit {:d}: {:.1f} AU, {:.1f} Mkm'.format(
            self.orbit_no,
            self.au,
            self.mkm
        )
