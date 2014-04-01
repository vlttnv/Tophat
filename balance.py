#!/usr/bin/python

import argparse
from balancer import app

parser = argparse.ArgumentParser(description='Manages comunication between \
				Producers, Consumers and Wokers. Balances load.')
parser.add_argument('port', type=int, help='Port number to bind to')
args = parser.parse_args()

app.run(host='0.0.0.0', port=int(args.port), debug=True)
