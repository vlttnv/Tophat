import requests, json, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', help='Destination IP address')
parser.add_argument('-i', '--id', help='Producer ID')
args = parser.parse_args()
some_id = 1
r = requests.get('http://' + args.address  + '/get_data/' + args.id)
print r.text
