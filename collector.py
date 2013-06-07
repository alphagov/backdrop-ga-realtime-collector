import sys
from backdrop.collector.realtime import Realtime

args = sys.argv

if not args[1]:
    print "usage: run.py query_file [config_file]"
    exit()

config_path = ".collector/config.json"

if len(args) == 3:
    config_path = args[2]

Realtime(config_path).query(args[1])