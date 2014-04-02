from worker import db_manager

class Cache:

	def __init__(self, limit):
		self.limit = limit
		self.cache = {}

	def size(self):
		return len(self.cache)

	def isEmpty(self):
		return len(self.cache) == 0

	def isFull(self):
		return len(self.cache) == self.limit

	def add(self, heartbeat):
		"""
		Add heartbeat to the cache. Flush the contents to the database if the
		cache is full.
		"""

		producer_id = heartbeat['id']
		
		if self.isFull() and (producer_id not in self.cache):
			print 'Cache is full. Flushing.'
			self.flush()

		if producer_id in self.cache:
			print 'Cache update - Producer:', producer_id
		else:
			print 'Cache update - Producer(New):', producer_id

		self.cache[producer_id] = heartbeat

	def get(self, producer_id):
		if producer_id in self.cache:
			return self.cache[producer_id]
		else:
			return None

	def flush(self):
		"""
		Flush producer heartbeats to the database.
		"""

		for key, value in self.cache.iteritems():
			updated_heartbeat = db_manager.update_heartbeat(value)

			if updated_heartbeat:
				print 'Database update - Heartbeat: ' + str(value)
			else:
				print 'Database update error: - Heartbeat: ' + str(value)

		# clear half of the cache
		if self.isFull():
			cache_new = dict(self.cache.items()[len(self.cache)/2:])
			self.cache = cache_new
