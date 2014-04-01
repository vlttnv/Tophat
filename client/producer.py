import requests, json, argparse,time, BaseHTTPServer
import threading, sys

MAX_RETRIES = 10

# Sample Json
json_data = {
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
		}
}

# Set up command line arguments
parser = argparse.ArgumentParser(description='A producer that sends heartbeats to a specified server, including data.')
parser.add_argument('remote_address', help='Destination IP address used for the hearbeats')
parser.add_argument('remote_port', help='Destionatioon PORT number used for the heartbeat')
parser.add_argument('id', help='Producer ID')
parser.add_argument('-hB', '--heartbeat', type=int, default=1, help='Heartbeat interval')
parser.add_argument('-s', '--silent', action='store_true', default=False, help='Enable silent mode')
args = parser.parse_args()

def heartbeat():
	"""
	Sending  periodic heartbeats to the main server

	The interval can be specified using a command line argument -hB
	"""
	global MAX_RETRIES

	if MAX_RETRIES == 0:
		sys.exit('Maximum retries reached.')
	
	# Register first
	try:
		adr = requests.get('http://' + args.remote_address + ':' + args.remote_port + '/register/' + str(args.id))
		if adr.status_code == 400:
			sys.exit(adr.text)
		print 'Registered'
	except requests.ConnectionError:
		sys.exit('Incorrect address/port or main server is offline.')

	# Hearbeat forever
	while 1:
		time.sleep(args.heartbeat)
		payload = {'id': args.id, 'location': 'value2', 'data': json.dumps(json_data)}
		headers = {'content-type': 'application/json'}

		try:
			r = requests.post(adr.text + "/heartbeat", data=json.dumps(payload), headers=headers)
		except requests.ConnectionError:
			MAX_RETRIES = MAX_RETRIES - 1
			print 'Retrying...', str(MAX_RETRIES) + ' left.'
			heartbeat()
		if not args.silent:
				print 'O>', r.text


if __name__ == '__main__':
	try:
		heartbeat()
	except KeyboardInterrupt:
		sys.exit('Exiting.')
