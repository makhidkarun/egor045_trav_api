'''traveller-rest-api utils'''

import json
import requests
import falcon
from prometheus_client import multiprocess, CollectorRegistry
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


class RestQuery(object):
    '''REST queries'''
    @staticmethod
    def get(url, params=None):
        '''GET'''
        if isinstance(params, dict):
            resp = requests.get(url, params=params)
        else:
            resp = requests.get(url)
        return resp


# @staticmethod
def parse_query_string(query_string='', valid_query_parameters={}):
    '''Parse query string, return query_parameters dict'''
    query_parameters = valid_query_parameters
    if query_string != '':
        options_list = query_string.split('&')
        for option in options_list:
            param, value = option.split('=')
            if param in valid_query_parameters:
                if isinstance(query_parameters[param], list):
                    query_parameters[param].append(value)
                else:
                    query_parameters[param] = value
            else:
                raise falcon.HTTPError(
                    title='Invalid parameter',
                    status='400 Invalid parameter',
                    description='Invalid parameter "{}"'.format(param))
    return query_parameters


class Metrics(object):
    '''Report Prometheus metrics'''

    def on_get(self, req, resp):
        '''GET /metrics/'''
        registry = CollectorRegistry()
        multiprocess.MultiProcessCollector(registry)
        data = generate_latest(registry)

        resp.body = data
        resp.content_type = CONTENT_TYPE_LATEST
        resp.status = falcon.HTTP_200


class RequestProcessor(object):
    '''Request processor'''

    def __init__(self):
        self.query_parameters = {}

    def parse_query_string(self, query_string=''):
        '''Process query string (from req)'''
        # self.query_parameters = valid_query_parameters
        if query_string != '':
            options_list = query_string.split('&')
            for option in options_list:
                param, value = option.split('=')
                if param in self.query_parameters:
                    if isinstance(self.query_parameters[param], list):
                        self.query_parameters[param].append(value)
                    elif isinstance(self.query_parameters[param], bool):
                        if str(value).lower() == 'true':
                            self.query_parameters[param] = True
                    else:
                        self.query_parameters[param] = value
                else:
                    raise falcon.HTTPError(
                        title='Invalid parameter',
                        status='400 Invalid parameter',
                        description='Invalid parameter "{}"'.format(param))

    def get_doc(self, req):
        '''Return class doc, replace <apiserver> with server prefix'''
        if self.__doc__:
            doc = {
                'doc': self.__doc__.replace('<apiserver>', req.prefix)
            }
        else:
            doc = {'doc': 'API documentation not available'}
        return doc

    def get_doc_json(self, req):
        '''Return class doc as JSON'''
        return json.dumps(self.get_doc(req))
