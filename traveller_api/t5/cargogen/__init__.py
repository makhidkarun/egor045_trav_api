'''__init__.py'''

import json
import configparser
import falcon
import re
import logging
from .trade_cargo import TradeCargo, TradeCargoBroker
from prometheus_client import Histogram

config = configparser.ConfigParser()
config.read('t5.ini')
uwp_validator = re.compile(r'[A-HX][0-9A-Z]{6}\-([0-9A-Z])')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

REQUEST_TIME = Histogram(
    't5_cargogen_request_latency_seconds',
    't5_cargogen latency')


def validate_uwps(source_uwp, market_uwp):
    '''Validate UWPs'''
    validity = True
    if not uwp_validator.match(source_uwp):
        validity = False
    if market_uwp is not None:
        if not uwp_validator.match(market_uwp):
            validity = False
    return validity


class CargoGen(object):
    '''CargoGen'''
    @staticmethod
    @REQUEST_TIME.time()
    def on_get(req, resp, source_uwp, market_uwp=None):
        '''
        Return T5 cargo object
        GET /t5/cargogen/source/<source_uwp>/market/<dest_uwp>'

        Returns
        {
            "actual value": <actual_value>,
            "actual value rolls": [ <av_roll1>, <av_roll2> ],
            "cargo": <source TL>-<source TCs> Cr<cost> <description>
            "cost": <cost>,
            "description": <description>,
            "market": {
                "trade_codes": [ <market TC>, <market TC> ... ],
                "uwp": <market UWP>
            },
            "price": <price>,
            "source": {
                "trade_codes": [ <source TC>, <source TC> ...],
                "uwp": <source UWP>
            },
            "tech level": <source TL>
        }

        GET /t5/cargogen/source/<source_uwp>

        returns
        {
            "cargo": <source TL>-<source TCs> Cr<cost> <description>,
            "cost": <cost>,
            "description": <description>,
            "source": {
                "trade_codes": [ <source TC>, <source TC> ...],
                "uwp": <source UWP>
            },
            "tech level": <source TL>
        }

        where
        - <source UWP>, <market UWP> are source world and market world UWPs
        - <actual value> is the end price
        - <av_roll1>, <av_roll2> are the Flux rolls used to
          determine actual value
        - <cost> is the purchase cost of the cargo
        - <description> is the cargo description
        - <market TC>, <source TC> are market world and source world
          trade codes
        - <source TL> is the source world's tech level
        '''

        if validate_uwps(source_uwp, market_uwp):
            cargo = TradeCargo()
            try:
                cargo.generate_cargo(source_uwp, market_uwp)
            except ValueError:
                if market_uwp is None:
                    error_desc = 'Invalid UWP in {}'.format(source_uwp)
                else:
                    error_desc = 'Invalid UWP in {}, {}'.format(
                        source_uwp, market_uwp)
                raise falcon.HTTPUnprocessableEntity(
                    title='Bad source or market UWP',
                    description=error_desc)
            doc = {
                'source': {
                    'uwp': cargo.source_world.uwp(),
                    'trade_codes': cargo.source_world.trade_codes
                },
                'cargo': str(cargo),
                'cost': cargo.cost,
                'description': cargo.description,
                'tech level': int(cargo.source_world.tech_level)

            }
            resp.body = json.dumps(doc)
            resp.status = falcon.HTTP_200
        else:
            if market_uwp is None:
                doc = {
                    'message': 'Invalid UWP in {}'.format(source_uwp)
                }
            else:
                doc = {
                    'message': 'Invalid UWP in {} {}'.format(
                        source_uwp, market_uwp)
                }
            resp.body = json.dumps(doc)
            resp.status = falcon.HTTP_400

        if market_uwp is not None:
            if uwp_validator.match(market_uwp):
                LOGGER.debug('Market UWP %s valid', market_uwp)
                doc['market'] = {
                    'uwp': cargo.market_world.uwp(),
                    'trade_codes': cargo.market_world.trade_codes
                }
                doc['price'] = cargo.price
                doc['actual value'] = cargo.actual_value
                doc['actual value rolls'] = cargo.actual_value_rolls

                resp.body = json.dumps(doc)
                resp.status = falcon.HTTP_200
            else:
                doc = {
                    'message': 'Invalid market UWP {}'.format(market_uwp)
                }
                resp.body = json.dumps(doc)
                resp.status = falcon.HTTP_400


class BrokerGen(object):
    '''CargoGen'''
    @staticmethod
    @REQUEST_TIME.time()
    def on_get(req, resp, source_uwp, market_uwp=None, broker_skill=None):
        '''
        Return T5 cargo object
        GET /t5/cargogen/source/<source_uwp>/market/<dest_uwp>/broker/<skill>'

        Returns
        {
            "actual value": <actual_value>,
            "actual value rolls": [ <av_roll1>, <av_roll2> ],
        "broker": {
            "commission": <commission>,
            "skill": <skill>
        },

            "cargo": <source TL>-<source TCs> Cr<cost> <description>
            "cost": <cost>,
            "description": <description>,
            "market": {
                "trade_codes": [ <market TC>, <market TC> ... ],
                "uwp": <market UWP>
            },
            "price": <price>,
            "source": {
                "trade_codes": [ <source TC>, <source TC> ...],
                "uwp": <source UWP>
            },
            "tech level": <source TL>
        }

        where
        - <source UWP>, <market UWP> are source world and market world UWPs
        - <actual value> is the gross end price (does not include commission)
        - <av_roll1>, <av_roll2> are the Flux rolls used to
          determine actual value
        - <cost> is the purchase cost of the cargo
        - <description> is the cargo description
        - <market TC>, <source TC> are market world and source world
          trade codes
        - <source TL> is the source world's tech level
        - <skill> is the broker's skill
        - <commission> is the broker's commission
        '''

        cargo = TradeCargoBroker()
        try:
            cargo.generate_cargo(source_uwp, market_uwp, broker_skill)
        except ValueError:
                if market_uwp is None:
                    error_desc = 'Invalid UWP in {}'.format(source_uwp)
                else:
                    error_desc = 'Invalid UWP in {}, {}'.format(
                        source_uwp, market_uwp)
                raise falcon.HTTPUnprocessableEntity(
                    title='Bad source or market UWP',
                    description=error_desc)
        doc = {
            'source': {
                'uwp': cargo.source_world.uwp(),
                'trade_codes': cargo.source_world.trade_codes
            },
            'cargo': str(cargo),
            'cost': cargo.cost,
            'description': cargo.description,
            'tech level': int(cargo.source_world.tech_level)

        }
        if cargo.market_world is not None:
            doc['market'] = {
                'uwp': cargo.market_world.uwp(),
                'trade_codes': cargo.market_world.trade_codes
            }
            doc['price'] = cargo.price
            doc['actual value'] = cargo.actual_value
            doc['actual value rolls'] = cargo.actual_value_rolls
        if broker_skill is not None:
            doc['broker'] = {
                'skill': cargo.broker_skill,
                'commission': cargo.commission
            }
            doc['net actual value'] = cargo.net_actual_value
        resp.body = json.dumps(doc)
        resp.status = falcon.HTTP_200
