from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

worker_app = Flask('worker')
worker_app.config.from_object('config')

db = SQLAlchemy(worker_app)

from worker import views, models
