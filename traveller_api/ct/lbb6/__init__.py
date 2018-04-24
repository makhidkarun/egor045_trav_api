'''__init__.py'''

import logging
import requests
import falcon
from traveller_api.util import RequestProcessor
from traveller_api.ct.lbb6.planet import LBB6Planet
from traveller_api.ct.lbb6.star import Star as StarData
from traveller_api.ct.lbb6.orbit import Orbit as OrbitData

API_ENDPOINT = 'http://localhost:8000'

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class Star(RequestProcessor):
    '''
    Return world details
    GET <apiserver>/ct/lbb6/star?code=<star>

    Returns
    {
        "classification": <classification>,
        "decimal": <decimal classification>,
        "hz_orbit": <habitable zone orbit>,
        "hz_period": <habitable zone period>,
        "int_orbit": <interior orbit>,
        "luminosity": <luminosity>,
        "magnitude": <magnitude>,
        "mass": <mass>,
        "min_orbit": <minimum orbit>,
        "radius": <radius>,
        "size": <size>,
        "temperature": <temperature>,
        "type": <stellar type>
    }

    where
    - <classification is <type><decimal> <size>
    - <decimal> is a subdivision of type in the range 0-9. Dwarf stars do not have a
      decimal classification; <decimal> is blank for dwarf stars
    - <habitable zone orbit> is the orbit where a habitable world may exist. A null
      value indicates that the star does not have a habitable zone (e.g. most
      dwarf stars). This will be null if there is no habitable zone.
    - <habitable zone period>: the period of a body orbiting the star in the habitable
      zone orbit.
    - <interior orbit> is the largest orbit that is within the sphere of the star.
      This orbit, and any smaller than it, cannot contain planets. <interior orbit>
      will be null if there are no interior orbits.
    - <minimum orbit> is the closest orbit to the star that can contain a planet,
      due to temperature effects. It will be null if all orbits can be occupied by a
      planet.
    - <luminosity>: Stellar luminosity. Luminosity 2 indicates a star that is twice as
      bright as the Sun.
    - <magnitude>: Magnitude across all wavelengths.
    - <mass>: Mass of the star in solar masses.
    - <radius>: Radius of the star in solar radii.
    - <size>: One of Ia, Ib, II, III, IV, V, VI, D
        - Ia, Ib are supergiant stars
        - II, III are giant stars
        - IV is a subgiant star
        - V is main-sequence star
        - VI is a subdwarf
        - D is a white dwarf star
    - <type>: One of O, B, A, F, G, K, M

    GET <apiserver>/ct/lbb6/star?doc=true returns this text
    '''

    def on_get(self, req, resp):
        '''GET <apiserver>/ct/lbb6/star?code=<star>'''
        self.query_parameters = {
            'doc': False,
            'code': None
        }
        self.parse_query_string(req.query_string)

        if self.query_parameters['doc'] is True:
            resp.body = self.get_doc_json(req)
            resp.status = falcon.HTTP_200
        else:
            try:
                star = StarData(self.query_parameters['code'])
            except TypeError as err:
                raise falcon.HTTPError(
                    title='Invalid star',
                    status='400 Invalid parameter',
                    description=str(err))
            resp.body = star.json()
            resp.status = falcon.HTTP_200


class Orbit(RequestProcessor):
    '''
    GET <apiserver>/ct/lbb6/orbit?orbit_no=<orbit>&star=<code>
    {
        "angular_diameter": <angular diameter of star (degrees)>,
        "au": <orbital radius (AU)>,
        "mkm": <orbital radius (Mkm)>,
        "notes": [],
        "orbit_no": <orbit number>,
        "period": <orbital period (years)>,
        "star": <classification>
    }
    <angular diameter of star>, <orbital period> and <star> will be null if
    star is not specified. orbit_no is required

    GET <apiserver>/ct/lbb6/orbit?doc=true returns this text
    '''

    def on_get(self, req, resp):
        '''GET <apiserver>/ct/lbb6/orbit?orbit_no=<orbit>&star=<code>'''
        self.query_parameters = {
            'doc': False,
            'orbit_no': None,
            'star': None
        }
        self.parse_query_string(req.query_string)

        if self.query_parameters['doc'] is True:
            resp.body = self.get_doc_json(req)
            resp.status = falcon.HTTP_200
        else:
            # Anything to do?
            if self.query_parameters['orbit_no'] is None:
                raise falcon.HTTPError(
                    title='Invalid orbit',
                    status='400 Invalid parameter',
                    description='No orbit specified')

            # Star? If yes, retrieve star data into Star object
            if self.query_parameters['star'] is not None:
                try:
                    star = StarData(self.query_parameters['star'])
                except TypeError as err:
                    raise falcon.HTTPError(
                        title='Invalid star',
                        status='400 Invalid parameter',
                        description='Invalid star {}'.format(
                            self.query_parameters['star']))
            else:
                star = None
            try:
                orbit = OrbitData(
                    self.query_parameters['orbit_no'],
                    star
                )
            except ValueError as err:
                raise falcon.HTTPError(
                    title='Invalid orbit',
                    status='400 Invalid parameter',
                    description=str(err))

            resp.body = orbit.json()
            resp.status = falcon.HTTP_200


class Planet(RequestProcessor):
    '''
    GET <apiserver>/ct/lbb6/planet?uwp=<uwp>&<options>

    Options:
    - name=<name>: planet name
    - is_mainworld=<true|false>: plant is mainworld or satellite
    - orbit=<orbit no>: Planet orbits n orbit <orbit no>
    - star=<code>: Planet orbits a star of type <code>

    Returns
    {
        "is_mainworld": <true/false>,
        "name": <name>,
        "orbit": <orbit details>,
        "star": <star classification>,
        "temperature": {"max": <max temp>, "min": <min temp>},
        "temperature_factors": {
            "albedo": {"max": <max albedo>, "min": <min albedo>},
            "cloudiness": <cloudiness>,
            "greenhouse": {"max": <max greenhouse effect> , "min": <greenhouse effect>}
        },
        "trade_codes": [<tc>, <tc>],
        "uwp": "<uwp>"}
    }

    where
    - <orbit details> is a string listing orbit number and radius
    - <star classification is <type><decimal> <size>
    - <temp> is measured in degrees Kelvin
    - <albedo> is the amount of sunlight reflected by the planet
    - <cloudiness> identifies how much of the surface is obscured by clouds
      (range 0.0-1.0)
    - <greenhouse effect> is energy retained due to atmsphere type
    - <tc> is a starndard Traveller trade classification
    - <uwp> is planet's UWP

    GET <apiserver>/ct/lbb6/planet?doc=true returns this text
    '''
    def on_get(self, req, resp):
        '''GET <apiserver>/ct/lbb6/planet?uwp=<uwp>&<<options>>'''
        self.query_parameters = {
            'doc': False,
            'uwp': None,
            'orbit_no': None,
            'star': None,
            'name': None,
            'is_mainworld': True
        }
        self.parse_query_string(req.query_string)
        LOGGER.debug('querystring = %s', req.query_string)
        LOGGER.debug('is_mainworld = %s', self.query_parameters['is_mainworld'])

        if self.query_parameters['doc'] is True:
            resp.body = self.get_doc_json(req)
            resp.status = falcon.HTTP_200
        else:
            # Anything to do?
            if self.query_parameters['uwp'] is None:
                raise falcon.HTTPError(
                    title='Invalid UWP',
                    status='400 Invalid parameter',
                    description='No UWP specified')
            # Star?
            if self.query_parameters['star'] is not None:
                star = self.get_star_details()
            else:
                star = None
            # Orbit?
            if self.query_parameters['orbit_no'] is not None:
                orbit = self.get_orbit_details(star)
            else:
                orbit = None

            try:
                planet = LBB6Planet(
                    uwp=self.query_parameters['uwp'],
                    name=self.query_parameters['name']
                )
                LOGGER.debug(
                    'query_param is_mainworld = %s',
                    self.query_parameters['is_mainworld']
                )
                planet.generate(
                    star=star,
                    orbit=orbit,
                    is_mainworld=self.query_parameters['is_mainworld']
                )
            except ValueError as err:
                raise falcon.HTTPError(
                    title='Invalid planet',
                    status='400 Invalid parameter',
                    description=str(err))

            resp.body = planet.json()
            resp.status = falcon.HTTP_200

    def get_star_details(self):
        '''Get star details'''
        try:
            return StarData(self.query_parameters['star'])
        except TypeError:
            raise falcon.HTTPError(
                title='Invalid star',
                status='400 Invalid parameter',
                description='Invalid star {}'.format(
                    self.query_parameters['star']))

    def get_orbit_details(self, star):
        '''Get orbit details'''
        try:
            orbit = OrbitData(self.query_parameters['orbit_no'], star)
            return orbit
        except ValueError:
            raise falcon.HTTPError(
                title='Invalid orbit',
                status='400 Invalid parameter',
                description='Invalid orbit {}'.format(
                    self.query_parameters['orbit_no']))
