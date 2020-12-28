# ----------------------------------------------------
# Program by Andrey Vestimy
#
#
# Version   Date    Info
# 1.0       2020    ----
#
# ----------------------------------------------------
# from .db_setings import db, session, Base
from event import db
from event.models import time_now
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Date, Time, DATE, Binary, BINARY, BigInteger
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt
from datetime import datetime
from pytz import timezone
from flask_security import UserMixin, RoleMixin

class Menu(db.Model):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    url = Column(String(128))
    edit_menu = db.Column(db.DateTime, onupdate=time_now)
    created_menu = db.Column(db.DateTime, default=time_now)

    def __repr__(self):
        return self.name