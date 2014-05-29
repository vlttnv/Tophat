import requests, json, argparse, sys, time

# Set up command line arguments
parser = argparse.ArgumentParser(description='A consumer which makes requests to the broker.')
parser.add_argument('address', help='Destination IP address')
parser.add_argument('port', help='Destionation PORT number')
parser.add_argument('id', help='Producer ID')
args = parser.parse_args()

try:
	start = time.time()
	r = requests.get('http://' + args.address  + ':' + args.port + '/get_data/' + args.id)
	end = time.time()

	print end - start

	if r.status_code == 200:
		print 'Received data.'
	else:
		print 'Did not receive data.'
		
	print r.text

except requests.ConnectionError:
	sys.exit('Consumer exits: Balancer server offline or incorrect address/port.')
except KeyboardInterrupt:
	sys.exit('Consumer exits: KeyboardInterrupt')
