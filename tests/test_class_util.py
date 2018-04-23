'''test_class_util.py'''

# pragma pylint: disable=W0212, C0413

import json
import logging
import os
import sys
import unittest
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../'
)
from traveller_api.util import MinMax

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class TestMinMax(unittest.TestCase):
    '''MinMax unit tests'''

    def test_create(self):
        '''Test object creation'''
        # Create OK
        for test in [
                (2, 1),
                (1, 3),
                ('a', 'x'),
                ([0, 1, 2], [3, 4])
            ]:
            minmax = MinMax(test[0], test[1])
            self.assertTrue(minmax._min < minmax._max)

        # Create not OK
        for test in [
                (2, 'a'),
                ({'a': 1, 'b': 23}, {'p': 's', 'q': 404})
            ]:
            with self.assertRaises(TypeError):
                _ = MinMax(test[0], test[1])

    def test_functions(self):
        '''Test min(), max()'''
        minmax = MinMax(2, 1)
        self.assertTrue(minmax.min() == 1)
        self.assertTrue(minmax.max() == 2)
    
    def test_representations(self):
        '''Test representations'''
        as_dict = {'min': 'ax', 'max': 'c'}
        as_str = '<min = ax max = c>'
        as_json = json.dumps(as_dict, sort_keys=True)
        minmax = MinMax('c', 'ax')

        LOGGER.debug('minmax = %s', minmax)
        self.assertTrue(as_dict == minmax.dict())
        self.assertTrue(as_str == str(minmax))
        self.assertTrue(as_json == minmax.json())
        self.assertTrue(as_str == repr(minmax))
        