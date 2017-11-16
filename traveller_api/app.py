'''app.py'''

import falcon
import traveller_api.ct as ct
import traveller_api.misc as misc

api = application = falcon.API()

__routes = {
    '/misc/angdia/{distance}/{diameter}': misc.AngDia(),
    '/ct/lbb6/star/{code}': ct.lbb6.star.Star(),
    '/ct/lbb6/star/{code}/orbit/{orbit_no:int}': ct.lbb6.orbit.Orbit()
}

for url in __routes:
    api.add_route(url, __routes[url])
