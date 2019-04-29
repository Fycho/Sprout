from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:root@my\\sql2:3306/sprout', max_overflow=5)

Session = sessionmaker(bind=engine, autocommit=True)
session = Session()

Base = declarative_base()

__all__ = ['session', 'engine', 'Base']
