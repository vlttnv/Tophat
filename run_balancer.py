#!/venv/bin/python

import argparse
from balancer import balancer_app

parser = argparse.ArgumentParser(description='Manages comunication between \
				Producers, Consumers and Wokers. Balances load.')
parser.add_argument('port', type=int, help='Port number to bind to')
args = parser.parse_args()

balancer_app.run(host='0.0.0.0', port=int(args.port), debug=True, use_reloader=False)
