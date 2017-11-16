'''Test SQLAlchemy SQLite'''

import logging
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String

'''
Usage:

db = DB(sqlite_file)
session = db.Session()
table = Schemas.StarTable()
session.query(table).filter_by() ...
'''

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

Base = declarative_base()


class Schemas(object):
    '''SQLAlchemy schemas'''

    class StarTable(Base):
        '''SQLAlchemy representation of star table'''
        __tablename__ = 'star'
        indx = Column(Integer, primary_key=True, autoincrement=True)
        typ = Column(String(1), index=True)
        decimal = Column(Integer, index=True)
        size = Column(String(2), index=True)

        min_orbit = Column(Integer, default=0)
        hz_orbit = Column(Integer)
        int_orbit = Column(Integer)
        magnitude = Column(Float)
        luminosity = Column(Float)
        temperature = Column(Integer)
        radius = Column(Float)
        mass = Column(Float)

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

    class OrbitTable(Base):
        '''SQLAlchemy representation of orbit table'''
        __tablename__ = 'orbit'
        indx = Column(Integer, primary_key=True)
        au = Column(Float, nullable=False)
        mkm = Column(Float, nullable=False)

        def __repr__(self):
            return '<Orbit(indx={0} au={1} mkm={2})>'.format(
                self.indx,
                self.au,
                self.mkm)
