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

@app.route('/heartbeat', methods=['POST'])
def heartbeat():
	"""

	"""

	print 'Request from', request.remote_addr, ': redirect to: '

	if not request.json:
		return 'Hearbeat object must be in json format.', 400

	if not ('port' and 'id' and 'location' and 'data' in request.json):
		return 'Heartbeat object not udnerstood.', 400

	global ptr
	headers = {'content-type': 'application/json'}
	url = workers[ptr] + "/hearbeat"
	if ptr == len(workers) - 1:
		ptr = 0
	else:
		ptr = ptr + 1

	return redirect(url, code=302)
