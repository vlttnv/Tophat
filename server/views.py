from flask import render_template, request, abort, jsonify, g
from server import app, models, db
from datetime import datetime
import time
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
    # -check if producer exists
    # --if not create new producer
    # --otherwise query db for user id
    # --and modify timestap
    if models.Producer.query.filter_by(id=request.json['id']).count() == 0:
	    prd = models.Producer(id=request.json['id'],location=request.json['location'],ip_address="null",timestamp=11)
	    db.session.add(prd)
	    db.session.commit()
	    print "Added new user"
    else:
	    prd = models.Producer.query.filter_by(id=request.json['id']).first()
	    prd.timestamp = 11
	    db.session.commit()
	    print "Heartbeat for producer id" + request.json['id'] 

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

    now = datetime.utcnow()
    epoch = time.time()

    # updateDB(data)
    data_set = models.ProducerDataSet(id=int(request.json['id']) + int(time.time()), producer_id=request.json['id'], data=request.json['data'], time_stamp=now)
    db.session.add(data_set)
    db.session.commit()

    return 'Data recorded', 200
