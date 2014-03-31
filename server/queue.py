from server import db_manager

class Queue:

	def __init__(self, limit):
		self.limit = limit
		self.queue = {}

	def size(self):
		return len(self.queue)

	def isEmpty(self):
		return len(self.queue) == 0

	def isFull(self):
		return len(self.queue) == self.limit

	def add(self, producer):
		producer_id = producer['id']

		if self.isFull() and (producer_id not in self.queue):
			print 'Queue is full. Flushing.'
			self._flush()

		if producer_id in self.queue:
			print 'Updating pre-existing producer(' + str(producer_id) + \
					') information in the queue.'
		else:
			print 'Adding a new producer(' + str(producer_id) + \
					') infromation to the queue.'

		self.queue[producer_id] = producer

	def get(self, producer_id):
		if producer_id in self.queue:
			print 'Producer(' + str(producer_id) + \
					') information is in the queue.'
			return self.queue[producer_id]
		else:
			print 'Producer(' + str(producer_id) + \
					') information is not in the queue.'
			return None

	def _flush(self):
		for key, value in self.queue.iteritems():
			updated_heartbeat = db_manager.update_heartbeat(value)

			if updated_heartbeat:
				print 'Heartbeat recorded for producer:', key
			else:
				print 'Heartbeat not recorded for producer:', key

		self.queue.clear()