from event import db
from sqlalchemy import String, Integer, ForeignKey, DateTime, Date, Time, DATE
from sqlalchemy.orm import relationship
from event.models import time_now


class EquipmentCategory(db.Model):
    __tablename__ = 'equipmentcategory'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(128), nullable=False)
    title = db.Column(String(128), nullable=False)
    # equipment = relationship('Equipment', back_populates='equipmentcategory')
    description = db.Column(String(256))
    equipmentsubcategory = relationship('EquipmentSubcategory', back_populates='equipmentcategory')

    edit = db.Column(db.DateTime, onupdate=time_now)
    created = db.Column(db.DateTime, default=time_now)

    def __repr__(self):
        return self.name


class EquipmentSubcategory(db.Model):
    __tablename__ = 'equipmentsubcategory'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(128), nullable=False)
    title = db.Column(String(128))
    description = db.Column(String(256))

    equipmentcategory_id = db.Column(Integer, ForeignKey('equipmentcategory.id'))
    equipmentcategory = relationship('EquipmentCategory', back_populates='equipmentsubcategory')
    equipment = relationship('Equipment', back_populates='subcategory')
    edit = db.Column(db.DateTime, onupdate=time_now)
    created = db.Column(db.DateTime, default=time_now)

    def __repr__(self):
        return self.name


class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(128), nullable=False)
    title = db.Column(String(128))
    description = db.Column(String(256))
    number = db.Column(Integer)
    rent = db.Column(Integer)
    weight_kg = db.Column(Integer)
    power_w = db.Column(Integer)

    subcategory_id = db.Column(Integer, ForeignKey('equipmentsubcategory.id'))
    subcategory = relationship('EquipmentSubcategory', back_populates='equipment')

    edit = db.Column(db.DateTime, onupdate=time_now)
    created = db.Column(db.DateTime, default=time_now)

    def __repr__(self):
        return self.name
