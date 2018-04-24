'''traveller-rest-api utils'''

# pragma pylint: disable=W0102, W0613

import json
import requests
import falcon



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
                            self.query_parameters[param] = False
                    else:
                        self.query_parameters[param] = value
                else:
                    raise falcon.HTTPError(
                        title='Invalid parameter',
                        status='400 Invalid parameter',
                        description='Invalid parameter "{}"'.format(param))
            self._dedupe_list()


    def _dedupe_list(self):
        '''Dedupe list parameter'''
        for param in self.query_parameters:
            if isinstance(self.query_parameters[param], list):
                t_set = set(self.query_parameters[param])
                self.query_parameters[param] = list(t_set)


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


class Ping(RequestProcessor):
    '''
    GET /ping

    Returns
    {
        "status": "OK"
    }
    '''
    @staticmethod
    def on_get(req, resp):
        '''GET /ping'''
        doc = {
            "status": "OK"
        }
        resp.body = json.dumps(doc)
        resp.status = falcon.HTTP_200


class MinMax(object):
    '''Min-max class'''

    def __init__(self, v_1=0, v_2=0):
        try:
            self._min = min(v_1, v_2)
            self._max = max(v_1, v_2)
        except TypeError:
            raise TypeError(
                '{} ({}), {} ({}) different types'.format(
                    v_1, type(v_1),
                    v_2, type
                )
            )

    def min(self):
        '''Min'''
        return self._min

    def max(self):
        '''Max'''
        return self._max

    def dict(self):
        '''dict representation'''
        return {
            'min': self._min,
            'max': self._max
        }

    def json(self):
        '''JSON representation'''
        return json.dumps(self.dict(), sort_keys=True)

    def __str__(self):
        return '<min = {} max = {}>'.format(self._min, self._max)

    def __repr__(self):
        return str(self)
