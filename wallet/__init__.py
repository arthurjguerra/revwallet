import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import Config

logging.basicConfig(filename='/var/log/revwallet/revwallet.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

logger = logging.getLogger()

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        # test configuration
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping(
            SECRET_KEY='dev',
            SQLALCHEMY_DATABASE_URI=Config.DB_URI,
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )

    db.init_app(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        print(f'{app.instance_path} directory already exists.')

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp, url_prefix='/wallet')
        db.create_all()

    return app
