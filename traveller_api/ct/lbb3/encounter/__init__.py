''' ct/lbb3/encounter/__init__.py'''

import json
import re
import logging
import configparser
import falcon
from traveller_api.util import RequestProcessor
from traveller_api.ct.lbb3.encounter.encounter_table import EncounterTable1D
from traveller_api.ct.lbb3.encounter.encounter_table import EncounterTable2D
from traveller_api.ct.lbb3.encounter.tables import TERRAIN_TYPES_DM

config = configparser.ConfigParser()    # noqa
config.read('t5.ini')
uwp_validator = re.compile(r'[A-HX][0-9A-Z]{6}\-([0-9A-Z])')    # noqa
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def catch_html_space(text):
    '''Catch HTML space (%20) in text'''
    return text.replace('%20', ' ')


class EncounterTable(RequestProcessor):
    '''
    Return CT LBB3 wilderness encounter table
    GET <apiserver>/ct/lbb3/encounter_table?<options>

    where <options> include:
    - uwp=<UWP>
    - terrain=<terrain type>
    - size=<table size (1 => 6 rows, 2 => 11 rows)

    Returns
    {
        "rows": {
            <n>: {
                'terrain': <terrain type>,
                'quantity': <number of animals>,
                'type': <animal type>,
                'weight': <anmal weight (kg)>,
                'hits': {
                    'dead': <hits to kill>,
                    'unconscious': <hits to render unconscious>
                },
                'wounds': <damage inflicted>,
                'weapons': <weapon type>,
                'armor': <armor type>,
                'behaviour': <behaviour>
            },
            <n>: {
                'terrain': <terrain type>,
                'quantity': null,
                'type': <event description>,
                'weight': null,
                'hits': null,
                'wounds': null,
                'weapons': null,
                'armor': null,
                'behaviour': null
            },
            <...>
        },
        "terrain": <terrain type>,
        "uwp": <UWP>
    }

    First row is an animal, second row is an event.

    <behaviour> is Fn An Sn (herbivores) or An Fn Sn (all others)
    - A<n>: Roll greater than <n> to attack; <n> == 0 => special situation
    - F<n>: Roll greater than <n> to flee; <n> == 0 => special situation
    - S<n>: Animal travels at <n> times normal speeed

    GET <apiserver>/ct/lbb3/encounter_table?list_terrains=true

    Returns
    {
        [
            <terrain type>,
            <terrain type>,
            <...>
        ]
    }

    Listing all valid terrain types

    GET <apiserver>/ct/lbb3/encounter?doc=true

    Returns this text
    '''

    def on_get(self, req, resp):
        '''GET <apiserver>/ct/lbb3/encounter_table'''

        self.query_parameters = {
            'doc': False,
            'list_terrains': False,
            'terrain': None,
            'uwp': None,
            'size': 2
        }
        self.parse_query_string(req.query_string)
        LOGGER.debug('size = %s', self.query_parameters['size'])

        if self.query_parameters['doc'] is True:
            resp.body = self.get_doc_json(req)
            resp.status = falcon.HTTP_200
        elif self.query_parameters['list_terrains'] is True:
            lst = []
            lst.extend(sorted(TERRAIN_TYPES_DM.keys()))
            resp.body = json.dumps(lst)
            resp.status = falcon.HTTP_200
        else:
            try:
                if int(self.query_parameters['size']) == 1:
                    table = EncounterTable1D(
                        terrain=catch_html_space(
                            self.query_parameters['terrain']),
                        uwp=self.query_parameters['uwp']
                    )
                else:
                    table = EncounterTable2D(
                        terrain=catch_html_space(
                            self.query_parameters['terrain']),
                        uwp=self.query_parameters['uwp']
                    )
            except ValueError as err:
                raise falcon.HTTPError(
                    title='Invalid parameter',
                    status='400 Invalid parameter',
                    description=str(err)
                )

            resp.body = table.json()
            resp.status = falcon.HTTP_200
