import requests, json
from flask import jsonify

payload = {'id': 'value', 'location': 'value2'}
headers = {'content-type': 'application/json'}
r = requests.post("http://138.251.207.92:5000/register", data=json.dumps(payload), headers=headers)
print r.text
print r.url
