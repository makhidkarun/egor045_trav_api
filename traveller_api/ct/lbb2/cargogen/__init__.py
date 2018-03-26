'''ct/lbb2/cargogen/__init__.py'''

import logging
import falcon
from prometheus_client import Histogram
from traveller_api.util import RequestProcessor
from ...lbb3.worldgen.planet import System  # noqa
from .cargo import Cargo, CargoSale
from .... import Config
from ....util import parse_query_string

KONFIG = Config()
config = KONFIG.config['traveller_api.ct.lbb2']

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

REQUEST_TIME = Histogram(
    'ct_lbb2_cargogen_request_latency_seconds',
    'ct_lbb2_cargogen latency')


class Purchase(RequestProcessor):
    '''
    Return CT LBB2 cargo object
    GET <apiserver>/ct/lbb2/cargogen/purchase?<options>

    Options:
    - source_uwp: UWP of source world
    - source_tc: Trade classification of source world (may be repeated)
    - population: Population of source world

    If source_uwp is specified, trade codes and population from that UWP take
    precedence over any source_tc or population specified as options.source_uwp

    Examples:
    - GET <apiserver>/ct/lbb2/cargogen/purchase?source_uwp=C776989-A
    - GET <apiserver>/ct/lbb2/cargogen/purchase?source_tc=In&source_tc=Ri&population=9

    Returns
    {
        "actual_lot_price": <actual lot price>,
        "actual_unit_price": <actual unit price>,
        "base_price": <base price>,
        "id": <cargo id>,
        "name": <cargo description>,
        "purchase_dms": {
            <trade classificaton>: <purchase DM>, ...
        },
        "quantity": <lot size>,
        "resale_dms": {
            <trade classification>: <resale DM>, ...
        },
        "trade_codes": [
            <trade classification>, ....
        ]
    }

    where
    - <actual lot price> is <actual unit price> * <lot size>
    - <actual unit price> is <base price> modifief by actual value roll
        (using purchase DMs)
    - <base price> is base unit price of cargo
    - <id> (string) is ID of randomly-selected cargo
    - <cargo description> is the name/description of the selected cargo
    - <trade classification> is one of the standard Traveller trade codes
    - <purchase DM> is the cargo's purchase DM for the specified trade code
    - <resale DM> is the cargo's resale DM for the specified trade code
    '''

    @REQUEST_TIME.time()
    def on_get(self, req, resp):
        '''GET <apiserver>/ct/lbb2/cargogen/purchase?<options>'''
        self.query_parameters = {
            'source_uwp': None,
            'source_tc': [],
            'population': None,
            'doc': False
        }
        LOGGER.debug('query_string = %s', req.query_string)

        self.parse_query_string(req.query_string)
        if self.query_parameters['doc'] is True:
            resp.body = self.get_doc_json(req)
            resp.status = falcon.HTTP_200
        else:
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
                    'Using source_uwp %s',
                    self.query_parameters['source_uwp'])
                try:
                    planet = System(uwp=self.query_parameters['source_uwp'])
                except TypeError as err:
                    raise falcon.HTTPError(
                        title='Invalid UWP',
                        status='400 Invalid UWP',
                        description=str(err))
                trade_codes = planet.trade_codes
                self.query_parameters['population'] = planet.population
            LOGGER.debug('trade codes = %s', trade_codes)
            LOGGER.debug(
                'population = %s',
                self.query_parameters['population'])
            cargo = Cargo(trade_codes, self.query_parameters['population'])

            resp.body = cargo.json()
        resp.status = falcon.HTTP_200

    """def parse_query_string(self, query_string):
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
                        description='Unknown parameter {}'.format(param))"""


class Sale(RequestProcessor):
    '''
    Return CT LBB2 cargo sale object
    GET <apiserver>/ct/lbb2/cargogen/sale?<options>

    Options:
    - cargo: cargo ID (from table) or description (from table)
    - market_uwp: UWP of market world
    - market_tc: Trade classification of market world (may be repeated)
    - admin: Admin skill available for sale (optional)
    - bribery: Bribery skill available for sale (optional)
    - broker: Broker skill available for sale (optional)
    - quantity: Lot size

    If market_uwp is specified, trade codes from that UWP take
    precedence over any market_tc specified as options.

    Examples:
    - GET <apiserver>/ct/lbb2/cargogen/sale?cargp=64&quantity=10
    - GET <apiserver>/ct/lbb2/cargogen/sale?cargp=64&quantity=10&market_tc=In&market_tc=Ri

    Returns
    {
        "actual_gross_lot_price": <gross lot price>,
        "actual_gross_unit_price": <gross unit price>,
        "actual_net_lot_price": <net lot price>,
        "actual_net_unit_price": <net unit price>,
        "admin": <admin skill level>,
        "base_price": <base price>,
        "bribery": <bribery skill level>,
        "broker": <broker skill level>,
        "commission": <broker's commission>,
        "id": <cargo id>,
        "name": <cargo description>,
        "quantity": <lot size>,
        "trade_codes": [ <trade classification>, ...]
    }

    where
    - <gross lot price> is <gross unit price> * <lot size>
    - <gross unit price> is <base price> modified by actual value table roll
        and market world trade classifications
    - <net lot price> is <gross lot price> less broker's commission
    - <net unit price> is <gorss unit price> less broker's commission
    - <admin skill level> is Admin skill level used in the sale (supplied in
        options)
    - <bribery skill level> is Bribery skill level used in the sale (supplied
        in options)
    - <broker skill level> is Broker skill level used in the sale (supplied in
        options)
    - <commission> is broker's commission, based on <broker skill level>
    - <id> is cargo ID corresponding to <cargo> (supplied in options)
    - <name> is cargo name/description corresponding to <cargo> (supplied in
        options)
    - <lot size> is <quantity> (supplied in options)
    - <trade classificattion> is market world trade code, either supplied in
        options or derived from market uWP
    '''

    def __init__(self):
        self.query_parameters = {}

    @REQUEST_TIME.time()
    def on_get(self, req, resp):
        '''GET <apiserver>/ct/lbb2/cargogen/sale?<options>'''
        self.query_parameters = {
            'cargo': None,
            'market_uwp': None,
            'market_tc': [],
            'admin': 0,
            'bribery': 0,
            'broker': 0,
            'quantity': 0,
            'doc': False
        }
        LOGGER.debug('query_string = %s', req.query_string)
        self.parse_query_string(req.query_string)
        for param in self.query_parameters:
            LOGGER.debug('param %s = %s', param, self.query_parameters[param])

        if self.query_parameters['doc'] is True:
            resp.body = self.get_doc_json(req)
            resp.status = falcon.HTTP_200
        else:
            try:
                cargo = CargoSale(
                    cargo=self.query_parameters['cargo'],
                    quantity=self.query_parameters['quantity'],
                    admin=self.query_parameters['admin'],
                    bribery=self.query_parameters['bribery'],
                    broker=self.query_parameters['broker'],
                    trade_codes=self.determine_trade_codes())
            except ValueError as err:
                raise falcon.HTTPError(
                    title='Invalid parameter',
                    status='400 Bad Request',
                    description=str(err))
            resp.body = cargo.json()
            resp.status = falcon.HTTP_200

    def determine_trade_codes(self):
        '''Determine trade codes from either market_tc or market_uwp'''
        if self.query_parameters['market_uwp'] is None:
            trade_codes = self.query_parameters['market_tc']
        else:
            planet = System(uwp=self.query_parameters['market_uwp'])
            trade_codes = planet.trade_codes
        return trade_codes
