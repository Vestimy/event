import logging
import os, inspect, sys
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, flash, request, redirect, url_for, render_template, send_from_directory, json
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_jwt_extended import JWTManager
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

from flask_security import SQLAlchemySessionUserDatastore, Security
from flask_security import current_user, user_registered, login_required
from flask_mail import Mail
from flask_datepicker import datepicker
from flask_bootstrap import Bootstrap

UPLOAD_FOLDER = '/home/vestimy/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy()
jwt = JWTManager()
login = LoginManager()
admin = Admin(name='admins')
security = Security()
mail = Mail()
bootstrap = Bootstrap()

from .forms_security import ExtendedRegisterForm


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    admin.init_app(app, url='/admin', index_view=HomeAdminView(name='Home'))
    login.init_app(app)
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    mail.init_app(app)
    # security.init_app(app, user_datastore, register_form=ExtendedRegisterForm)
    security.init_app(app, user_datastore, register_form=ExtendedRegisterForm)
    bootstrap.init_app(app)

    @user_registered.connect_via(app)
    def user_registered_sighandler(app, user, confirm_token):
        default_role = user_datastore.find_role("users")
        user_datastore.add_role_to_user(user, default_role)
        db.session.commit()

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

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_PHOTO_PROFILES'],
                                   filename)

    @app.route('/photo_profile/<filename>')
    @login_required
    def photo_profile(filename):
        return send_from_directory(Config.UPLOAD_PHOTO_PROFILES,
                                   filename)

    @app.route('/photo_arena/<filename>')
    @login_required
    def photo_arena(filename):
        return send_from_directory(Config.UPLOAD_PHOTO_ARENA,
                                   filename)

    @app.route('/photo_artist/<filename>')
    @login_required
    def photo_artist(filename):
        return send_from_directory(Config.UPLOAD_PHOTO_ARTIST,
                                   filename)

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
admin.add_view(AdminView(ManagerPhoto, db.session))
admin.add_view(AdminView(TypeHall, db.session))
admin.add_view(AdminView(TypeEvent, db.session))

admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    file_heandler = logging.FileHandler(Config.PATH + '/log/api.log')
    file_heandler.setFormatter(formatter)
    logger.addHandler(file_heandler)

    return logger


logger = setup_logger()


def allowed_photo_profile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_PHOTO
