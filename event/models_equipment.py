# from .db_setings import db, session, Base
from event import db
from sqlalchemy import String, Integer, ForeignKey, DateTime, Date, Time, DATE
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt
from datetime import datetime

class EquipmentCategory(db.Model):
    __tablename__ = 'equipmentcategory'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(255), nullable=False)
    equipment = relationship('Equipment', back_populates='equipmentcategory')

    edit_equipmentcategory = db.Column(db.DateTime, onupdate=datetime.now)
    created_equipmentcategory = db.Column(db.DateTime, default=datetime.now())

class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(Integer, primary_key=True)

    category_id = db.Column(Integer, ForeignKey('equipmentcategory.id'))
    equipmentcategory = relationship('EquipmentCategory', back_populates='equipment')
    edit_equipment = db.Column(db.DateTime, onupdate=datetime.now)
    created_equipment = db.Column(db.DateTime, default=datetime.now())
