import json
from optparse import OptionParser
from backdrop.collector.backdrop import Backdrop
from backdrop.collector.realtime import Realtime

def get_contents_as_json(path_to_file):
    with open(path_to_file) as file_to_load:
        contents = file_to_load.read()
    return contents

parser = OptionParser()
parser.add_option("-q", "--query", dest="query",
                  help="file containing google analytics query as json")
parser.add_option("-c", "--config", dest="config",
                  help="config location (config/config.json by default)")
(options, args) = parser.parse_args()

if not options.query:
    parser.print_help()
    exit()

config_path = options.config or "config/config.json"
config = json.loads(get_contents_as_json(config_path))

query_path = options.query
query = json.loads(get_contents_as_json(query_path))

visitors = Realtime(config).query(query)
Backdrop(config).send_current_user_event(visitors, query["filters"])
