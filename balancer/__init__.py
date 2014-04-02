from flask import Flask

balancer_app = Flask('balancer')

from balancer import views
