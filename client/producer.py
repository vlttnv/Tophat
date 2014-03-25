import requests, json
from flask import jsonify

#payload = {'id': 'value', 'location': 'value2'}
#headers = {'content-type': 'application/json'}
#r = requests.post("http://138.251.207.92:5000/heartbeat", data=json.dumps(payload), headers=headers)
#print r.text
#print r.url

payload2 = {'id': '1', 'location': 'home', 'data': 'd2ed2e4r3ro4j3k n324nk34'}
headers2 =  {'content-type': 'application/json'}
r2 = requests.post("http://138.251.207.92:5000/send", data=json.dumps(payload2), headers=headers2)
print r2.text
