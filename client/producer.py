import requests, json, argparse, time
from flask import jsonify

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', help='Destination IP address')
args = parser.parse_args()

while 1:
	time.sleep(1)
	payload = {'id': '2', 'location': 'value2'}
	headers = {'content-type': 'application/json'}
	r = requests.post("http://" + args.address + "/heartbeat", data=json.dumps(payload), headers=headers)
	print r.text
	print r.url

#payload2 = {'producer_id': '1', 'data': 'd2ed2e4r3ro4j3k n324nk34'}
#headers2 =  {'content-type': 'application/json'}
#r2 = requests.post("http://" + args.address + "/send", data=json.dumps(payload2), headers=headers2)
#print r2.text
