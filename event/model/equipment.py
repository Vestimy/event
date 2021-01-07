from event import db
from sqlalchemy import String, Integer, ForeignKey, DateTime, Date, Time, DATE
from sqlalchemy.orm import relationship
from event.models import time_now


class EquipmentCategory(db.Model):
    __tablename__ = 'equipmentcategory'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(255), nullable=False)
    equipment = relationship('Equipment', back_populates='equipmentcategory')

    edit_equipmentcategory = db.Column(db.DateTime, onupdate=time_now)
    created_equipmentcategory = db.Column(db.DateTime, default=time_now)


class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(Integer, primary_key=True)

    category_id = db.Column(Integer, ForeignKey('equipmentcategory.id'))
    equipmentcategory = relationship('EquipmentCategory', back_populates='equipment')
    edit_equipment = db.Column(db.DateTime, onupdate=time_now)
    created_equipment = db.Column(db.DateTime, default=time_now)
