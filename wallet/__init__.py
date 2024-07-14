import os

from flask import Flask
from wallet.wallet import db
import wallet.app as app_routes

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
        db.create_all()

    app.register_blueprint(app_routes.bp)

    return app
