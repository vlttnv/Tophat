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
    """
    Consumer registers with the broker
    """

    if not request.json or not ('id' and 'location' in request.json):
        return 'Heartbeat object not understood.', 400
    
    producer = {
        'ip': request.remote_addr,
        'id': int(request.json['id']),
        'location': request.json['location'],
        'timestamp': datetime.utcnow()
    }

    print 'Producer', request.remote_addr, 'registering a heartbeat'

    updated = dbManager.updateHeartBeat(producer)

    if updated:
        return 'Heartbeat recorded', 200
    else:
        return 'Heartbeat not recorded. Try again later.', 400

@app.route('/get_data/<int:producer_id>', methods=['GET'])
def get_data(producer_id):
    """
    Consumer requests data from a producer
    """

    print 'Consumer', request.remote_addr, 'looking for producer:', producer_id

    if dbManager.doesProducerExist(producer_id) == False:
        return 'Producer does not exist', 400

    else:
        #add consumer to the queue

        producer_ip = dbManager.getProducerIP(producer_id)

        if producer_ip is None:
            return 'Cannot find producer\'s IP address. Try again later', 400
        else:
            print 'Found producer IP address:', producer_ip
            return handle_data_request(producer_id, producer_ip)

def handle_data_request(producer_id, producer_ip):
    """
    Get data from the producer and return it
    """

    data = get_live_data_from_producer(producer_id, producer_ip)

    if data is None:
        return 'Requests timeout', 400

    dataset_new = {
        'id': producer_id + int(time.time()),
        'producer_id': producer_id,
        'data': data,
        'timestamp': datetime.utcnow()
    }

    # update DB
    dbManager.addProducerData(dataset_new)

    return data, 200

def get_live_data_from_producer(producer_id, producer_ip):
    """
    Retrieve live data from the producer
    """
    try:
        # timeout after 10 seconds
        r = requests.get('http://' + producer_ip + ':9000', timeout=10)
        return r.text
    except requests.exceptions.Timeout:
        print 'Requests timeout from producer:', producer_id
        return None

@app.route('/send', methods=['POST'])
def receive():
    """
    Receive data from the producers
    """

    if not request.json or not ('producer_id' and 'data' in request.json):
        return 'Data object not understood.\n', 400

    # id = custom identifier for the dataset
    dataset = {
        'id': request.json['producer_id'] + int(time.time()),
        'producer_id': request.json['producer_id'],
        'data': request.json['data'],
        'timestamp': datetime.utcnow()
    }

    updated = dbManager.addProducerData(dataset)

    if updated:
        return 'Data recorded', 200
    else:
        return 'Data not recorded. Try again later', 400