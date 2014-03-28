class ProducerIPNotFoundException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return 'Cannot find producer\'s IP address.'

class ProducerPortNotFoundException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return 'Cannot find producer\'s port number.'

class ProducerDataNotFoundException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return 'Cannot retreive data.'

class ProducerConnectionException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return 'Failed to connect to the producer'