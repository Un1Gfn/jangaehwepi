#!/dev/null

import json
from ruamel.yaml import YAML
from sys import stdout
from copy import deepcopy
from pprint import pprint

# store everything in a big serializable dict
# save to persistant storage on exit
storage = {
    'active': -1,
    'nodes': [ ]
}

def loadconf():
    with open("default.json", 'r') as f:
        default_conf = json.load(f)
    with open("clash.yaml", "r") as f:
        from_yaml = YAML().load(f)
    id = 0
    for p in from_yaml['proxies']:
        n = {
            'name': "",
            'conf': deepcopy(default_conf)
        }
        id += 1
        for k, v in p.items():
            match k:
                case 'skip-cert-verify': assert True == v
                case 'udp':              assert True == v
                case 'type':             assert "trojan" == v
                case 'alpn':             assert "['h2', 'http/1.1']" == str(v)
                case 'name':             n['name'] = v
                case 'server':           n['conf']['remote_addr'] = v
                case 'port':             n['conf']['remote_port'] = v
                case 'password':         n['conf']['password'] = [ v ]
                case _:                  print(f"unknown field ['{k}']: \"{v}\""); raise RuntimeError
        storage['nodes'].append(n)
