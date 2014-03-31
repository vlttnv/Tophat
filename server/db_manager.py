from server import models, db
from sqlalchemy.exc import IntegrityError
import time

def update_heartbeat(producer):
	"""
	Update the producer's IP address, port, and timestamp.

	Add a new record of the producer to the database if it does not already
	exists.

	Return True if the database has been updated, and False otherwise.

	Producer format:
	{
		'id': producer ID (mobile phone unique ID),
		'location': location,
		'ip_address': ID address,
		'timestamp': timestamp,
		'data': data
	}
	"""

	producers = models.Producer.query.filter_by(id=producer['id'])
	producers_count = producers.count()

	if producers_count == 0:
		# add a new producer
		producer_new = models.Producer(
			id = producer['id'],
			location = producer['location'],
			ip_address = producer['ip_address'],
			timestamp = producer['timestamp'],
			data = producer['data']
		)

		try:
			db.session.add(producer_new)
			db.session.commit()
			print 'Added new producer:', producer['id']
			return True

		except IntegrityError as err:
			print 'Failed to add a new producer:', producer['id']
			return False

	elif producers_count == 1:
		# update producer info
		producer_old = producers.first()

		try:
			# update ip & timestamp
			producer_old.ip_address = producer['ip_address']
			producer_old.timestamp = producer['timestamp']
			db.session.commit()
			print 'Updated heartbeat for producer:', producer['id']
			return True

		except IntegrityError as err:
			print 'Failed to update heartbeat for producer:', producer['id']
			return False

	else:
		print 'Found more than one producer with the same id:', producer['id']
		return False


def add_dataset(dataset):
	"""
	Add producer data to the database.

	Return True if successful, and False otherwise.

	Dataset format:
	{
		'id': dataset ID
		'producer_id': producer ID (mobile phone unique ID),
		'data': data,
		'timestamp': timestamp
	}
	"""

	dataset_new = models.ProducerDataSet(
		id = dataset['id'],
		producer_id = dataset['producer_id'],
		data = dataset['data'],
		timestamp = dataset['timestamp']
	)

	try:
		db.session.add(dataset_new)
		db.session.commit()
		print 'Added new dataset:', dataset['id'], \
			'. Data: ', dataset['data']
		return True

	except IntegrityError as err:
		print 'Failed to add dataset:', dataset['id'], \
			'. Data: ', dataset['data']
		return False

def get_heartbeat(producer_id):
	"""
	Retrieve heartbeat information from the producer.

	Return None if there is no match found.
	"""

	heartbeat = models.Producer.query.filter_by(id=producer_id) \
				.order_by(models.Producer.timestamp.desc()).first()

	if heartbeat is None:
		print 'Failed to find heartbeat of producer:', producer_id
		return None
	else:
		print 'Found heartbeat of producer:', producer_id
		return heartbeat.data

def get_dataset(producer_id):
	"""
	Retrieve the most recent data uploaded from the producer.

	Return None if there is no match found.
	"""

	dataset = models.ProducerDataSet.query.filter_by(producer_id=producer_id) \
				.order_by(models.ProducerDataSet.timestamp.desc()).first()

	if dataset is None:
		print 'Dataset not found'
		return None
	else:
		print 'Found dataset:', dataset.id
		return dataset.data

def get_dateset_location(location):
	"""
	Retrieve the most recent data from the location.

	Return None if no match found
	"""

	dataset = models.ProducerDataSet.query.filter_by(location=location) \
				.order_by(models.ProducerDataSet.timestamp.desc()).first()

	if dataset is None:
		print 'Dataset not found'
		return None
	else:
		print 'Found dataset:', dataset.id
		return dataset.data

def generate_dataset_id(producer_id):
	"""
	Generate a unique ID for a dataset

	"""
	new_id = int(producer_id) + int(time.time())
	return new_id

def exists_producer(producer_id):
	"""
	Return True if a record of the producer exists in the database,
	and False otherwise
	"""

	if models.Producer.query.filter_by(id=producer_id).count() > 0:
		return True
	else:
		return False

def exists_location(location):
	"""
	Return True if a record of the producer from the location exists in the
	database, and False otherwise
	"""

	if models.Producer.query.filter_by(location=location).count() > 0:
		return True
	else:
		return False

def get_producer_ip(producer_id):
	"""
	Retrieve the producer IP address from the ID.

	Return None if there is no match or one than one match.
	"""

	producers = models.Producer.query.filter_by(id=producer_id)
	producers_count = producers.count()

	if producers_count == 0:
		print 'Producer not found.'
		return None
	elif producers_count > 1:
		print 'Found more than one producer.'
		return None
	else:
		# use the first row for now
		ip_address = producers.first().ip_address

		print 'Found producer:', producer_id, 'IP address:', ip_address
		return ip_address

def get_producer_port(producer_id):
	"""
	Retrieve the producer port from the ID

	Return None if there is no match or one than one match.
	"""

	producers = models.Producer.query.filter_by(id=producer_id)
	producers_count = producers.count()

	if producers_count == 0:
		print 'Producer not found.'
		return None
	elif producers_count > 1:
		print 'Found more than one producer.'
		return None
	else:
		# use the first row for now
		port_number = producers.first().port

		print 'Found producer:', producer_id, 'port number:', port_number
		return port_number
