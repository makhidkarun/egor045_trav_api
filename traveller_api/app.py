'''app.py'''

import falcon
import traveller_api.ct as ct
import traveller_api.misc as misc
import traveller_api.mt as mt

api = application = falcon.API()

# Misc APIs
api.add_route('/misc/angdia/{distance}/{diameter}', misc.AngDia())

# Classic Traveller APIs
api.add_route('/ct/lbb6/star/{code}', ct.lbb6.star.Star())
api.add_route(
    '/ct/lbb6/star/{code}/orbit/{orbit_no:int}',
    ct.lbb6.orbit.Orbit())
api.add_route(
    '/ct/lbb6/star/{code}/orbit/{orbit_no:int}/planet/{uwp}',
    ct.lbb6.planet.Planet())

# MegaTraveller World Builder's Handbook APIs
api.add_route('/mt/wbh/star/{code}', mt.wbh.star.Star())
