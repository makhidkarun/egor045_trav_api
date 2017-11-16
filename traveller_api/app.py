'''app.py'''

import falcon
import traveller_api.ct as ct
import traveller_api.misc as misc

api = application = falcon.API()

api.add_route('/misc/angdia/{distance}/{diameter}', misc.AngDia())
api.add_route('/ct/lbb6/star/{code}', ct.lbb6.star.Star())
api.add_route(
    '/ct/lbb6/star/{code}/orbit/{orbit_no:int}',
    ct.lbb6.orbit.Orbit())
api.add_route(
    '/ct/lbb6/star/{code}/orbit/{orbit_no:int}/planet/{uwp}',
    ct.lbb6.planet.Planet())
