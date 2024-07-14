import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(app.instance_path, "wallet.db")}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    if test_config:
        # test configuration
        app.config.from_mapping(test_config)
    else:
        # production configuration
        app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        print(f'{app.instance_path} directory already exists.')

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)
        db.create_all()

    return app
