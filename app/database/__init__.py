import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOST = os.environ.get('MYSQL_HOST')
PORT = 3306
USER = os.environ.get('MYSQL_USER')
PWD = os.environ.get('MYSQL_PWD')

engine = create_engine(f'mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/sprout', max_overflow=5)

Session = sessionmaker(bind=engine, autocommit=True)
session = Session()

Base = declarative_base()

__all__ = ['session', 'engine', 'Base']
