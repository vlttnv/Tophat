class ProducerIPNotFoundException(Exception):
	def __str__(self):
		return 'Cannot find producer\'s IP address.'

class ProducerPortNotFoundException(Exception):
	def __str__(self):
		return 'Cannot find producer\'s port number.'

class ProducerDataNotFoundException(Exception):
	def __str__(self):
		return 'Cannot retreive data.'

class ProducerConnectionException(Exception):
	def __str__(self):
		return 'Failed to connect to the producer.'