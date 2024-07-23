import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        # test configuration
        app.config.from_mapping(test_config)
    else:
        # production configuration
        db_name = os.environ.get('DB_NAME')
        db_host = os.environ.get('DB_HOST')
        db_username = os.environ.get('DB_USERNAME')
        db_password = os.environ.get('DB_PASSWORD')
        db_uri = f"postgresql://{db_username}:{db_password}@{db_host}/{db_name}"

        app.config.from_mapping(
            SECRET_KEY='dev',
            SQLALCHEMY_DATABASE_URI=db_uri,
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
