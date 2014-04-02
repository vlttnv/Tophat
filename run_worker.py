#!/usr/bin/python

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import argparse
import requests
import sys
import signal
from worker import worker_app

parser = argparse.ArgumentParser(description='To be added')
parser.add_argument('port', type=int, help='Port number to bind to')
parser.add_argument('balancer_addr', help='Balancer IP address')
parser.add_argument('balancer_port', type=int, help='Balancer port number')
args = parser.parse_args()

def register_with_balancer():
	print 'Registering with the balancer.'

	r = requests.get(
		'http://' + str(args.balancer_addr) + ':' + str(args.balancer_port) + \
		'/balancer/' + str(args.port))

	if r.status_code == 200:
		print 'Connected to the balancer.'
	else:
		print 'Cannot connect to the balancer. Trying again.'
		register_with_balancer()

try:
	register_with_balancer()
except requests.ConnectionError:
	sys.exit('Balancer is offline or incorrect address/port')

try:
	#worker_app.run(host='0.0.0.0', port=int(args.port), debug=True, use_reloader=False)
	http_server = HTTPServer(WSGIContainer(worker_app))
	http_server.listen(args.port)
	IOLoop.instance().start()
except KeyboardInterrupt:
	sys.exit('Exiting...')
