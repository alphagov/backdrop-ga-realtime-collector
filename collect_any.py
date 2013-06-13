import json
import importlib

from backdrop.collector import arguments


def _load_json_file(path):
    with open(path) as f:
        return json.load(f)

if __name__ == '__main__':
    args = arguments.parse_args('Multi source')

    targets = _load_json_file('./config/targets.json')

    collector = importlib.import_module(args.query['collector'])
    collector.send_records_for(args.query['query'],
                               to=targets.get(args['target']))
