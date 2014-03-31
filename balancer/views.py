from balancer import app
from flask import redirect, request
from server import db_manager
import json

workers = ['http://138.251.212.25:5000','http://138.251.212.25:5000','http://138.251.212.25:5000']

list_workers = {}



ptr = 0

@app.route('/get_data/<int:id>')
def index(id):
	ip = list_workers[id]
	url = ip + '/get_data/' + str(id)
	return redirect(url, code=302)

@app.route('/register/<int:id>', methods=['GET'])
def register(id):
	"""

	"""

	print 'Request from', request.remote_addr, ': registering.'
	global ptr
	if ptr == len(workers) - 1:
		ptr = 0
	else:
		ptr = ptr + 1
	
	list_workers[id] = workers[ptr]
	print list_workers

	return workers[ptr] 
