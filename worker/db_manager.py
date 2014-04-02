from worker import models, db
from sqlalchemy.exc import IntegrityError

def update_heartbeat(heartbeat):
	"""
	Update the heartbeat of a particular producer.

	Return True if the database has been updated, and False otherwise.

	Heartbeat format:
	{
		'id': producer ID (mobile phone unique ID),
		'location': location,
		'ip_address': ID address,
		'timestamp': timestamp,
		'data': data
	}
	"""

	records = models.Producer.query.filter_by(id=heartbeat['id'])

	# new producer
	if records is None or records.count() == 0:
		producer_new = models.Producer(
			id = heartbeat['id'],
			location = heartbeat['location'],
			ip_address = heartbeat['ip_address'],
			timestamp = heartbeat['timestamp'],
			data = heartbeat['data']
		)

		try:
			db.session.add(producer_new)
			db.session.commit()
			print 'Database update - Producer(New):', heartbeat['id']
			return True
		except IntegrityError as err:
			print 'Database error - Producer(New):', heartbeat['id']
			return False

	# update old heartbeat
	elif records.count() == 1:
		old_record = records.first()

		try:
			old_record.ip_address = heartbeat['ip_address']
			old_record.timestamp = heartbeat['timestamp']
			db.session.commit()
			print 'Database update - Producer:', heartbeat['id']
			return True
		except IntegrityError as err:
			print 'Database error - Producer:', heartbeat['id']
			return False

	else:
		print 'Database conflict - More than one prodcuer: ', heartbeat['id']
		return False

def get_dateset(producer_id):
	"""
	Retrieve data from the producer.

	Return the result if found, and None otherwise.
	"""

	if _exists_producer(producer_id) == False:
		print 'Database error - Producer not found:', producer_id
		return None
	else:
		heartbeat = models.Producer.query.filter_by(id=producer_id) \
					.order_by(models.Producer.timestamp.desc()).first()
		print 'Database retreival - Producer:', producer_id
		return heartbeat.data	

def get_dateset_location(location):
	"""
	Retrieve the most recent data from the location.

	Return the result if found, and None otherwise.
	"""

	if _exists_location(location) == False:
		print 'Database error - Location not found:', location
		return None
	else:
		heartbeat = models.Producer.query.filter_by(location=location) \
					.order_by(models.Producer.timestamp.desc()).first()
		print 'Database retreival - Location:', location
		return heartbeat.data

def _exists_producer(producer_id):
	"""
	Return True if a record of the producer exists in the database,
	and False otherwise
	"""

	result = models.Producer.query.filter_by(id=producer_id)

	if result is None or result.count() == 0:
		return False
	else:
		return True

def _exists_location(location):
	"""
	Return True if a record from the location exists in the database,
	and False otherwise
	"""

	result = models.Producer.query.filter_by(location=location)

	if result is None or result.count() == 0:
		return False
	else:
		return True
