from flask import render_template, request, abort, jsonify, g
from server import app, dbManager
from datetime import datetime
import time
import os
import sqlite3
import requests
import threading

@app.route('/')
@app.route('/index')
def index():
    return 'Hello World'

@app.route('/heartbeat', methods=['POST'])
def heartbeat():

    if not request.json or not ('id' and 'location' in request.json):
        return 'Heartbeat object not understood.', 400
    
    producer = {
        'ip': request.remote_addr,
        'id': int(request.json['id']),
        'location': request.json['location'],
        'timestamp': datetime.utcnow()
    }

    updated = dbManager.updateHeartBeat(producer)

    if updated:
        return 'Heartbeat recorded', 200
    else:
        return 'Heartbeat not recorded. Try again later.', 400

@app.route('/get_data/<int:producer_id>', methods=['GET'])
def get_data(producer_id):

    if dbManager.doesProducerExist(producer_id) == False:
        return 'Producer does not exist', 400

    else:
        #add consumer to the queue

        producer_ip = dbManager.getProducerIP(producer_id)

        if producer_ip is None:
            return 'Cannot find producer\'s IP address. Try again later', 400

        fire_data_request(producer_ip)

        check_response = threading.Timer(1000.0, check_producer_response,
            [producer_id, request.remote_addr])
        check_response.start()

    location = {
        'location': 'St Andrews'
    }

    return jsonify({'location': location}), 200

@app.route('/send', methods=['POST'])
def receive():
    if not request.json or not ('producer_id' and 'data' in request.json):
        return 'Data object not understood.\n', 400

    # id = custom identifier for the package
    package = {
        'id': request.json['producer_id'] + int(time.time()),
        'producer_id': request.json['producer_id'],
        'data': request.json['data'],
        'timestamp': datetime.utcnow()
    }

    updated = dbManager.addProducerData(package)

    if updated:
        return 'Data recorded', 200
    else:
        return 'Data not recorded. Try again later', 400

def fire_data_request(producer_ip):
    requests.get('http://' + producer_ip + '/get_data')

def fire_data_response(producer_data, request_ip):
    requests.post("http://" + requests_ip + "/send_data", data=producer_data)

def check_producer_response(producer_id, resquest_ip):
    """
    Get latest producer data, check timestamp, and then decided whether to send
    it back to the consumer
    """

    producer_data = dbManager.getProducerData(producer_id)

    # check timestamp

    fire_data_response(producer_data, request_ip)