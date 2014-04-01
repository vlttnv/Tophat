from balancer import app
from flask import redirect, request
from server import db_manager
import json, argparse


parser = argparse.ArgumentParser(description='Manages comunication between \
		Producers, Consumers and Wokers. Balances load.')

workers = []
list_workers = {}
# Round robin
ptr = 0

@app.route('/get_data/<int:id>')
def index(id):
	"""
	Bulds the url and
	redirects the consumer to the coresponding producer
	"""
	ip = list_workers[id]
	url = ip + '/get_data/' + str(id)
	return redirect(url, code=302)

@app.route('/register/<int:id>', methods=['GET'])
def register(id):
	"""
	Registers the producer and returns a worker address
	"""

	print 'Request from', request.remote_addr, ': registering producer'
	global ptr

	if len(workers) == 0:
		return 'No workers are online right now', 400
	
	# Reset balancing
	if ptr == len(workers) - 1:
		ptr = 0
	else:
		ptr = ptr + 1
	
	list_workers[id] = workers[ptr]

	return workers[ptr]

@app.route('/balancer/<int:port>')
def balancer(port):
	"""
	Register a worker and add it to the list
	"""
	url = 'http://' + request.remote_addr + ':' +  str(port)
	print 'Request from', request.remote_addr, ': registering worker'
	if url not in workers:
		workers.append(url)
	
	return 'Successful rgistration', 200
