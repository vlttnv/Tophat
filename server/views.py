from flask import render_template, request
from server import app
import os

@app.route('/')
@app.route('/index')
def index():
    title = 'Home'
    return title