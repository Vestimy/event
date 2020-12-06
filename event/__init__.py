import logging
from flask import Flask, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_jwt_extended import JWTManager
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_security import SQLAlchemySessionUserDatastore, Security
from flask_security import current_user
from flask_mail import Mail
from flask_datepicker import datepicker
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
jwt = JWTManager()
login = LoginManager()
admin = Admin(name='admins')
security = Security()
mail = Mail()
bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    admin.init_app(app, url='/admin', index_view=HomeAdminView(name='Home'))
    login.init_app(app)
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    from .models import Role, User
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    mail.init_app(app)
    security.init_app(app, user_datastore)
    bootstrap.init_app(app)

    from .views.main.views import main
    from .views.event.views import events
    from .views.arena.views import arenas
    from .views.city.views import citys
    from .views.artist.views import artists
    from .views.manager.views import managers
    from .views.login.views import logins
    from .views.tour.views import tours

    app.register_blueprint(main)
    app.register_blueprint(events)
    app.register_blueprint(arenas)
    app.register_blueprint(citys)
    app.register_blueprint(artists)
    app.register_blueprint(managers)
    app.register_blueprint(tours)
    # app.register_blueprint(logins)

    jwt.init_app(app)
    return app


from .models import *
from .models_equipment import *


class AdminMixIn:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminView(AdminMixIn, ModelView):
    pass
    # def is_accessible(self):
    #     return current_user.has_role('admin')
    #
    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('security.login', next=request.url))


class HomeAdminView(AdminMixIn, AdminIndexView):
    pass
    # def is_accessible(self):
    #     return current_user.has_role('admin')
    #
    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('security.login', next=request.url))


# admin.index_view =

admin.add_view(AdminView(Tour, db.session))
admin.add_view(AdminView(Event, db.session))
admin.add_view(AdminView(Artist, db.session))
admin.add_view(AdminView(City, db.session))
admin.add_view(AdminView(Arena, db.session))
admin.add_view(AdminView(Manager, db.session))
admin.add_view(AdminView(ImgArena, db.session))
admin.add_view(AdminView(PhotoArtist, db.session))
admin.add_view(AdminView(EquipmentCategory, db.session))
admin.add_view(AdminView(Equipment, db.session))

admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))


# @login.user_loader
# def load_user(user_id):
#     return User.get(user_id)


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_heandler = logging.FileHandler('log/api.log')
    file_heandler.setFormatter(formatter)
    logger.addHandler(file_heandler)

    return logger


# db.create_all()
logger = setup_logger()
