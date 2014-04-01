#!/usr/bin/python

import argparse
from balancer import app

parser = argparse.ArgumentParser(description='To be added')
parser.add_argument('port', type=int, help='Port number to bind to')
args = parser.parse_args()

app.run(host='0.0.0.0', port=int(args.port), debug=True)
