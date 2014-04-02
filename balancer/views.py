from balancer import balancer_app
from flask import redirect, request
from worker import db_manager
import json, argparse

parser = argparse.ArgumentParser(description='Manages comunication between \
		Producers, Consumers and Wokers. Balances load.')

workers = []
list_workers = {}
# Round robin
ptr = 0

@balancer_app.route('/get_data/<int:id>', methods=['GET'])
def get_data(id):
	"""
	Bulds the url and
	redirects the consumer to the coresponding producer
	"""

	if id not in list_workers:
		return 'Producer does not exist', 400

	ip = list_workers[id]
	url = ip + '/get_data/' + str(id)
	return redirect(url, code=302)

@balancer_app.route('/register/<int:id>', methods=['GET'])
def get_register(id):
	"""
	Registers the producer and returns a worker address
	"""

	print 'Request from', request.remote_addr, ': register producer', id
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

@balancer_app.route('/balancer/<int:port>', methods=['GET'])
def get_balancer(port):
	"""
	Register a worker and add it to the list
	"""
	
	url = 'http://' + request.remote_addr + ':' + str(port)
	print 'Request from', request.remote_addr, ': register worker'
	if url not in workers:
		workers.append(url)
	
	return 'Successful rgistration', 200

@balancer_app.route('/worker/quit/<int:port>', methods=['GET'])
def get_worker_quit(port):
	"""

	"""
	url = 'http://' + request.addr + ':' +str(port)
	if url in workers:
		workers.remove(url)
		return 'Acknowledged quit', 200

	return 'Quit not accepted', 400

