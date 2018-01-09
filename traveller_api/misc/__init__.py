'''angdia.py'''

from math import atan2, pi
import falcon
import json
import logging
import os
from .. import Config
from .db import Schemas


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

KONFIG = Config()
config = KONFIG.config['traveller_api.misc']


class AngDia(object):
    '''Angular diameter API'''
    # GET /misc/angdia/<distance>/<diameter>
    # Return ang_dia (deg), ang_dia (rad)

    def on_get(self, req, resp, distance, diameter):
        '''GET /misc/angdia/<distance>/<diameter>'''
        distance = float(distance)
        diameter = float(diameter)
        angdia_deg = round(
            atan2(diameter, distance) * 180 / pi, 3)
        angdia_rad = round(
            atan2(diameter, distance))
        doc = {
            'ang_dia_deg': angdia_deg,
            'ang_dia_rad': angdia_rad
        }
        resp.body = json.dumps(doc)
        resp.status = falcon.HTTP_200


class StarColor(object):
    '''Star color API
    GET /misc/starcolor/<code>
    Return (r, G, B) corresponding to star color'''
    # See star_color.sqlite for RGB

    def __init__(self):
        self.clear_data()
        # Path
        sqlite_file = '{}/{}'.format(
            os.path.dirname(os.path.realpath(__file__)),
            config.get('dbfile'))
        self.db = DB(sqlite_file)
        self.session = self.db.session()

    def on_get(self, req, resp, code):
        '''GET /misc/starcolor/<code>'''

