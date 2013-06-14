import json
from backdrop.collector import arguments
from os.path import realpath, dirname
from collector import realtime


def _load_json_file(path):
    with open(path) as f:
        return json.load(f)

if __name__ == '__main__':
    args = arguments.parse_args('Google Analytics realtime')

    collector = realtime.Collector(args.credentials)

    targets = _load_json_file(dirname(realpath(__file__)) +
                              '/config/targets.json')

    collector.send_records_for(args.query['query'],
                               to=targets.get(args.query['target']))
