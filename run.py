#!usr/bin/python

import argparse
import requests
import sys
from server import app

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

app.run(host='0.0.0.0', port=int(args.port), debug=True, use_reloader=False)