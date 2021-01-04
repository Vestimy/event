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
        # self.date_event = self.date_event.strftime("%Y %m %d")
        # n = self.date_event.strftime('%m/%d/%Y')
        return f'{self.artist} {self.date_event}'


class TypeEvent(db.Model):
    __tablename__ = 'typeevent'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    # event_id = db.Column(Integer, ForeignKey('event.id'))
    event = relationship('Event', back_populates='typeevent')
    # city = db.Column(db.String(255))
    # city_id = db.Column(Integer, ForeignKey('city.id'))
    # city = relationship('City', back_populates='event')
    edit_typeevent = db.Column(db.DateTime, onupdate=time_now)
    created_edit_typeevent = db.Column(db.DateTime, default=time_now)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.city_id = kwargs.get('city_id')

    def __repr__(self):
        # self.date_event = self.date_event.strftime("%Y %m %d")
        # n = self.date_event.strftime('%m/%d/%Y')
        return self.name


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(128))
    first_name = db.Column(db.String(128))
    administrator = db.Column(db.String(128))
    alias = db.Column(String(128))
    phone_administrator = db.Column(db.String(128))
    sound_engineer = db.Column(db.String(128))
    phone_sound = db.Column(db.String(128))
    monitor_engineer = db.Column(db.String(128))
    phone_monitor = db.Column(db.String(128))
    light = db.Column(db.String(128))
    phone_light = db.Column(db.String(128))

    img = db.Column(db.String(255))

    event = relationship("Event", back_populates="artist")
    photoartist = relationship("PhotoArtist", back_populates="artist")

    edit_artist = db.Column(db.DateTime, onupdate=time_now)
    created_artist = db.Column(db.DateTime, default=time_now)

    # def __init__(self, **kwargs):
    #     self.name = kwargs.get('name')
    #     self.created_artist = self.date
    # def creted_new_artist(self, date):
    #     if date is not None:
    #         return datetime.utcnow()




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
    name = db.Column(db.String(255), nullable=False)
    region_id = db.Column(Integer, ForeignKey('region.id'))
    region = relationship('Region', back_populates='city')

    # event = relationship("Event", back_populates='city')
    arena = relationship("Arena", back_populates="city")

    #
    # edit_city = db.Column(db.DateTime, onupdate=time_now)
    # created_city = db.Column(db.DateTime, default=time_now)

    def __repr__(self):
        return self.name


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
    imgarena = relationship("ImgArena", back_populates="arena")
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
    # arena_id = db.Column(Integer, ForeignKey('typehall.id'))
    arena = relationship("Arena", back_populates="typehall")

    edit_time = db.Column(DateTime, onupdate=time_now)
    create_time = db.Column(DateTime, default=time_now)

    def __repr__(self):
        return self.name


class ImgArena(db.Model):
    __tablename__ = 'imgarena'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    arena_id = db.Column(Integer, ForeignKey('arena.id'))
    arena = relationship("Arena", back_populates="imgarena")

    edit_imgarena = db.Column(db.DateTime, onupdate=time_now)
    created_imgarena = db.Column(db.DateTime, default=time_now)

    def __repr__(self):
        return self.url


class PhotoArtist(db.Model):
    __tablename__ = 'photoartist'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    artist_id = db.Column(Integer, ForeignKey('artist.id'))
    artist = relationship("Artist", back_populates="photoartist")

    edit_imgarena = db.Column(db.DateTime, onupdate=time_now)
    created_imgarena = db.Column(db.DateTime, default=time_now)

    def __repr__(self):
        return self.url


class ManagerPhoto(db.Model):
    __tablename__ = 'managerphoto'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    manager_id = db.Column(Integer, ForeignKey('manager.id'))
    manager = relationship("Manager", back_populates="managerphoto")

    edit_managerphoto = db.Column(db.DateTime, onupdate=time_now)
    created_managerphoto = db.Column(db.DateTime, default=time_now)

    def __repr__(self):
        return self.url


class Manager(db.Model):
    __tablename__ = 'manager'
    id = db.Column(db.Integer, primary_key=True)
    managerphoto = relationship("ManagerPhoto", back_populates="manager")

    edit_manager = db.Column(db.DateTime, onupdate=time_now)
    created_manager = db.Column(db.DateTime, default=time_now)

    # def __repr__(self):
    #     return self.user


class Tour(db.Model):
    __tablename__ = 'tour'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    event = relationship('Event', back_populates='tour')
    # event_id = relationship('Event', back_populates='tour')

    edit_tour = db.Column(db.DateTime, onupdate=time_now)
    created_tour = db.Column(db.DateTime, default=time_now())

    def __repr__(self):
        return self.name


association = db.Table('association',
                       db.Model.metadata,
                       db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('roles_id', db.Integer, db.ForeignKey('roles.id')))


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
    roles = relationship('Role', secondary=association, back_populates='users', lazy=True)
    lead_roles_id = db.Column(Integer, ForeignKey('roles.id'))
    lead_roles = relationship("Role", back_populates='users_lead')
    birthday = db.Column(Date)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    photo = db.Column(db.String(255))

    event = relationship('Event', back_populates='user')
    event_staff = relationship('Event', secondary=event_staff_users, back_populates='users_staff', lazy=True)
    facebook = db.Column(db.String(255))
    instagram = db.Column(db.String(255))

    document = relationship("Document", back_populates='users')
    edit_time = db.Column(DateTime, onupdate=time_now)
    create_time = db.Column(DateTime, default=time_now)

    # def __init__(self, **kwargs):
    #     self.name = kwargs.get('name')
    #     self.email = kwargs.get('email')
    #     self.password = kwargs.get('password')

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
