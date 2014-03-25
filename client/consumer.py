import requests, json

some_id = 1
r = requests.get('http://138.251.207.92:5000/get_location/1')
print r.json()
