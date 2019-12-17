import os

from trender.utils import make_dir, INSTANCE_FOLDER_PATH


class BaseConfig(object):
    PROJECT = "TrenderBackend"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    DEBUG = False
    
    SECRET_KEY = 'secret key'
    
    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, 'logs')


class DefaultConfig(BaseConfig):

    DEBUG = False

    # http://packages.python.org/Flask-SQLAlchemy/config.html
    SQLALCHEMY_ECHO = True
    # QLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be
    # disabled by default in the future.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLITE for prototyping.
    SQLALCHEMY_DATABASE_URI='sqlite:///'+INSTANCE_FOLDER_PATH+'/sources.sqlite'
    
    # MYSQL for production.
    
    # SQLALCHEMY_DATABASE_URI =
    # 'mysql://username:password@server/db?charset=utf8'
    
