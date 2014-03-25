from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')
db = SQLAlchemy(app)

from server import views, models
