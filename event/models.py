# from .db_setings import db, session, Base
from event import db
from sqlalchemy import String, Integer, ForeignKey, DateTime, Date, Time, DATE, Binary, BINARY, BigInteger
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt
from datetime import datetime
from pytz import timezone
from flask_security import UserMixin, RoleMixin


def time_now():
    return datetime.now(timezone('Europe/Moscow'))


event_staff_users = db.Table('event_staff_users',
                             db.Model.metadata,
                             db.Column('users_staff', db.Integer, ForeignKey('users.id')),
                             db.Column('event_staff', db.Integer, ForeignKey('event.id'))
                             )
association = db.Table('association',
                       db.Model.metadata,
                       db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('roles_id', db.Integer, db.ForeignKey('roles.id')))


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(Integer, ForeignKey('artist.id'))
    artist = relationship("Artist", back_populates="event")
    typeevent_id = db.Column(Integer, ForeignKey('typeevent.id'))
    typeevent = relationship('TypeEvent', back_populates='event')
    date_event = db.Column(Date)
    time_event = db.Column(Time)
    description = db.Column(db.String(500))
    # city_id = db.Column(Integer, ForeignKey('city.id'))
    # city = relationship('City', back_populates='event')
    arena_id = db.Column(Integer, ForeignKey('arena.id'))
    arena = relationship('Arena', back_populates='event')
    user_id = db.Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='event')

    users_staff = relationship('User', secondary=event_staff_users, back_populates='event_staff', lazy=True)

    tour_id = db.Column(Integer, ForeignKey('tour.id'))
    tour = relationship('Tour', back_populates='event')
    edit_event = db.Column(db.DateTime, onupdate=time_now)
    created_event = db.Column(db.DateTime, default=time_now)

    def __repr__(self):
        return f'{self.artist} {self.date_event}'


class TypeEvent(db.Model):
    __tablename__ = 'typeevent'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    event = relationship('Event', back_populates='typeevent')
    edit_typeevent = db.Column(db.DateTime, onupdate=time_now)
    created_edit_typeevent = db.Column(db.DateTime, default=time_now)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.city_id = kwargs.get('city_id')

    def __repr__(self):
        return self.name


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)

    last_name = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    alias = db.Column(String(128))

    description = db.Column(db.String(500))

    administrator = db.Column(db.String(128))
    phone_administrator = db.Column(db.String(128))

    sound_engineer = db.Column(db.String(128))
    phone_sound = db.Column(db.String(128))

    monitor_engineer = db.Column(db.String(128))
    phone_monitor = db.Column(db.String(128))

    light = db.Column(db.String(128))
    phone_light = db.Column(db.String(128))

    img = db.Column(db.String(255))

    event = relationship("Event", back_populates="artist")

    edit_artist = db.Column(db.DateTime, onupdate=time_now)
    created_artist = db.Column(db.DateTime, default=time_now)


class Arena(db.Model):
    __tablename__ = 'arena'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(500))
    city_id = db.Column(Integer, ForeignKey('city.id'))
    city = relationship("City", back_populates="arena")
    typehall_id = db.Column(Integer, ForeignKey('typehall.id'))
    typehall = relationship("TypeHall", back_populates="arena")
    address = db.Column(db.String(255))
    phone_admin = db.Column(db.String(20))
    number_of_seats = db.Column(db.String(20))
    hall_size = db.Column(db.String(255))
    razgruzka = db.Column(db.String(255))
    sound = db.Column(db.String(255))
    phone_sound = db.Column(db.String(20))
    light = db.Column(db.String(255))
    phone_light = db.Column(db.String(20))
    img = db.Column(String(255))
    event = relationship('Event', back_populates='arena')

    edit_arena = db.Column(db.DateTime, onupdate=time_now)
    created_arena = db.Column(db.DateTime, default=time_now)

    def __repr__(self):
        return self.name


class TypeHall(db.Model):
    __tablename__ = "typehall"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    arena = relationship("Arena", back_populates="typehall")

    edit_time = db.Column(DateTime, onupdate=time_now)
    create_time = db.Column(DateTime, default=time_now)

    def __repr__(self):
        return self.name


class Tour(db.Model):
    __tablename__ = 'tour'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    event = relationship('Event', back_populates='tour')

    edit_tour = db.Column(db.DateTime, onupdate=time_now)
    created_tour = db.Column(db.DateTime, default=time_now())

    def __repr__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(250), nullable=True)
    first_name = db.Column(db.String(250), nullable=True)
    patronymic = db.Column(db.String(250), nullable=True)

    email = db.Column(db.String(255), nullable=False, unique=True)
    login = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    active = db.Column(db.Boolean)

    facebook = db.Column(db.String(128))
    instagram = db.Column(db.String(128))

    birthday = db.Column(Date)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    photo = db.Column(db.String(255))

    roles = relationship('Role', secondary=association, back_populates='users', lazy=True)
    lead_roles_id = db.Column(Integer, ForeignKey('roles.id'))
    lead_roles = relationship("Role", back_populates='users_lead')

    event = relationship('Event', back_populates='user')
    event_staff = relationship('Event', secondary=event_staff_users, back_populates='users_staff', lazy=True)

    document = relationship("Document", back_populates='users')
    edit_time = db.Column(DateTime, onupdate=time_now)
    create_time = db.Column(DateTime, default=time_now)

    def __repr__(self):
        return f"{self.last_name} {self.first_name}"

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
    title = db.Column(db.String(250))
    description = db.Column(db.String(255), nullable=False)
    users = relationship('User', secondary=association, back_populates='roles', lazy=True)
    users_lead = relationship("User", back_populates='lead_roles')
    edit_time = db.Column(DateTime, onupdate=time_now)
    create_time = db.Column(DateTime, default=time_now)

    def __repr__(self):
        return self.name


class Document(db.Model):
    __tablename__ = "document"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(255))

    users_id = db.Column(Integer, ForeignKey('users.id'))
    users = relationship("User", back_populates='document')
    edit_time = db.Column(DateTime, onupdate=time_now)
    create_time = db.Column(DateTime, default=time_now)

    def __repr__(self):
        return self.name
