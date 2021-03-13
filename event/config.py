import os
import inspect
import sys
from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    LOG_DIR = BASE_DIR.joinpath('log')
    PROJECT_DIR = BASE_DIR.joinpath('event')
    UPLOADS = PROJECT_DIR.joinpath('uploads')
    PROJECT_STATIC = PROJECT_DIR.joinpath('static')
    ###########DATABASE##################
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://vestimy:User1816!@localhost/mydb'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://vestimy:User1816!@touremanager.ru/mydb'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:user1816@touremanager.ru/mydb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #####################################
    UPLOAD_FOLDER = 'uploads'
    UPLOAD_PHOTO_PROFILES = UPLOADS.joinpath('profiles')
    UPLOAD_ADMIN = PROJECT_STATIC.joinpath('inspina')
    UPLOAD_DOCUMENTS_PROFILES = UPLOADS.joinpath('documents')
    UPLOAD_PHOTO_ARENA = UPLOADS.joinpath('arena')
    UPLOAD_PHOTO_ARTIST = UPLOADS.joinpath('artist')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    ALLOWED_PHOTO = set(['png', 'jpg', 'jpeg', 'gif'])
    ALLOWED_DOCUMENT = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
    #####################################
    SECRET_KEY = '26edec8e275e43cab5777cb9050906f9'
    ADMIN_PASSWD_HASH = '7ULJ61PMMGBJ1KWQB64P7D'
    STATIC_URL_PATH = '/static'
    #############MAIL#######################
    #MAIL_SERVER = 'smtp.gmail.com'
    #MAIL_PORT = 25
    #MAIL_USE_SSL = True
    #MAIL_USE_TLS = False
    #MAIL_USERNAME = 'vestimyandrey@gmail.com'
    #MAIL_PASSWORD = 'yzumcatxtiwatzvp'
    MAIL_ASCII_ATTACHMENTS = False
    
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    #############WEATHER#####################
    APPID = '7457f5e9ef9836778c2df4e92d173e3f'
