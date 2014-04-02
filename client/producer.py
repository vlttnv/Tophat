import requests, json, argparse,time, BaseHTTPServer
import threading, sys

MAX_RETRIES = 10

# Set up command line arguments
parser = argparse.ArgumentParser(
	description='A producer that sends heartbeats, including data.')

parser.add_argument('remote_address',
	help='Destination IP address used for the hearbeats.')
parser.add_argument('remote_port',
	help='Destionatioon PORT number used for the heartbeats.')
parser.add_argument('id',
	help='Producer ID, the unique identifier of the mobile phone.')
parser.add_argument('-hB', '--heartbeat',
	type=int, default=1, help='Heartbeat interval')
parser.add_argument('-s', '--silent',
	action='store_true', default=False, help='Enable silent mode')

args = parser.parse_args()

# Sample Json
json_data = {
    'id': args.id,
	'data': 'Phasellus consectetur tortor eu risus pretium consectetur eu \
				faucibus tellus. Fusce imperdiet sed urna at ultrices. Etiam \
				varius viverra facilisis. Quisque quis imperdiet augue, et \
				ullamcorper justo. Maecenas a risus erat. Curabitur non \
				adipiscing leo. Phasellus ultrices cursus dolor ac tempus. \
				Vivamus urna arcu, convallis feugiat justo ut, fermentum \
				mattis lacus. Nunc laoreet lorem sit amet rhoncus malesuada. \
				Fusce nec enim eu nisl ultrices ultrices.'
}

producer = 'Producer(' + args.id + ')> '

def heartbeat():
	"""
	Send periodic heartbeats to the main server.

	The interval can be specified with the command line argument -hB
	"""

	global MAX_RETRIES

	if MAX_RETRIES == 0:
		sys.exit(producer + 'Maximum retries reached.')
	
	# Register with the balancer
	try:
		adr = requests.get('http://' + args.remote_address + ':' + args.remote_port + '/register/' + str(args.id))
		if adr.status_code == 400:
			sys.exit(adr.text)
		print producer + 'Registered with balancer, waiting for assigned worker.'
		print producer + 'Assigned worker is ' + adr.text
	except requests.ConnectionError:
		sys.exit('Incorrect address/port or main server is offline.')

	# Hearbeat forever
	while 1:
		time.sleep(args.heartbeat)
		payload = {'id': args.id, 'location': 'value2', 'data': json.dumps(json_data)}
		headers = {'content-type': 'application/json'}

		try:
			print producer + 'Send heartbeat.'
			# timeout in 10 seconds
			r = requests.post(adr.text + "/heartbeat", data=json.dumps(payload), headers=headers, timeout=10)

			if r.status_code != 200:
				print producer + 'Request failed. Sending heartbeat again.'
		except requests.exceptions.ConnectionError:
			MAX_RETRIES = MAX_RETRIES - 1
			print producer + 'Worker unreachable. Retrying...', str(MAX_RETRIES) + ' retries left.'
			heartbeat()
		except requests.exceptions.Timeout:
			MAX_RETRIES = MAX_RETRIES - 1
			print producer + 'Worker unreachable. Retrying...', str(MAX_RETRIES) + ' retries left.'
			heartbeat()

		if not args.silent and r.status_code == 200:
			print 'Response> ', r.text

if __name__ == '__main__':
	try:
		heartbeat()
	except KeyboardInterrupt:
		sys.exit('Exiting.')
