from flask import render_template, request, abort, jsonify, g
from server import app, db_manager
from server.exceptions import ProducerConnectionException, \
    ProducerIPNotFoundException, ProducerPortNotFoundException, \
    ProducerDataNotFoundException
from datetime import datetime
import time
import os
import sqlite3
import requests
import threading

queue = {}
limit = 100

def size():
    return len(queue)

def isEmpty():
    return len(queue) == 0

def isFull():
    return len(queue) == limit

def add(producer):
    producer_id = producer['id']

    if isFull() and (producer_id not in queue):
        print 'Queue is full. Flushing.'
        flush()

    if producer_id in queue:
        print 'Updating pre-existing producer(' + str(producer_id) + \
                ')information in the queue.'
    else:
        print 'Adding a new producer(' + str(producer_id) + \
                ')infromation to the queue.'

    queue[producer_id] = producer

def remove(producer):
    if isEmpty():
        print 'Queue is empty.'
        return False
    else:
        producer_id = producer['id']

        if producer_id in queue:
            return True

def get(producer_id):
    if producer_id in queue:
        print 'Producer(' + str(producer_id) + \
                ')information is in the queue.'
        return queue[producer_id]
    else:
        print 'Producer(' + str(producer_id) + \
                ')information is not in the queue.'
        return None

def flush():
    for key, value in queue_heartbeat.iteritems():
        updated_heartbeat = db_manager.update_heartbeat(value)

        if updated_heartbeat:
            print 'Heartbeat recorded for producer:', key
        else:
            print 'Heartbeat not recorded for producer:', key

@app.route('/')
@app.route('/index')
def index():
    return 'Hello World'

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
    """
    Register the sender as a producer.
    """

    print 'Request from', request.remote_addr, ': register a heartbeat.'

    if not request.json or not ('port' and 'id' and 'location' in request.json):
        return 'Heartbeat object not understood.', 400

    producer = {
        'id': int(request.json['id']),
        'location': request.json['location'],
        'ip_address': request.remote_addr,
        'timestamp': datetime.utcnow(),
        'port': int(request.json['port'])
    }

    add(producer)

    return 'Heartbeat added to the queue', 200

    # updated_heartbeat = db_manager.update_heartbeat(producer)

    # if updated_heartbeat:
    #     return 'Heartbeat recorded. Time: ' + str(time.time()), 200
    # else:
    #     return 'Heartbeat not recorded. Try again later.', 400

@app.route('/get_data/<int:producer_id>', methods=['GET'])
def get_data(producer_id):
    """
    Request data from the producer whose ID is producer_id
    """

    print 'Request from', request.remote_addr, \
            ': retrieve data from producer', producer_id

    # check db
    if db_manager.exists_producer(producer_id) == False:
        return 'Producer does not exist', 400

    else:
        try:
            data = retrieve_data(producer_id)
            return data, 200
        except ProducerIPNotFoundException as err:
            return str(err) + 'Try again later.', 400
        except ProducerPortNotFoundException as err:
            return str(err) + 'Try again later.', 400
        except ProducerDataNotFoundException as err:
            return str(err) + 'Try again later.', 400

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

    # check live data
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
    except ProducerConnectionException:
        pass

    # check queue
    data_from_queue = get(producer_id)

    if data_from_queue is not None:
        return data_from_queue

    # check db
    try:
        data = get_old_data(producer_id)
        return data
    except ProducerDataNotFoundException:
        raise

def get_live_data(producer_addr, producer_port):
    """
    Retrieve live data from the producer @ producer_addr:producer_port

    Timeout after 10 seconds
    """

    print 'Asking live data from producer @ ' + \
        str(producer_addr) + ':' + str(producer_port)

    timeout = 10

    try:
        r = requests.get(
            'http://' + str(producer_addr) + ':' + str(producer_port),
            timeout=timeout)
        return r.text
    except requests.exceptions.Timeout:
        print 'Failed to get live data - request timeout.'
        raise ProducerConnectionException()
    except requests.exceptions.ConnectionError:
        print 'Failed to connect to the producer'
        raise ProducerConnectionException()

def get_old_data(producer_id):
    """
    Retrieve old data from the database
    """

    print 'Asking old data from the database'

    data = db_manager.get_latest_dataset(producer_id)

    if data is not None:
        return data
    else:
        print 'Failed to get old data - not in database.'
        raise ProducerDataNotFoundException()

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