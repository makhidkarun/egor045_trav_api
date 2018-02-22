'''__init__.py'''

import falcon
import logging
from .orbit import Orbit as CalcOrbit
from prometheus_client import Histogram
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

REQUEST_TIME = Histogram(
    't5_orbit_request_latency_seconds',
    't5_orbit latency')


class Orbit(object):
    '''
    Return orbit details
    GET /t5/orbit/<orbit_number>

    Returns
    {
        "orbit_number": <orbit_number>,
        "au": <orbit_radius (AU),
        "mkm": <orbit_radius (Mkm)
    }
    <orbit_number> must be in range 0-17.9
    '''

    @REQUEST_TIME.time()
    def on_get(self, req, resp, orbit_number):
        '''GET /t5/orbit/<orbit_number>'''
        try:
            orbit = CalcOrbit(orbit_number)
        except TypeError as err:
            raise falcon.HTTPInvalidParam(
                msg='orbit_number: {}'.format(orbit_number),
                param_name=str(err))
        except ValueError as err:
            raise falcon.HTTPInvalidParam(
                msg='orbit_number: {}'.format(orbit_number),
                param_name=str(err))
        resp.body = orbit.json()
        resp.status = falcon.HTTP_200
