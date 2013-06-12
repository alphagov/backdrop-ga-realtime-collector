import json
from backdrop.collector import arguments
from collector import realtime


def _load_json_file(path):
    with open(path) as f:
        return json.load(f)

if __name__ == '__main__':
    args = arguments.parse_args('Google Analytics realtime')

    collector = realtime.Collector(args.credentials)

    targets = _load_json_file('./config/targets.json')

    collector.send_records_for(args.query['query'],
                               to=targets.get(args.query['target']))
