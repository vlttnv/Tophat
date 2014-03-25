from flask import render_template, request, abort, jsonify, g
from server import app
from datetime import datetime
import os
import sqlite3

@app.route('/')
@app.route('/index')
def index():
    return 'Hello World'

@app.route('/heartbeat', methods = ['POST'])
def heartbeat():
    if not request.json or not ('id' and 'location' in request.json):
        return 'Heartbeat object not understood.\n', 400
        
    producer = {
        'ip': request.remote_addr,
        'id': request.json['id'],
        'location': request.json['location']
    }
    
    # updateDB(producer)

    return 'Heartbeat recorded', 200

@app.route('/get_location/<int:producer_id>', methods = ['GET'])
def get_location(producer_id):

    # getProducerLocation(producer_id)

    location = {
        'location': 'St Andrews'
    }

    return jsonify({ 'location': location }), 200

@app.route('/send', methods = ['POST'])
def receive():
    if not request.json or not ('id' and 'location' and 'data' in request.json):
        return 'Data object not understood.\n', 400

    data = {
        'id': request.json['id'],
        'location': request.json['location'],
        'data': request.json['data'],
        'timestamp': datetime.utcnow()
    }

    # updateDB(data)

    return 'Data recorded', 200
