'''orbit.py'''

import os
import logging
import json
from math import atan2, pi
import requests
import falcon
from .db import Schemas
from ... import DB
from ... import Config

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

KONFIG = Config()
config = KONFIG.config['traveller_api.ct.lbb6']


class Orbit(object):
    '''Orbit class'''

    def __init__(self):
        self.clear_data()
        # Path
        sqlite_file = '{}/{}'.format(
            os.path.dirname(os.path.realpath(__file__)),
            config.get('dbfile'))
        self.db = DB(sqlite_file)
        self.session = self.db.session()

    def on_get(self, req, resp, code, orbit_no):
        '''GET /ct/lbb6/star/<code>/<star>/orbit/<orbit>'''
        LOGGER.debug('orbit_no = %s', orbit_no)
        LOGGER.debug('type(orbit_no) = %s', type(orbit_no))
        self.clear_data()
        self.get_star(code)
        LOGGER.debug('star = %s', self.star)
        if self.star is not None:
            self.get_radius(orbit_no)
            self.determine_period()
            self.determine_angular_diameter()
            if self.orbit_no is None:
                resp.body = json.dumps({
                    'message': 'Invalid orbit number'
                })
                resp.status = falcon.HTTP_400
            else:
                doc = {
                    'angular_dia_deg': self.angular_dia_deg,
                    'angular_dia_sun': self.angular_dia_sun,
                    'au': self.au,
                    'mkm': self.mkm,
                    'period': self.period
                }
                resp.body = json.dumps(doc)
                resp.status = falcon.HTTP_200
        else:
            resp.body = json.dumps({
                'message': 'Invalid star classification'
            })
            resp.status = falcon.HTTP_400

    def clear_data(self):
        '''Clear data on new request'''
        self.star = None
        self.orbit_no = None
        self.au = 0
        self.mkm = 0
        self.period = 0
        self.angular_dia_deg = 0
        self.angular_dia_sun = 0

    def get_star(self, code):
        '''Get star details'''
        LOGGER.debug('Querying API endpoint for star type %s', code)
        resp = requests.get(
            'http://localhost:8000/ct/lbb6/star/{}'.format(code))
        LOGGER.debug('Done, response status = %s', resp.status_code)
        LOGGER.debug('resp.json() = %s', resp.json())
        if resp.status_code == 200:
            self.star = resp.json()

    def determine_period(self):
        '''Determine orbital period - need orbit radius, stellar mass'''
        LOGGER.debug('orbit_no = %s', self.orbit_no)
        if 'mass' in self.star and self.orbit_no is not None:
            self.period = round((self.au ** 3 / self.star['mass']) ** 0.5, 3)
            LOGGER.debug('period = %s', self.period)

    def determine_angular_diameter(self):
        '''Determine angular diameter of star as seen from this orbit'''
        # a = 2*arctan(Dstellar / (2 * R))
        # Convert from solar dia to Mkm (Dsun = 1.3914 Mkm)
        if 'mass' in self.star and self.orbit_no is not None:
            stellar_dia = self.star['radius'] * 1.3914
            LOGGER.debug('stellar dia = %s Mkm', stellar_dia)
            LOGGER.debug('orbital rad = %s Mkm', self.mkm)
            self.angular_dia_deg = round(
                atan2(stellar_dia, self.mkm) * 180 / pi,
                3)
            # Sun's angular diameter from earth orbit ~ 0.522 deg
            self.angular_dia_sun = round(self.angular_dia_deg / 0.522, 3)
            LOGGER.debug(
                'angular dia = %s degrees (%sx the sun from earth)',
                self.angular_dia_deg,
                self.angular_dia_sun)

    def get_radius(self, orbit_no):
        '''Get orbit radius from OrbitTable'''
        if 'mass' in self.star and orbit_no is not None:
            details = self.session.query(Schemas.OrbitTable).\
                filter_by(indx=orbit_no).\
                first()

            LOGGER.debug('orbit details = %s', details)
            if details:
                self.orbit_no = orbit_no
                self.au = details.au
                self.mkm = details.mkm
                # Tag infeasible orbits
                LOGGER.debug('type(orbit_no) = %s', type(orbit_no))
                LOGGER.debug(
                    'type(star["min_orbit"] = %s',
                    type(self.star['min_orbit']))
                if orbit_no <= self.star['min_orbit']:
                    self.orbit_no = '{0} (orbit too close to star)'.format(
                        orbit_no)
                if self.star['int_orbit'] is not None:
                    LOGGER.debug('Star has potential internal orbits')
                    if orbit_no <= self.star['int_orbit']:
                        self.orbit_no = '{0} (orbit within star)'.format(
                            orbit_no)
