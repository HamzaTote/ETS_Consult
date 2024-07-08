import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://erpbet_ad:123456@localhost:3306/erpbet_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
app.config.from_object(Config)