from balancer import app
from flask import redirect

@app.route('/get_data/<int:id>')
def index(id):
	return redirect("http://127.0.0.1:5000/get_data/" + str(id), code=302)
