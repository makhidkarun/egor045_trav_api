'''angdia.py'''

from math import atan2, pi
import falcon
import json


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
