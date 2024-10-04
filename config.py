import os

class Config:
    SECRET_KEY = os.environ.get('kessy') or 'kessy'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1978@localhost:3307/flask_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
