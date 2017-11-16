'''traveller-rest-api utils'''

import requests


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
