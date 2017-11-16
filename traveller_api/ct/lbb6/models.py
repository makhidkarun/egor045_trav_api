'''models.py'''

# from flask import current_app, request
# from app.exceptions import ValidationError
from . import db


class StarTable(db.Model):
    '''SQLAlchemy representation of star table'''
    __tablename__ = 'star'
    indx = db.Column(db.Integer, primary_key=True, autoincrement=True)
    typ = db.Column(db.String(1), index=True)
    decimal = db.Column(db.Integer, index=True)
    size = db.Column(db.String(2), index=True)

    min_orbit = db.Column(db.Integer, default=0)
    hz_orbit = db.Column(db.Integer)
    int_orbit = db.Column(db.Integer)
    magnitude = db.Column(db.Float)
    luminosity = db.Column(db.Float)
    temperature = db.Column(db.Integer)
    radius = db.Column(db.Float)
    mass = db.Column(db.Float)

    def __repr__(self):
        fmt_string = '<Star(typ={0} decimal={1} size={2} min_orbit={3} '
        fmt_string += 'hz_orbit={4} int_orbit={10} magnitude={5} '
        fmt_string += 'luminosity={6} '
        fmt_string += 'temperature={7} radius={8} mass={9})>'
        return fmt_string.format(
            self.typ,
            self.decimal,
            self.size,
            self.min_orbit,
            self.hz_orbit,
            self.magnitude,
            self.luminosity,
            self.temperature,
            self.radius,
            self.mass,
            self.int_orbit)


class OrbitTable(db.Model):
    '''SQLAlchemy representation of orbit table'''
    __tablename__ = 'orbit'
    indx = db.Column(db.Integer, primary_key=True)
    au = db.Column(db.Float, nullable=False)
    mkm = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Orbit(indx={0} au={1} mkm={2})>'.format(
            self.indx,
            self.au,
            self.mkm)
