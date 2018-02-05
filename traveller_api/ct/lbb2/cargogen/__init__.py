'''ct/lbb2/cargogen/__init__.py'''

import falcon
import logging
from ...lbb3.worldgen.planet import System
from .cargo import Cargo, CargoSale
from .... import Config

KONFIG = Config()
config = KONFIG.config['traveller_api.ct.lbb2']

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class Purchase(object):
    '''CT spec trade API - purchase'''
    # GET /ct/lbb2/cargogen/purchase?<options>
    # Return Cargo object

    def on_get(self, req, resp):
        '''GET /ct/lbb2/cargogen/purchase?<options>'''
        self.query_parameters = {
            'source_uwp': None,
            'source_tc': [],
            'population': None
        }
        LOGGER.debug('query_string = %s', req.query_string)
        self.parse_query_string(req.query_string)
        for param in self.query_parameters:
            LOGGER.debug(
                'param %s = %s',
                param,
                self.query_parameters[param])
        if self.query_parameters['source_uwp'] is None:
            LOGGER.debug('Using TCs from source_tc')
            trade_codes = self.query_parameters['source_tc']
        else:
            LOGGER.debug(
                'Using souce_uwp %s',
                self.query_parameters['source_uwp'])
            planet = System(uwp=self.query_parameters['source_uwp'])
            trade_codes = planet.trade_codes
            self.query_parameters['population'] = planet.population
        LOGGER.debug('trade codes = %s', trade_codes)
        LOGGER.debug('population = %s', self.query_parameters['population'])
        cargo = Cargo(trade_codes, self.query_parameters['population'])

        resp.body = cargo.json()
        resp.status = falcon.HTTP_200

    def parse_query_string(self, query_string):
        '''Parse options'''
        # options format: option1=value1&option2=value2 ...'
        if query_string != '':
            options_list = query_string.split('&')
            for option in options_list:
                param, value = option.split('=')
                if param in self.query_parameters:
                    if isinstance(self.query_parameters[param], list):
                        self.query_parameters[param].append(value)
                    else:
                        self.query_parameters[param] = value
                else:
                    raise falcon.HTTPUnprocessableEntity(
                        title='Unprocessable request',
                        description='Unknown parameter {}'.format(param))


class Sale(object):
    '''CT spec trade API -- sale'''
    # GET /ct/lbb2/cargogen/sale?<options>
    # Return CargoSale object

    def on_get(self, req, resp):
        '''GET /ct/lbb2/cargogen/sale?<options>'''
        self.query_parameters = {
            'cargo': None,
            'market_uwp': None,
            'market_tc': [],
            'admin': 0,
            'bribery': 0,
            'broker': 0,
            'quantity': 0
        }
        LOGGER.debug('query_string = %s', req.query_string)
        self.parse_query_string(req.query_string)

        try:
            cargo = CargoSale(
                cargo=self.query_parameters['cargo'],
                quantity=self.query_parameters['quantity'],
                admin=self.query_parameters['admin'],
                bribery=self.query_parameters['bribery'],
                broker=self.query_parameters['broker'],
                trade_codes=self.determine_trade_codes())
        except ValueError as err:
            raise falcon.HTTPInvalidParam(
                msg='query_string: {}'.format(req.query_string),
                param_name=str(err))
        resp.body = cargo.json()
        resp.status = falcon.HTTP_200

    def parse_query_string(self, query_string):
        '''Parse query string'''
        if query_string != '':
            options_list = query_string.split('&')
            for option in options_list:
                param, value = option.split('=')
                if param in self.query_parameters:
                    if isinstance(self.query_parameters[param], list):
                        self.query_parameters[param].append(value)
                    else:
                        self.query_parameters[param] = value
                else:
                    raise falcon.HTTPUnprocessableEntity(
                        title='Unprocessable request',
                        description='Unknown parameter {}'.format(param))

    def determine_trade_codes(self):
        '''Determine trade codes from either market_tc or market_uwp'''
        if self.query_parameters['market_uwp'] is None:
            trade_codes = self.query_parameters['market_tc']
        else:
            planet = System(uwp=self.query_parameters['market_uwp'])
            trade_codes = planet.trade_codes
        return trade_codes
