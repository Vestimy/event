# from .db_setings import db, session, Base
from event import db
from sqlalchemy import String, Integer, ForeignKey, DateTime, Date, Time, DATE
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt
from datetime import datetime
from pytz import timezone
from flask_security import UserMixin, RoleMixin


def time_now():
    return datetime.now(timezone('UTC'))


arena_city = db.Table('arena_city',
                      db.metadata,
                      db.Column('city_id', db.Integer, db.ForeignKey('city.id')),
                      db.Column('arena_id', db.Integer, db.ForeignKey('arena.id'))
                      )


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    # artist = db.Column(db.String(255))
    artist_id = db.Column(Integer, ForeignKey('artist.id'))
    artist = relationship("Artist", back_populates="event")
    date_event = db.Column(Date)
    time_event = db.Column(Time)
    description = db.Column(db.String(500))
    # city = db.Column(db.String(255))
    city_id = db.Column(Integer, ForeignKey('city.id'))
    city = relationship('City', back_populates='event')
    # arena = db.Column(db.String(255))
    arena_id = db.Column(Integer, ForeignKey('arena.id'))
    arena = relationship('Arena', back_populates='event')
    # manager = db.Column(db.String(255))
    manager_id = db.Column(Integer, ForeignKey('manager.id'))
    manager = relationship('Manager', back_populates='event')
    tour_id = db.Column(Integer, ForeignKey('tour.id'))
    tour = relationship('Tour', back_populates='event')
    edit_event = db.Column(db.DateTime, default=datetime.utcnow)
    created_event = db.Column(db.DateTime)

    def __repr__(self):
        # self.date_event = self.date_event.strftime("%Y %m %d")
        # n = self.date_event.strftime('%m/%d/%Y')
        return f'{self.artist} {self.date_event}'


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    administrator = db.Column(db.String(255))
    event = relationship("Event", back_populates="artist")
    phone_administrator = db.Column(db.String(255))
    sound_engineer = db.Column(db.String(255))
    phone_sound = db.Column(db.String(255))
    monitor_engineer = db.Column(db.String(255))
    phone_monitor = db.Column(db.String(255))
    light = db.Column(db.String(255))
    phone_light = db.Column(db.String(255))

    photoartist = relationship("PhotoArtist", back_populates="artist")
    edit_artist = db.Column(db.DateTime, onupdate=time_now)
    created_artist = db.Column(db.DateTime, default=datetime.utcnow)

    # def __init__(self, **kwargs):
    #     self.name = kwargs.get('name')
    #     self.created_artist = self.date
    # def creted_new_artist(self, date):
    #     if date is not None:
    #         return datetime.utcnow()

    def __repr__(self):
        return self.name


class City(db.Model):
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    # arena = db.Column(db.String(255))
    # arena = relationship('Arena', secondary=arena_city, back_populates='city', lazy=True)
    event = relationship("Event", back_populates='city')
    arena = relationship("Arena", back_populates="city")
    edit_city = db.Column(db.DateTime, onupdate=time_now)
    created_city = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.edit_city = datetime.utcnow()
        self.created_city = self.created_city_time()

    def created_city_time(self):
        if self.created_city is None:
            return datetime.utcnow()

    def __repr__(self):
        return self.name


class Arena(db.Model):
    __tablename__ = 'arena'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    city_id = db.Column(Integer, ForeignKey('city.id'))
    city = relationship("City", back_populates="arena")
    typehall_id = db.Column(Integer, ForeignKey('typehall.id'))
    typehall = relationship("TypeHall", back_populates="arena")
    # city = relationship('City', secondary=arena_city, back_populates='arena', lazy=True)
    address = db.Column(db.String(255))
    phone_admin = db.Column(db.String(255))
    number_of_seats = db.Column(db.Integer)
    hall_size = db.Column(db.String(255), nullable=True)
    razgruzka = db.Column(db.String(255), nullable=True)
    sound = db.Column(db.String(255))
    phone_sound = db.Column(db.String(255))
    light = db.Column(db.String(255))
    phone_light = db.Column(db.String(255))

    imgarena = relationship("ImgArena", back_populates="arena")
    event = relationship('Event', back_populates='arena')
    edit_arena = db.Column(db.DateTime, onupdate=time_now)
    created_arena = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.city_id = kwargs.get('city_id')
        self.typehall_id = kwargs.get('typehall_id')
        self.address = kwargs.get('address')
        self.phone_admin = kwargs.get('phone_admin')
        self.number_of_seats = kwargs.get('number_of_seats')
        self.hall_size = kwargs.get('hall_size')
        self.razgruzka = kwargs.get('razgruzka')
        self.sound = kwargs.get('sound')
        self.phone_sound = kwargs.get('phone_sound')
        self.light = kwargs.get('light')
        self.phone_light = kwargs.get('phone_light')
        self.edit_arena = datetime.utcnow()
        self.created_arena = self.created_arena_time()

    def created_arena_time(self):
        if self.created_arena is None:
            return datetime.utcnow()

    def __repr__(self):
        return self.name


class TypeHall(db.Model):
    __tablename__ = "typehall"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    # arena_id = db.Column(Integer, ForeignKey('typehall.id'))
    arena = relationship("Arena", back_populates="typehall")
    def __repr__(self):
        return self.name


class ImgArena(db.Model):
    __tablename__ = 'imgarena'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    arena_id = db.Column(Integer, ForeignKey('arena.id'))
    arena = relationship("Arena", back_populates="imgarena")

    edit_imgarena = db.Column(db.DateTime, onupdate=time_now)
    created_imgarena = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.url


class PhotoArtist(db.Model):
    __tablename__ = 'photoartist'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    artist_id = db.Column(Integer, ForeignKey('artist.id'))
    artist = relationship("Artist", back_populates="photoartist")

    edit_imgarena = db.Column(db.DateTime, onupdate=time_now)
    created_imgarena = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.url


class ManagerPhoto(db.Model):
    __tablename__ = 'managerphoto'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    manager_id = db.Column(Integer, ForeignKey('manager.id'))
    manager = relationship("Manager", back_populates="managerphoto")

    edit_managerphoto = db.Column(db.DateTime, onupdate=time_now)
    created_managerphoto = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.url


class Manager(db.Model):
    __tablename__ = 'manager'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(255))
    birthday = db.Column(Date)
    address = db.Column(db.String(255))
    event = relationship('Event', back_populates='manager')
    photo = db.Column(db.String(255))
    facebook = db.Column(db.String(255))
    instagram = db.Column(db.String(255))

    managerphoto = relationship("ManagerPhoto", back_populates="manager")

    edit_manager = db.Column(db.DateTime, onupdate=datetime.now)
    created_manager = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return self.name


class Tour(db.Model):
    __tablename__ = 'tour'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    event = relationship('Event', back_populates='tour')
    # event_id = relationship('Event', back_populates='tour')

    edit_tour = db.Column(db.DateTime, onupdate=datetime.now)
    created_tour = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return self.name


association = db.Table('association',
                       db.Model.metadata,
                       db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('roles_id', db.Integer, db.ForeignKey('roles.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean)
    roles = relationship('Role', secondary=association, back_populates='users', lazy=True)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        # self.password = bcrypt.hash(kwargs.get('password'))
        self.password = kwargs.get('password')

    def __repr__(self):
        return self.name

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id,
            expires_delta=expire_delta
        )
        return token

    @classmethod
    def authentificate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise Exception('No user with this password')
        return user


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    users = relationship('User', secondary=association, back_populates='roles', lazy=True)

    def __repr__(self):
        return self.name
