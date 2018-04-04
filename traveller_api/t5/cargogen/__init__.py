'''__init__.py'''

import json
import re
import logging
import configparser
import falcon
from traveller_api.util import RequestProcessor
from .trade_cargo import TradeCargo

config = configparser.ConfigParser()    # noqa
config.read('t5.ini')
uwp_validator = re.compile(r'[A-HX][0-9A-Z]{6}\-([0-9A-Z])')    # noqa
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def validate_uwps(source_uwp, market_uwp):
    '''Validate UWPs'''
    validity = True
    if not uwp_validator.match(source_uwp):
        validity = False
    if market_uwp is not None:
        if not uwp_validator.match(market_uwp):
            validity = False
    return validity


class CargoGen(RequestProcessor):
    '''
    Return T5 cargo object
    GET <apiserver>/t5/cargogen?source_uwp=<source_uwp>&market_uwp=<dest_uwp>&broker=<broker_skill>

    Returns
    {
        "cargo": "<source TL>-<source TCs> Cr<cost> <description>",
        "cost": <cost>,
        "description": <description>,
        "market": {
            "broker_commission": <broker commission>,
            "gross_actual_value": <actual value>,
            "net_actual_value": <net actual value>,
            "trade_codes": [ <market TC>, <market TC>, ...],
            "uwp": <market UWP>
        },
        "notes": {
            "actual_value_rolls": [
                <av roll1>, <av roll2>],
            "broker_skill": <broker_skill>
        },
        "price": <price>,
        "source": {
            "trade_codes": [ <source TC>, <source TC>, ... ],
            "uwp": <cource UWP>
        },
        "tech_level": <source TL>
    }

    where
    - <source UWP>, <dest UWP> are source world and market world UWPs
      - source_uwp is required
    - <actual value> is the end price
    - <av_roll1>, <av_roll2> are the Flux rolls used to
      determine actual value
    - <cost> is the purchase cost of the cargo
    - <description> is the cargo description
    - <market TC>, <source TC> are market world and source world
      trade codes
    - <source TCs> is the list of source world trade codes
    - <source TL> is the source world's tech level
    - <broker skill> is the broker skill used when selling (default is 0/none)
    - <broker commission> is the commission paid to the broker
    - <actual value> is the end price following actual value roll
    - <net actual value> is the end price minus broker commission

    If broker is not specified, <broker skill> and <broker commission> will be 0.

    If market is not specified:
    - <price>, <actual value> and <net actual value> will be 0
    - <market UWP>, <av roll1>, <av roll2> will be null


    GET <apiserver>/t5/cargogen?doc=true

    Returns this text
    '''

    def on_get(self, req, resp):
        '''
        GET <apiserver>/t5/cargogen?source_uwp=<source_uwp>&market_uwp=<dest_uwp>
        GET <apiserver>/t5/cargogen?source_uwp=<source_uwp>'''

        self.query_parameters = {
            'doc': False,
            'source_uwp': None,
            'market_uwp': None,
            'broker': 0
        }
        self.parse_query_string(req.query_string)

        if self.query_parameters['doc'] is True:
            resp.body = self.get_doc_json(req)
            resp.status = falcon.HTTP_200
        else:
            cargo = TradeCargo()
            LOGGER.debug('broker = %s', self.query_parameters['broker'])
            try:
                cargo.generate_cargo(
                    self.query_parameters['source_uwp'],
                    self.query_parameters['market_uwp'],
                    self.query_parameters['broker']
                )
            except ValueError as err:
                raise falcon.HTTPError(
                    title='Invalid UWP',
                    status='400 Invalid parameter',
                    description=str(err))

            resp.body = cargo.json()
            resp.status = falcon.HTTP_200
