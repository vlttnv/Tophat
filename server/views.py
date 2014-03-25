from flask import render_template, request
from server import app
import os

@app.route('/')
@app.route('/index')
def index():
    return 'Hello World'

@app.route('/register', methods = ['POST'])
def register():
    id = request.form['id']
    location = request.form['location']
	return 'Registered'