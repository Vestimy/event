import logging
import uuid
from flask import Flask, jsonify, flash, request, redirect, url_for, render_template, send_from_directory, json

from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_security import SQLAlchemySessionUserDatastore, Security
from flask_login import current_user, login_required
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap

UPLOAD_FOLDER = '/home/vestimy/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin(name='admins')
# security = Security()
mail = Mail()
bootstrap = Bootstrap()

login_manager.login_view = 'security.login'
login_manager.login_message = u"Пожалуйста, авторизируйтесь."
from .forms_security import ExtendedRegisterForm


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    admin.init_app(app, url='/admin', index_view=HomeAdminView(name='Главная'))
    login_manager.init_app(app)
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    mail.init_app(app)
    bootstrap.init_app(app)

    from .views.main.views import main
    from .views.event.views import events
    from .views.arena.views import arenas
    from .views.artist.views import artists
    from .views.manager.views import managers
    from .views.login.views import logins
    from .views.tour.views import tours
    from .views.api.views import api
    from .views.security.views import security

    app.register_blueprint(main)
    app.register_blueprint(events)
    app.register_blueprint(arenas)
    app.register_blueprint(artists)
    app.register_blueprint(managers)
    app.register_blueprint(tours)
    app.register_blueprint(api)
    app.register_blueprint(security)

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

    @app.route('/document_profile/<filename>')
    @login_required
    def document_profile(filename):
        return send_from_directory(Config.UPLOAD_DOCUMENTS_PROFILES,
                                   filename)

    @app.route('/img_arena/<img>')
    @login_required
    def img_arena(img):
        return send_from_directory(Config.UPLOAD_PHOTO_ARENA,
                                   img)

    @app.route('/photo_artist/<filename>')
    def photo_artist(filename):
        return send_from_directory(Config.UPLOAD_PHOTO_ARTIST,
                                   filename)

    @app.route('/inspina/<path:filename>')
    def inspina(filename):
        return send_from_directory(Config.UPLOAD_ADMIN,
                                   filename)

    @app.context_processor
    def company_default():
        if current_user.is_authenticated:
            company_default = Company.query.get(current_user.settings.company_default_id)
            if not company_default:
                settings = Settings.query.get(current_user.settings_id)
                settings.company_default_id = current_user.company[0].id
                db.session.commit()
                company_default = Company.query.get(current_user.settings.company_default_id)
            # return dict(company_default=current_user.company[0])
            return dict(company_default=company_default)
        return dict(company_default=None)

    return app


from .models import *
from .model.equipment import *
from .model.menu import *
from .model.city import *

from .openweather import OpenWeather

weather = OpenWeather(appid=Config.APPID, db=db, model=Weather)


class AdminMixIn:
    def is_accessible(self):
        if current_user.is_anonymous:
            return False
        else:
            return 'admin' in current_user.roles

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminView(AdminMixIn, ModelView):
    pass


class HomeAdminView(AdminMixIn, AdminIndexView):
    pass


admin.add_view(AdminView(Tour, db.session))
admin.add_view(AdminView(Event, db.session))
admin.add_view(AdminView(Artist, db.session))
admin.add_view(AdminView(Arena, db.session))
admin.add_view(AdminView(TypeHall, db.session))
admin.add_view(AdminView(TypeEvent, db.session))
admin.add_view(AdminView(Menu, db.session))

admin.add_view(AdminView(EquipmentCategory, db.session))
admin.add_view(AdminView(Equipment, db.session))
admin.add_view(AdminView(Country, db.session))
admin.add_view(AdminView(Region, db.session))
admin.add_view(AdminView(City, db.session))
admin.add_view(AdminView(Weather, db.session))

admin.add_view(AdminView(Document, db.session))
admin.add_view(AdminView(CompanyType, db.session))
admin.add_view(AdminView(Company, db.session))

admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))
admin.add_view(AdminView(Confirmation, db.session))
admin.add_view(AdminView(Invite, db.session))
admin.add_view(AdminView(Settings, db.session))


# user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    error_log = Config.LOG_DIR.joinpath('error.log')
    file_heandler = logging.FileHandler(error_log)

    file_heandler.setFormatter(formatter)
    logger.addHandler(file_heandler)

    return logger


logger = setup_logger()


def allowed_photo_profile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_PHOTO


def allowed_document_profile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_DOCUMENT


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def generate_id():
    return str(uuid.uuid4())
