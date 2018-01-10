'''__init__.py'''

import json
import configparser
import falcon
from .trade_cargo import TradeCargo, TradeCargoBroker

config = configparser.ConfigParser()
config.read('t5.ini')


class CargoGen(object):
    '''CargoGen'''
    @staticmethod
    def on_get(req, resp, source_uwp, market_uwp=None):
        '''GET /t5/cargogen/source/<source_uwp>/dest/<dest_uwp>'''
        cargo = TradeCargo()
        cargo.generate_cargo(source_uwp, market_uwp)
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

        resp.body = json.dumps(doc)
        resp.status = falcon.HTTP_200


class BrokerGen(object):
    '''CargoGen'''
    @staticmethod
    def on_get(req, resp, source_uwp, market_uwp=None, broker_skill=None):
        '''GET /t5/cargogen/source/<source_uwp>/dest/<dest_uwp>'''
        cargo = TradeCargoBroker()
        cargo.generate_cargo(source_uwp, market_uwp, broker_skill)
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
