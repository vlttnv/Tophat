import requests, json, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', help='Destination IP address')
args = parser.parse_args()
some_id = 1
r = requests.get('http://138.251.246.169:9000/get_data/15')
print r.text
