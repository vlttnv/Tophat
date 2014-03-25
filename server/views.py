from flask import render_template, request, abort, jsonify
from server import app
import os

@app.route('/')
@app.route('/index')
def index():
    return 'Hello World'

@app.route('/register', methods = ['POST'])
def register():
    if not request.json or not 'id' and 'location' in request.json:
        abort(400)
        
    producer = {
        'id': request.json['id'],
        'location': request.json['location']
    }

    print producer
    
    return jsonify( { 'producer': producer } ), 201