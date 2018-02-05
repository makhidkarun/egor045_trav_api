'''app.py'''

import falcon
import traveller_api.ct as ct
import traveller_api.misc as misc
import traveller_api.mt as mt
import traveller_api.t5.cargogen as t5_cargogen

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
api.add_route(
    '/mt/wbh/star/{code}/orbit/{orbit_no:int}',
    mt.wbh.orbit.Orbit())

# T5 Cargogen API
api.add_route('/t5/cargogen/source/{source_uwp}', t5_cargogen.CargoGen())
api.add_route(
    '/t5/cargogen/source/{source_uwp}/market/{market_uwp}',
    t5_cargogen.CargoGen())
api.add_route(
    '/t5/cargogen/source/{source_uwp}/market/{market_uwp}/' +
    'broker/{broker_skill:int}',
    t5_cargogen.BrokerGen())

# CT Cargogen API
api.add_route('/ct/lbb2/cargogen/purchase', ct.lbb2.cargogen.Purchase())
