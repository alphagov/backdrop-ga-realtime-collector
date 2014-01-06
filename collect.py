import json
import logging
from backdrop.collector import arguments
from backdrop.collector.logging_setup import set_up_logging
from os.path import realpath, dirname
from collector import realtime


def _load_json_file(path):
    with open(path) as f:
        return json.load(f)

if __name__ == '__main__':
    args = arguments.parse_args('Google Analytics realtime')

    set_up_logging('ga-realtime', logging.DEBUG)

    collector = realtime.Collector(args.credentials)

    targets_json_path = '/config/targets.json'
    targets = _load_json_file(dirname(realpath(__file__)) +
                              targets_json_path)

    target = targets.get(args.query['target'])
    if not target:
        logging.error("ERROR: Entry for `%s` not found in %s"
                      % (args.query['target'], targets_json_path))
        exit(1)

    collector.send_records_for(args.query['query'],
                               to=target)
