#!/usr/bin/python

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import argparse
from balancer import balancer_app

parser = argparse.ArgumentParser(description='Manages the comunication between \
	Producers, Consumers and Wokers. Balances load.')
parser.add_argument('port', type=int, help='Port number to bind to')
args = parser.parse_args()

try:
	#worker_app.run(host='0.0.0.0', port=int(args.port), debug=True, use_reloader=False)
	http_server = HTTPServer(WSGIContainer(balancer_app))
	http_server.listen(args.port)
	IOLoop.instance().start()
except KeyboardInterrupt:
	print 'Balancer exits: KeyboardInterrupt'