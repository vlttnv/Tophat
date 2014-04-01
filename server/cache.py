from server import db_manager

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

	def add(self, producer):
		producer_id = producer['id']

		if self.size == limit / 2:
			print 'Cache is half full. Flushing.'
			self.flush()

		if self.isFull() and (producer_id not in self.cache):
			print 'Cache is full. Flushing.'
			self.flush()

		if producer_id in self.cache:
			print 'Updating pre-existing producer(' + str(producer_id) + \
					') information in the cache.'
		else:
			print 'Adding a new producer(' + str(producer_id) + \
					') infromation to the cache.'

		self.cache[producer_id] = producer

	def get(self, producer_id):
		if producer_id in self.cache:
			print 'Producer(' + str(producer_id) + \
					') information is in the cache.'
			return self.cache[producer_id]
		else:
			print 'Producer(' + str(producer_id) + \
					') information is not in the cache.'
			return None

	def flush(self):
		for key, value in self.cache.iteritems():
			updated_heartbeat = db_manager.update_heartbeat(value)

			if updated_heartbeat:
				print 'Heartbeat recorded for producer:', key
			else:
				print 'Heartbeat not recorded for producer:', key

		# clear half of the cache
		if self.isFull():
			cache_new = dict(self.cache.items()[len(self.cache)/2:])
			self.cache = cache_new