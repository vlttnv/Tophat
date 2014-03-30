from flask import Flask
from balancer import views
app = Flask(__name__, static_url_path='/static')
