import os

class Config:
    SECRET_KEY = os.environ.get('blessedbeHibbardsClass23') or 'a hard to guess string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///elevate.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
