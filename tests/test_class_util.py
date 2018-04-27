'''test_class_util.py'''

# pragma pylint: disable=C0413, E0401

import json
import logging
import os
import sys
import unittest
from ehex import ehex
sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__)) + '/../')
from traveller_api.util import MinMax

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class TestMinMax(unittest.TestCase):
    '''MinMax unit tests'''

    def test_min_max_basic(self):
        '''MinMax unit tests'''

        # No args => None, None
        minmax = MinMax()
        self.assertTrue(minmax.min() is None)
        self.assertTrue(minmax.max() is None)

        # Test min vs max
        minmax = MinMax(2, 1)
        self.assertTrue(minmax.min() == 1)
        self.assertTrue(minmax.max() == 2)
        minmax = MinMax(1, 2)
        self.assertTrue(minmax.min() == 1)
        self.assertTrue(minmax.max() == 2)

        # Test min == max
        minmax = MinMax(1, 1)
        self.assertTrue(minmax.min() == minmax.max())

    def test_representations(self):
        '''Test representations'''
        minmax = MinMax(1, 2)
        self.assertTrue(minmax.dict() == {'min': 1, 'max': 2})
        self.assertTrue(str(minmax) == '<min = 1 max = 2>')
        LOGGER.debug('minmax.json() = %s', minmax.json())
        self.assertTrue(
            minmax.json() == json.dumps({'min': 1, 'max': 2}, sort_keys=True)
        )

    def test_valid_data_types(self):
        '''Test data types'''
        tests = [
            1.5, 3.5,           # float-float
            1, 2.0,             # int-float
            'a', 'b',           # str-str
            'a', 'bbb',         # str-str
            [0, 1], [1, 0],     # list-list
            ehex(1), ehex(6),   # ehex-ehex
            1, ehex(6),         # int-ehex
            ehex(6), 'A',       # ehex-str
        ]
        i = 0
        while i < len(tests):
            v_1 = tests[i]
            v_2 = tests[i + 1]
            i += 2

            minmax = MinMax(v_1, v_2)
            LOGGER.debug(
                'v_1 = %s v_2 = %s minmax = %s',
                v_1, v_2, str(minmax)
            )
            self.assertTrue(minmax.min() == v_1)
            self.assertTrue(minmax.max() == v_2)

    def test_invalid_data_types(self):
        '''Test invalid data types'''
        tests = [
            {'a': 1, 'b': 3}, {'c': 1, 'd': 2}, # dict
        ]
        i = 0
        while i < len(tests):
            v_1 = tests[i]
            v_2 = tests[i + 1]
            i += 2

            with self.assertRaises(TypeError):
                LOGGER.debug('v_1 = %s v_2 = %s', v_1, v_2)
                _ = MinMax(v_1, v_2)

    def test_invalid_comparisons(self):
        '''Test invalid comparisons'''
        tests = [
            'a', 1,         # str-int
            'a', 1.0,       # str-float
            [1, 0], 1,      # list-int
            1.0, [1, 0],    # float-list
            1, None,        # int-None
            1.0, None,      # float-None
            'a', None,      # str-None
            [1, 0], None    # list-None
        ]
        i = 0
        while i < len(tests):
            v_1 = tests[i]
            v_2 = tests[i + 1]
            i += 2

            with self.assertRaises(TypeError):
                LOGGER.debug('v_1 = %s v_2 = %s', v_1, v_2)
                _ = MinMax(v_1, v_2)

        # Test one param only
        with self.assertRaises(TypeError):
            _ = MinMax(1)
