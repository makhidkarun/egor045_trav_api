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

    class StarColorTable(Base):
        '''SQLAlchemy representation of starcolor table'''
        __tablename__ = 'starcolor'
        code = Column(String(6), primary_key=True)
        red = Column(Integer)
        green = Column(Integer)
        blue = Column(Integer)

        def __repr__(self):
            fmt_string = '<Star(code={0} red={1} green={2} blue={3})>'
            return fmt_string.format(
                self.code,
                self.red,
                self.green,
                self.blue)
