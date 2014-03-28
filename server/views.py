from flask import render_template, request, abort, jsonify, g
from server import app, db_manager, exceptions
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
    Producer registers with the broker
    """

    if not request.json or not ('port' and 'id' and 'location' in request.json):
        return 'Heartbeat object not understood.', 400
    
    producer_addr = request.remote_addr
    producer_port = request.json['port']
    producer_id = request.json['id']
    producer_location = request.json['location']

    print 'Request from', producer_addr, ': register a heartbeat.'

    if type(producer_port) is not int:
        return 'Producer id must be an integer.', 400

    if type(producer_id) is not int:
        return 'Producer port must be an integer.', 400

    producer = {
        'ip': producer_addr,
        'port': int(producer_port),
        'id': int(producer_id),
        'location': producer_location,
        'timestamp': datetime.utcnow()
    }

    updated_heartbeat = db_manager.update_heartbeat(producer)

    if updated_heartbeat:
        return 'Heartbeat recorded.', 200
    else:
        return 'Heartbeat not recorded. Try again later.', 400

@app.route('/get_data/<int:producer_id>', methods=['GET'])
def get_data(producer_id):
    """
    Consumer requests data from a producer
    """

    print 'Request from', request.remote_addr, + \
            ': retrieve data from producer', producer_id

    if db_manager.exists_producer(producer_id) == False:
        return 'Producer does not exist', 400

    else:
        #add consumer to the queue

        try:
            data = retrieve_data(producer_id)
            return data, 200
        except ProducerIPNotFoundException:
            return 'Cannot find producer\'s IP address. Try again later.', 400
        except ProducerPortNotFoundException:
            return 'Cannot find producer\'s port number. Try again later.', 400
        except ProducerTimeoutException:
            return 'Request to the producer timeout\'d. Try again later.', 400

def retrieve_data(producer_id):
    """
    Retrieve the most recent data from the producer
    """

    print 'Getting live data from producer', producer_id

    producer_addr = db_manager.get_producer_ip(producer_id)
    producer_port = db_manager.get_producer_port(producer_id)

    if producer_addr is None:
        raise ProducerIPNotFoundException()

    if producer_port is None:
        raise ProducerPortNotFoundException()

    print 'Found producer IP address:', producer_ip, + \
            'and port number:', producer_port

    try:
        data = get_live_data(producer_ip, producer_port)

        dataset_new = {
            'id': producer_id + int(time.time()),
            'producer_id': producer_id,
            'data': data,
            'timestamp': datetime.utcnow()
        }

        # update DB
        db_manager.add_dataset(dataset_new)

        return data

    except ProducerTimeoutException:
        raise

def get_live_data(producer_ip, producer_port):
    """
    Retrieve live data from the producer (id=producer_id, ip=producer_ip)

    Timeout after 10 seconds
    """

    timeout = 10

    try:
        r = requests.get(
            'http://' + producer_ip + producer_port,
            timeout=timeout)
        return r.text
    except requests.exceptions.Timeout:
        raise ProducerTimeoutException()

@app.route('/send', methods=['POST'])
def receive():
    """
    Receive data from the producers
    """

    if not request.json or not ('producer_id' and 'data' in request.json):
        return 'Data object not understood.\n', 400
    
    print 'Request from', request.remote_addr, ': send data'

    dataset = {
        'id': request.json['producer_id'] + int(time.time()),
        'producer_id': request.json['producer_id'],
        'data': request.json['data'],
        'timestamp': datetime.utcnow()
    }

    updated = db_manager.add_dataset(dataset)

    if updated:
        return 'Data recorded', 200
    else:
        return 'Data not recorded. Try again later', 400