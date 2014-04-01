import requests, json, argparse, sys

# Set up command line arguments
parser = argparse.ArgumentParser(description='A consumer which makes requests to the broker.')
parser.add_argument('address', help='Destination IP address')
parser.add_argument('port', help='Destionation PORT number')
parser.add_argument('id', help='Producer ID')
args = parser.parse_args()

# Check required command line arguments
if not args.address or not args.port:
		print '!> Missing addres or port'
		print '!> Use -h for help'
		quit(1)

try:
	r = requests.get('http://' + args.address  + ':' + args.port + '/get_data/' + args.id)

	if r.status_code == 200:
		print 'Received data.'
	else:
		print 'Did not receive data.'
	print r.text
except requests.ConnectionError:
	sys.exit('Server offline or incorrect address/port.')
