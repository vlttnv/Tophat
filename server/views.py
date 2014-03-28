from flask import render_template, request, abort, jsonify, g
from server import app, db_manager
from server.exceptions import ProducerTimeoutException, \
    ProducerIPNotFoundException, ProducerPortNotFoundException, \
    ProducerDataNotFoundException
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

    print 'Request from', request.remote_addr, ': register a heartbeat.'

    if not request.json or not ('port' and 'id' and 'location' in request.json):
        return 'Heartbeat object not understood.', 400

    producer = {
        'ip': request.remote_addr,
        'port': int(request.json['port']),
        'id': int(request.json['id']),
        'location': request.json['location'],
        'timestamp': datetime.utcnow()
    }

    print 'heartbeat port:', producer['port']

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

    print 'Request from', request.remote_addr, \
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
        except ProducerDataNotFoundException:
            return 'Cannot retreive data. Try again later.', 400

def retrieve_data(producer_id):
    """
    Retrieve the most recent data from the producer
    """

    print 'Retrieving data from producer:', producer_id

    producer_addr = db_manager.get_producer_ip(producer_id)
    producer_port = db_manager.get_producer_port(producer_id)

    if producer_addr is None:
        raise ProducerIPNotFoundException()

    if producer_port is None:
        raise ProducerPortNotFoundException()

    try:
        data = get_live_data(producer_addr, producer_port)

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
        print 'Failed to get live data, looking into the database'

        data = db_manager.get_latest_dataset(producer_id)

        if data is not None:
            return data
        else:
            print 'Failed to get old data'
            raise ProducerDataNotFoundException()

def get_live_data(producer_addr, producer_port):
    """
    Retrieve live data from the producer producer_addr:producer_port

    Timeout after 10 seconds
    """

    print 'Asking for live data from producer:' + \
        str(producer_addr) + ':' + str(producer_port)

    timeout = 10

    try:
        r = requests.get(
            'http://' + str(producer_addr) + ':' + str(producer_port),
            timeout=timeout)
        return r.text
    except requests.exceptions.Timeout:
        raise ProducerTimeoutException()

@app.route('/send', methods=['POST'])
def receive():
    """
    Receive data from the producers
    """

    print 'Request from', request.remote_addr, ': send data'

    if not request.json or not ('producer_id' and 'data' in request.json):
        return 'Data object not understood.\n', 400

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