from flask import request
from server import worker_app, cache, db_manager
from server.exceptions import ProducerConnectionException, \
	ProducerIPNotFoundException, ProducerPortNotFoundException, \
	ProducerDataNotFoundException
from datetime import datetime
import threading
import time

cache_heartbeat = cache.Cache(10)

def update_DB():
	try:
		print 'why why why'
		cache_heartbeat.flush()
		# every hour
		thread = threading.Timer(2, update_DB)
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
def heartbeat():
	"""
	Register the sender as a producer.
	"""

	print 'Request from', request.remote_addr, ': register a heartbeat.'

	if not request.json:
		return 'Heartbeat object must be in json format.', 400

	if not ('port' and 'id' and 'location' and 'data' in request.json):
		return 'Heartbeat object not understood.', 400

	producer = {
		'id': int(request.json['id']),
		'location': request.json['location'],
		'ip_address': request.remote_addr,
		'timestamp': datetime.utcnow(),
		'data': request.json['data']
	}

	cache_heartbeat.add(producer)

	return 'Heartbeat added to the cache', 200

@worker_app.route('/get_data/<int:producer_id>', methods=['GET'])
def get_data_producerID(producer_id):
	"""
	Request data from the producer whose ID is producer_id.
	"""

	print 'Request from', request.remote_addr, \
			': retrieve data from producer', producer_id

	try:
		data = retrieve_data(producer_id)
		return data, 200
	except ProducerDataNotFoundException as err:
		return str(err) + 'Try again later.', 400

@worker_app.route('/get_data_location/<location>', methods=['GET'])
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

		if data is not None:
			return data, 200
		else:
			return 'Dataset not found. Try again later.', 400

def retrieve_data(producer_id):
	"""
	Retrieve the most recent data from the producer
	"""

	print 'Retrieve data from the cache.'

	# check cache
	producer_info = cache_heartbeat.get(producer_id)

	if producer_info is not None:
		return producer_info['data']

	# check db
	print 'Retrieve old data from the database'

	data = db_manager.get_dateset(producer_id)

	if data is not None:
		return data
	else:
		print 'Failed to retrieve old data'
		raise ProducerDataNotFoundException()
