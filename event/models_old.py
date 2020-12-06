from .db_setings import db, session, Base
from sqlalchemy.orm import relationship
from flask_jwt_extended import create_access_token
from datetime import timedelta
from passlib.hash import bcrypt
from datetime import datetime
from flask_security import UserMixin, RoleMixin


association = db.Table('association',
                       Base.metadata,
                       db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('roles_id', db.Integer, db.ForeignKey('roles.id')))

arena_city = db.Table('arena_city',
                      Base.metadata,
                      db.Column('citys_id', db.Integer, db.ForeignKey('citys.id')),
                      db.Column('arenas_id', db.Integer, db.ForeignKey('arenas.id'))
                      )
arena_event = db.Table('arena_event',
                       Base.metadata,
                       db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
                       db.Column('citys_id', db.Integer, db.ForeignKey('citys.id'))
                       )


class Event(Base):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String)
    description = db.Column(db.String(500), nullable=False)
    data = db.Column(db.DateTime)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))
    citys = relationship('City', secondary=arena_event, back_populates='event', lazy=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return self.artist

    @classmethod
    def get_user_list(cls, user_id):
        try:
            videos = cls.query.filter(Event.user_id == user_id).all()
            session.commit()
        except Exception:
            session.rollback()
            raise
        return videos

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def get(cls, tutorial_id, user_id):
        try:
            video = cls.query.filter(Event.id == tutorial_id,
                                     Event.user_id == user_id
                                     ).first()
            if not video:
                raise Exception('No tutorials with this id')
        except Exception:
            session.rollback()
            raise
        return video

    @classmethod
    def get_list(cls):
        try:
            event = cls.query.all()
            session.commit()
            if not event:
                raise Exception('No tutorials with this id')
        except Exception:
            session.rollback()
            raise
        return event

    def update(self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
            session.commit()
        except Exception:
            session.rollback()
            raise


class Manager(Base):
    __tablename__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255))
    adres = db.Column(db.String(255))
    event = relationship('Event', backref='managers', lazy=True)

    def __repr__(self):
        return self.name


class Arena(Base):
    __tablename__ = 'arenas'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    citys = relationship('City', secondary=arena_city, back_populates='arenas', lazy=True)
    # event = relationship('Event', backref='managers', lazy=True)
    def __repr__(self):
        return self.title


class City(Base):
    __tablename__ = 'citys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    arenas = relationship('Arena', secondary=arena_city, back_populates='citys', lazy=True)
    event = relationship('Event', secondary=arena_event, back_populates='citys', lazy=True)

    def __repr__(self):
        return self.name


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


class Rider(Base):
    __tablename__ = 'riders'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String)
