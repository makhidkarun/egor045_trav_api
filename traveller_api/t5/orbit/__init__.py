'''__init__.py'''

import logging
import falcon
from traveller_api.util import RequestProcessor
from prometheus_client import Histogram
from .orbit import Orbit as CalcOrbit
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

REQUEST_TIME = Histogram(
    't5_orbit_request_latency_seconds',
    't5_orbit latency')


class Orbit(RequestProcessor):
    '''
    Return orbit details
    GET <apiserver>/t5/orbit/<orbit_number>

    Returns
    {
        "orbit_number": <orbit_number>,
        "au": <orbit_radius (AU),
        "mkm": <orbit_radius (Mkm)
    }
    <orbit_number> must be in range 0-17.9

    GET <apiserver>/t5/orbit/doc returns this text
    '''

    @REQUEST_TIME.time()
    def on_get(self, req, resp, orbit_number):
        '''GET /t5/orbit/<orbit_number>'''
        if orbit_number == 'doc':
            resp.body = self.get_doc_json(req)
            resp.status = falcon.HTTP_200
        else:
            try:
                orbit = CalcOrbit(orbit_number)
            except TypeError as err:
                raise falcon.HTTPError(
                    title='Invalid type',
                    status='400 Invalid parameter',
                    description=str(err))
            except ValueError as err:
                raise falcon.HTTPError(
                    title='Value out of range',
                    status='400 Invalid parameter',
                    description=str(err))
            resp.body = orbit.json()
            resp.status = falcon.HTTP_200
