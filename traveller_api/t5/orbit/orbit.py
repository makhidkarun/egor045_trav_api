'''orbit.py'''

import json


class Orbit(object):
    '''Given flat orbit number, return orbital radius (Mkm and AU)'''

    def __init__(self, orbit_number=None):
        self._orbit_au = [
            0.2, 0.4, 0.7, 1.0, 1.6, 2.8, 5.2,
            10.0, 20.0, 40.0, 77.0,
            154.0, 308.0, 615.0,
            1230.0, 2458.0, 4916.0, 9830.0,
            19500.0     # Fits table on T5.09 Core p.684
        ]
        try:
            self.orbit_number = float(orbit_number)
        except TypeError:
            raise TypeError(
                'Invalid type for orbit_number {}'.format(str(orbit_number)))
        try:
            assert self.orbit_number >= 0
            assert self.orbit_number <= 17.9
        except AssertionError:
            raise ValueError(
                'Orbit number {} out of range'.format(self.orbit_number))
        self.orbit_radius_mkm = None
        self.orbit_radius_au = None
        self.determine_orbit_radius()
        self.orbit_radius_mkm = int(self.orbit_radius_au * 150)

    def determine_orbit_radius(self):
        '''Determine orbit_radius (AU)'''
        orbit_int = int(self.orbit_number)
        orbit_dec = self.orbit_number - int(self.orbit_number)
        self.orbit_radius_au = round(
            self._orbit_au[orbit_int] +
            (self._orbit_au[orbit_int + 1] - self._orbit_au[orbit_int]) *
            orbit_dec,
            1)

    def json(self):
        '''Return JSON representation'''
        doc = {
            'orbit_number': self.orbit_number,
            'au': self.orbit_radius_au,
            'mkm': self.orbit_radius_mkm
        }
        return json.dumps(doc)
