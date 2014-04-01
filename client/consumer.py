import requests, json, argparse, sys

# Set up command line arguments
parser = argparse.ArgumentParser(description='A consumer which makes requests to the broker.')
parser.add_argument('address', help='Destination IP address')
parser.add_argument('port', help='Destionation PORT number')
parser.add_argument('id', help='Producer ID')
args = parser.parse_args()

try:
	r = requests.get('http://' + args.address  + ':' + args.port + '/get_data/' + args.id)
	print r.text
except requests.ConnectionError:
	sys.exit('Server offline or incorrect address/port.')
