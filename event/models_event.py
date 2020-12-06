from .db_setings import db, session, Base
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt
from datetime import datetime
from flask_security import UserMixin, RoleMixin


class Event(Base):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String, nullable=False)
    date_event = db.Column(db.DateTime)
    description = db.Column(db.String(500))
    city = db.Column(db.String(255))
    arena = db.Column(db.String(255))
    data = db.Column(db.DateTime)
    manager = db.Column(db.String(255))
    edit_event = db.Column(db.DateTime, datetime=datetime.utcnow)
    created_event = db.Column(db.DateTime)


class Artist(Base):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    sound_engineer = db.Column(db.String(255))
    administrator = db.Column(db.String(255))
    edit_artist = db.Column(db.DateTime, datetime=datetime.utcnow)
    created_artist = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.created_artist = self.created_artist(self.date)

    def creted_new_artist(self, date):
        if date is not None:
            return datetime.utcnow()


class City(Base):
    __tablename__ = 'city'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    arena = db.Column(db.String(255))

    edit_city = db.Column(db.DateTime, datetime=datetime.utcnow)
    created_city = db.Column(db.DateTime)


class Manager(Base):
    __tablename__ = 'manager'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


association = db.Table('association',
                       Base.metadata,
                       db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('roles_id', db.Integer, db.ForeignKey('roles.id')))


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    # active = db.Column(db.Boolean)
    roles = relationship('Role', secondary=association, back_populates='users', lazy=True)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))

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


class Role(Base, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    users = relationship('User', secondary=association, back_populates='roles', lazy=True)
