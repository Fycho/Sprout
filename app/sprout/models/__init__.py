from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Vtb(Base):
    __tablename__ = 'vtb'

    vid = Column(Integer, primary_key=True, autoincrement=True)
    name_zh = Column(String(64), nullable=False)
    room_b = Column(String(16), nullable=False)

    user_subscribes = relationship('UserSubscribe', order_by='UserSubscribe.vid', lazy='dynamic')
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }

class UserSubscribe(Base):
    __tablename__ = 'user_subscribe'

    vid = Column(Integer, ForeignKey('vtb.vid'), nullable=False, primary_key=True)
    user_id = Column(String(16), nullable=False, primary_key=True)

    vtb = relationship('Vtb')
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }