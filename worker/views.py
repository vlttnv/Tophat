from flask import request
from worker import worker_app, cache, db_manager
from datetime import datetime
import threading
import time
import requests

cache_heartbeat = cache.Cache(100)

def update_DB():
	try:
		print 'Update Database'
		cache_heartbeat.flush()
		# every hour
		thread = threading.Timer(3600, update_DB)
		thread.daemon = True
		thread.start()
	except KeyboardInterrupt, SystemExit:

		pass

update_DB()

@worker_app.route('/')
@worker_app.route('/index')
def index():
	return 'Hello world, I am a worker.'

@worker_app.route('/heartbeat', methods=['POST'])
def post_heartbeat():
	"""
	Receive a heartbeat from a producer.
	"""

	print 'Request from', request.remote_addr, ': register a heartbeat.'

	if not request.json:
		return 'Heartbeat object must be in json format.', 400

	if not ('port' and 'id' and 'location' and 'data' in request.json):
		return 'Heartbeat object must contain ' + \
					'\'id\', \'location\', and \'data\'.', 400

	heartbeat = {
		'id': int(request.json['id']),
		'location': request.json['location'],
		'ip_address': request.remote_addr,
		'timestamp': datetime.utcnow(),
		'data': request.json['data']
	}

	cache_heartbeat.add(heartbeat)

	return 'Producer(' + str(heartbeat['id']) + ') heartbeat updated', 200

@worker_app.route('/get_data/<int:producer_id>', methods=['GET'])
def get_data_producerID(producer_id):
	"""
	Send producer data to the consumer.
	"""

	print 'Request from', request.remote_addr, \
			': retrieve data from producer', producer_id

	data = _retrieve_data(producer_id)

	if data is not None:
		return data, 200
	else:
		return 'Error - Data not found. Try again later.', 400

@worker_app.route('/get_data_location/<location>', methods=['GET'])
def get_data_location(location):
	"""
	Request data from the location given. Match the requested location with
	the lastest timestamp.
	"""

	print 'Request from', request.remote_addr, \
			': retrieve data from location', location

	data = db_manager.get_dataset_location(location)

	if data is not None:
		return data, 200
	else:
		return 'Error - Data not found. Try again later.', 400

def _retrieve_data(producer_id):
	"""
	Retrieve the most recent data from the producer.
	"""

	print 'Retrieve data from the cache.'

	# check cache
	heartbeat = cache_heartbeat.get(producer_id)
	if heartbeat is not None:
		return heartbeat['data']

	# check db
	print 'Retrieve data from the database.'

	data = db_manager.get_dateset(producer_id)
	if data is not None:
		return data

	return None
