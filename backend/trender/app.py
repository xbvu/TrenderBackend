# -*- coding: utf-8 -*-

import os

from flask import Flask

from trender.config import DefaultConfig
from trender.extensions import db
from trender.utils import make_dir, INSTANCE_FOLDER_PATH
from flask_cors import CORS, cross_origin

# For import *
__all__ = ['create_app']


def create_app(config=None, app_name=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = DefaultConfig.PROJECT
    make_dir(INSTANCE_FOLDER_PATH)

    app = Flask(app_name, instance_path=INSTANCE_FOLDER_PATH,
                instance_relative_config=True)
    cors = CORS(app)
    configure_app(app, config)
    configure_hook(app)
    configure_blueprints(app)
    configure_logging(app)
    configure_extensions(app)
    return app


def configure_app(app, config=None):
    """Different ways of configurations."""

    # http://flask.pocoo.org/docs/api/#configuration
    app.config.from_object(DefaultConfig)

    # http://flask.pocoo.org/docs/config/#instance-folders
    app.config.from_pyfile('production.cfg', silent=True)

    if config:
        app.config.from_object(config)

    # Use instance folder instead of env variables to make deployment easier.
    # app.config.from_envvar('%s_APP_CONFIG' % DefaultConfig.PROJECT.upper(),
    # silent=True)


def configure_extensions(app):
    # flask-sqlalchemy setup
    db.init_app(app)
    
    # database_path = app.config['SQLALCHEMY_DATABASE_URI']
    database_path = INSTANCE_FOLDER_PATH+'/sources.sqlite'
    if not os.path.exists(database_path):
        print("Database file not found on '{}'. Creating a database.".format(database_path))
        app.logger.info("Database file not found on '{}'. Creating a database.".format(database_path))
        with app.app_context():
            db.drop_all()
            db.create_all()
    else:
        print("Database found on '{}'.".format(database_path))
        app.logger.info("Database found on '{}'.".format(database_path))
    return


def configure_blueprints(app):
    """Configure blueprints in views."""

    from trender.api import api

    for bp in [api]:
        app.register_blueprint(bp)

def configure_logging(app):
    """Configure file(info)"""

    if app.debug or app.testing:
        # Skip debug and test mode. Just check standard output.
        return

    import logging
    import os

    from trender.utils import make_dir
    from logging.handlers import RotatingFileHandler
    
    # Set info level on logger, which might be overwritten by handers.
    # Suppress DEBUG messages.
    app.logger.setLevel(logging.INFO)

    info_log = os.path.join(app.config['LOG_FOLDER'])
    make_dir(info_log)
    
    info_file_handler = RotatingFileHandler(
        info_log+"/info.log", maxBytes=100000, backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(info_file_handler)

    # Testing
    # print("Testing logging")
    # app.logger.info("testing info.")
    # app.logger.warn("testing warn.")
    # app.logger.error("testing error.")


def configure_hook(app):

    @app.before_request
    def before_request():
        pass


