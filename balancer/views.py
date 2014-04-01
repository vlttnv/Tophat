from balancer import app
from flask import redirect, request
from server import db_manager
import json, argparse


parser = argparse.ArgumentParser(description='To be added')

workers = []

list_workers = {}



ptr = 0

@app.route('/get_data/<int:id>')
def index(id):
	"""
	Redirects the consumer to the coresponding producer
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

	if ptr == len(workers) - 1:
		ptr = 0
	else:
		ptr = ptr + 1
	
	list_workers[id] = workers[ptr]
	print list_workers

	return workers[ptr]

@app.route('/balancer/<int:port>')
def balancer(port):
	"""
	Register a worker
	"""
	url = request.remote_addr + ':' +  str(port)
	print 'Request from', request.remote_addr, ': registering worker'
	if url not in workers:
		workers.append(url)
