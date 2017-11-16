'''Overall __init__.py'''

import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String

logging.basicConfig(
    format='%(relativeCreated)d %(name)s %(funcName)s(): %(message)s',
    level=logging.INFO
)
LOGGER = logging.getLogger(__name__)

BASE = declarative_base()


class DB(object):
    '''SQLAlchemy SQLite access class'''

    def __init__(self, sqlite_file):
        LOGGER.debug('sqlite_file = %s', sqlite_file)
        LOGGER.debug('pwd = %s', os.getcwd())
        self.engine = create_engine(
            'sqlite:///{}'.format(sqlite_file))
        self.session = sessionmaker(bind=self.engine)
