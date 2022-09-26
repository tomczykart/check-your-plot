from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
from flask_login import LoginManager

#create flask instance
app = Flask(__name__)
app.config.from_object(Config)

#create database instance
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#initialize LoginMenager extension
login = LoginManager(app)

from app import routes, models
