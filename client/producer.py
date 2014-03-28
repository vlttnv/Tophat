import requests, json, argparse,time, BaseHTTPServer
import threading
from flask import jsonify

# Finals
HOST_NAME = ""
PORT_NUMBER = 9000


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
parser = argparse.ArgumentParser(description='A producer that sends heartbeats to a specified server, while lsitening on a specified port for incoming GET requests.')
parser.add_argument('-rA', '--remote-address', help='Destination IP address used for the hearbeats')
parser.add_argument('-rP', '--remote-port', help='Destionatioon PORT number used for the heartbeat')
parser.add_argument('-lA', '--local-address', default='',help='Host name used to listen for a GET request. Leave blank to listen on all interfaces.')
parser.add_argument('-lP', '--local-port', default=9000, type=int, help='Local PORT port number used for the listening server. Default is 9000')
parser.add_argument('-i', '--id', help='Producer ID')
parser.add_argument('-hB', '--heartbeat', type=int, default=1 help='Heartbeat interval')
args = parser.parse_args()

# Check the qreuqired command line arguments
if not args.remote_address or not args.remote_address:
	print '!> Missing remote address or remote port.'
	print '!> Use -h to for help.'
	quit(1)

"""
Sending  periodic heartbeats to the main server

The interval can be specified using a command line argument -hB
"""
def heartbeat():
	while 1:
		time.sleep(args.heartbeat)
		payload = {'id': args.id, 'location': 'value2'}
		headers = {'content-type': 'application/json'}
		r = requests.post("http://" + args.remote_address + args.remote_port + "/heartbeat", data=json.dumps(payload), headers=headers)
		print r.text
		print r.url


class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(s):
		s.send_response(200)
		s.send_header("Content-type", "application/json")
		s.end_headers()
		s.wfile.write(json_data)

def run_server():
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((args.local_address, args.local_port), Handler)
	print 'O> Server Starts - ', time.asctime()
	print 'O> Listening on port %s' % (args.local_port)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print 'O> Server Stops - ', time.asctime()



if __name__ == '__main__':
	# Make heartbeat thread and start it
	hb = threading.Thread(target=heartbeat)
	hb.daemon=True
	hb.start()
	run_server()
