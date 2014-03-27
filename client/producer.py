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


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', help='Destination IP address')
parser.add_argument('-i', '--id', help='Producer ID')
args = parser.parse_args()

def heartbeat():
	while 1:
		time.sleep(1)
		payload = {'id': args.id, 'location': 'value2'}
		headers = {'content-type': 'application/json'}
		r = requests.post("http://" + args.address + "/heartbeat", data=json.dumps(payload), headers=headers)
		print r.text
		print r.url

#payload2 = {'producer_id': '1', 'data': 'd2ed2e4r3ro4j3k n324nk34'}
#headers2 =  {'content-type': 'application/json'}
#r2 = requests.post("http://" + args.address + "/send", data=json.dumps(payload2), headers=headers2
#print r2.text

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(s):
		s.send_response(200)
		s.send_header("Content-type", "application/json")
		s.end_headers()
		s.wfile.write(json_data)

def run_server():
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class(('', PORT_NUMBER), MyHandler)
	print time.asctime(), "Server Starts - %s, %s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print time.asctime(), "Server Stops - %s, %s" % (HOST_NAME, PORT_NUMBER)



if __name__ == '__main__':
	hb = threading.Thread(target=heartbeat)
	hb.daemon=True
	hb.start()
		
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class(('', PORT_NUMBER), MyHandler)
	print time.asctime(), "Server Starts - %s, %s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print time.asctime(), "Server Stops - %s, %s" % (HOST_NAME, PORT_NUMBER)
