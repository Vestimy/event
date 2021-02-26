from event import db
from sqlalchemy import String, Integer, ForeignKey, DateTime, Date, Time, DATE, Binary, BINARY, BigInteger
from sqlalchemy.orm import relationship


class Country(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String(128), nullable=False)
    region = relationship('Region', back_populates='country')

    def __repr__(self):
        return self.name


class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String(128), nullable=False)

    country_id = db.Column(Integer, ForeignKey('country.id'))
    country = relationship('Country', back_populates='region')
    city = relationship('City', back_populates='region')

    def __repr__(self):
        return self.name




class City(db.Model):
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    region_id = db.Column(Integer, ForeignKey('region.id'))
    region = relationship('Region', back_populates='city')


    event = relationship("Event", back_populates='city')
    arena = relationship("Arena", back_populates="city")
    rentalcompany = relationship("RentalCompany", back_populates="city")
    #
    # edit_city = db.Column(db.DateTime, onupdate=time_now)
    # created_city = db.Column(db.DateTime, default=time_now)

    def __repr__(self):
        return self.name
