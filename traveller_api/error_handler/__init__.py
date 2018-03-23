'''error_handler/__init__.py'''

import logging
import falcon

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class Foo(object):
    '''
    Test error handling
    
    GET /foo/<strng>

    Returns
    {
        "title": "Generic error"
        "description": "Requested <strng>"
    }
    with HTTP status 400
    '''

    def on_get(self, req, resp, strng):
        '''GET /foo/<strng>'''
        raise falcon.HTTPError(
            title='Generic error',
            description='Requested {}'.format(strng),
            status='400 Confounded by developer'
        )
