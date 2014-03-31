from balancer import app
from flask import redirect, request
from server import db_manager
import json

workers = ['http://138.251.212.25:5000','http://138.251.212.25:5000','http://138.251.212.25:5000']

ptr = 0

@app.route('/get_data/<int:id>')
def index(id):
	global ptr
	url = workers[ptr] + "/get_data/" + str(id)
	if ptr == len(workers) - 1:
		ptr = 0
	else:
		ptr = ptr + 1

	print len(workers)
	return redirect(url, code=302)

@app.route('/register')
def register():
	"""

	"""

	print 'Request from', request.remote_addr, ': registering.'
	global ptr
	if ptr == len(workers) - 1:
		ptr = 0
	else:
		ptr = ptr + 1

	return workers[ptr] 
