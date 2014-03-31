from balancer import app
from flask import redirect

workers = ['http://127.0.0.1:5000','http://127.0.0.1:5000','http://127.0.0.1:5000']

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
