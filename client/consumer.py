import requests, json, argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', '--address', help='Destination IP address')
args = parser.parse_args()
some_id = 1
r = requests.get('http://' + args.address  + '/get_data/20')
print r.text
