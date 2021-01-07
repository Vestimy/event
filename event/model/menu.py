from event import db
from event.models import time_now
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Date, Time, DATE, Binary, BINARY, BigInteger


class Menu(db.Model):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    url = Column(String(128))
    edit_menu = db.Column(db.DateTime, onupdate=time_now)
    created_menu = db.Column(db.DateTime, default=time_now)

    def __repr__(self):
        return self.name
