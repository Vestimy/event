import os
import inspect
import sys
from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    PATH = sys.path[0]
    FILENAME = inspect.getframeinfo(inspect.currentframe()).filename
    PATH_EVENTS = os.path.dirname(os.path.abspath(FILENAME))
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://vestimy:User1816!@localhost/mydb'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:user1816@touremanager.ru/mydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    UPLOAD_PHOTO_PROFILES = PATH_EVENTS + '/uploads/profiles'
    UPLOAD_ADMIN = PATH_EVENTS + '/static/inspina'
    UPLOAD_DOCUMENTS_PROFILES = PATH_EVENTS + '/uploads/documents'
    UPLOAD_PHOTO_ARENA = PATH_EVENTS + '/uploads/arena'
    UPLOAD_PHOTO_ARTIST = PATH_EVENTS + '/uploads/artist'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    ALLOWED_PHOTO = set(['png', 'jpg', 'jpeg', 'gif'])
    ALLOWED_DOCUMENT = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
    DEBUG = True
    SECRET_KEY = '26edec8e275e43cab5777cb9050906f9'
    ADMIN_PASSWD_HASH = '7ULJ61PMMGBJ1KWQB64P7D'
    STATIC_URL_PATH = '/static'
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 465
    # # MAIL_PORT = 587
    # MAIL_USE_SSL = True
    # MAIL_USE_TLS = False
    # MAIL_USERNAME = 'vestimyandrey@gmail.com'
    # MAIL_PASSWORD = 'ukjusrgneeolhmww'
    SECURITY_REGISTERABLE = True
    SECURITY_REGISTER_URL = '/create_account'
    SECURITY_USER_IDENTITY_ATTRIBUTES = ['email', 'login']
    SECURITY_POST_LOGIN_VIEW = '/index'
    SECURITY_POST_LOGOUT_VIEW = '/login'
    SECURITY_SEND_REGISTER_EMAIL = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    APPID = '7457f5e9ef9836778c2df4e92d173e3f'
