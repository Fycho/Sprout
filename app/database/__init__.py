import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOST = os.environ.get('MYSQL_HOST')
PORT = 3306

engine = create_engine(f'mysql+pymysql://root:root@{HOST}:{PORT}/sprout', max_overflow=5)

Session = sessionmaker(bind=engine, autocommit=True)
session = Session()

Base = declarative_base()

__all__ = ['session', 'engine', 'Base']
