import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
  DB_NAME = os.environ.get('DB_NAME')
  DB_HOST = os.environ.get('DB_HOST')
  DB_USERNAME = os.environ.get('DB_USERNAME')
  DB_PASSWORD = os.environ.get('DB_PASSWORD')
  DB_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
