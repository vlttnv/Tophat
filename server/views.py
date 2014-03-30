from flask import render_template, request, abort, jsonify, g
from server import app, queue, db_manager
from server.exceptions import ProducerConnectionException, \
	ProducerIPNotFoundException, ProducerPortNotFoundException, \
	ProducerDataNotFoundException
from datetime import datetime
import time
import os
import sqlite3
import requests
import threading

ips={}
queue_heartbeat = queue.Queue(100)

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

	queue_heartbeat.add(producer)

	return 'Heartbeat added to the queue', 200

@app.route('/get_data/<int:producer_id>', methods=['GET'])
def get_data_producerID(producer_id):
    """
    Request data from the producer whose ID is producer_id.
    """

    print 'Request from', request.remote_addr, \
            ': retrieve data from producer', producer_id
    
    if request.remote_addr in ips and time.time() - ips[request.remote_addr] < 1:
        return 'Too many requsts from a single IP'

    if db_manager.exists_producer(producer_id) == False:
        ips[request.remote_addr] = time.time()
        return 'Producer does not exist.', 400
    else:
    	# try to get live data, or old data otherwise
        try:
            ips[request.remote_addr] = time.time()
            data = retrieve_data(producer_id)
            return data, 200
        except ProducerIPNotFoundException as err:
            return str(err) + 'Try again later.', 400
        except ProducerPortNotFoundException as err:
            return str(err) + 'Try again later.', 400
        except ProducerDataNotFoundException as err:
            return str(err) + 'Try again later.', 400

@app.route('/get_data_location/<location>', methods=['GET'])
def get_data_location(location):
	"""
	Request data from the location given. Match the requested location with
	the lastest timestamp.
	"""

	print 'Request from', request.remote_addr, \
			': retrieve data from location', location

	if db_manager.exists_location(location) == False:
		return 'No producer within the location.', 400
	else:
		data = db_manager.get_dataset_location(location)

		if data is None:
			return 'Dataset not found. Try again later.', 400
		else:
			return data, 200

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
	data_from_queue = queue_heartbeat.get(producer_id)

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

	data = db_manager.get_dataset(producer_id)

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
