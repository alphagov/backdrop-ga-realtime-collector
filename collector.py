import json
import argparse
from optparse import OptionParser
from backdrop.collector.backdrop import Backdrop
from backdrop.collector.realtime import Realtime


def get_contents_as_json(path_to_file):
    with open(path_to_file) as file_to_load:
        contents = file_to_load.read()
    return contents

parser = argparse.ArgumentParser(
    description='Read from the Google Analytics realtime API and send to '
                'backdrop.')
parser.add_argument('-q', '--query', dest='query',
                    help='file containing google analytics query as json')
parser.add_argument('-c', '--credentials', dest='credentials',
                    help='Google Analytics credentials',
                    default='config/credentials.json')
args = parser.parse_args()

if not args.query:
    parser.print_help()
    exit()

credentials = json.loads(get_contents_as_json(args.credentials))

query = json.loads(get_contents_as_json(args.query))

visitors = Realtime(credentials).query(query['query'])
Backdrop(query['target']).send_current_user_event(visitors, query['query']["filters"])
