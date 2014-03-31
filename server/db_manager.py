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

def get_dateset(producer_id):
	"""
	Retrieve heartbeat information from the producer.

	Return None if there is no match found.
	"""

	if _exists_producer(producer_id) == False:
		'Failed to find producer:', producer_id
		return None

	heartbeat = models.Producer.query.filter_by(id=producer_id) \
				.order_by(models.Producer.timestamp.desc()).first()
	print 'Found heartbeat for the given producer:', producer_id
	return heartbeat.data	

def get_dateset_location(location):
	"""
	Retrieve the most recent data from the location.

	Return None if no match found.
	"""

	if _exists_location(location) == False:
		'Failed to find location:', location
		return None

	heartbeat = models.Producer.query.filter_by(location=location) \
				.order_by(models.Producer.timestamp.desc()).first()
	print 'Found heartbeat for the given location:', location
	return heartbeat.data

def _exists_producer(producer_id):
	"""
	Return True if a record of the producer exists in the database,
	and False otherwise
	"""

	if models.Producer.query.filter_by(id=producer_id).count() > 0:
		return True
	else:
		return False

def _exists_location(location):
	"""
	Return True if a record of the producer from the location exists in the
	database, and False otherwise
	"""

	if models.Producer.query.filter_by(location=location).count() > 0:
		return True
	else:
		return False