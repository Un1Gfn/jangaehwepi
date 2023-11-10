#!/dev/null

# do not import storage from storage
# always use it with "storage.storage"
# otherwise assignment of the global var takes no effect

import json
from ruamel.yaml import YAML
from copy import deepcopy
from os.path import isfile

# store everything in a big serializable dict
# save to persistant storage on exit

blacklist = [

]

storage = {
    'active': -1,
    'nodes': [ ]
}

def add_blacklist(id):
    c = storage['nodes'][id]['conf']
    blacklist.append({
        'remote_addr': c['remote_addr'],
        'remote_port': c['remote_port']
    })
    with open("blacklist.json", 'w') as f:
        json.dump(blacklist, f, ensure_ascii=True, indent="  ")

def list():
    d = {
        'active': storage['active'],
        'list1': [ ],
        'list2': [ ]
    }
    for (i, n) in enumerate(storage['nodes']):
        if not any([ b.items() <= n['conf'].items() for b in blacklist ]):
            d['list1'].append([ i, n['name'], -1 ])
        else:
            d['list2'].append([ i, n['name'] ])

    return d

def load():
    global blacklist
    if isfile("blacklist.json"):
        with open("blacklist.json", 'r') as f:
            blacklist = json.load(f)
    global storage
    if isfile("storage.json"):
        with open("storage.json", 'r') as f:
            storage = json.load(f)
    else:
        from_clash()
        save()

def save():
    with open("storage.json", 'w') as f:
        json.dump(storage, f, ensure_ascii=True, indent="  ")

def from_clash():
    global storage
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
