#!/dev/null

# https://stackoverflow.com/questions/1207406/how-to-remove-items-from-a-list-while-iterating

# do not import storage from storage
# always use it with "storage.storage"
# otherwise assignment of the global var takes no effect

# do not put blacklist in storage
# blacklist data shall preserve if clash.yaml and storage.json are removed

from copy import deepcopy
from lnk_conf import *
from lnk_conf import *
from os.path import isfile
from ruamel.yaml import YAML
import benchmark
import json

blacklist = [

]

storage = {
    'active': -1,
    'nodes': [ ]
}

# serve_forever
def init():
    global blacklist
    if isfile("blacklist.json"):
        with open("blacklist.json", 'r') as f:
            blacklist = json.load(f)
    blacklist_save()
    global storage
    if isfile("storage.json"):
        with open("storage.json", 'r') as f:
            storage = json.load(f)
    elif isfile("clash.yaml"):
        storage_from_clash()
        storage_save()
    else:
        storage_save()

# g_upload [1/2]
def storage_from_clash():
    global storage
    storage['nodes'] = [ ]
    with open("default.json", 'r') as f:
        default_trojan = json.load(f)
        default_trojan['local_addr'] = SOCKS5_ADDR
        default_trojan['local_port'] = SOCKS5_PORT
    with open("clash.yaml", "r") as f:
        from_yaml = YAML().load(f)
    id = 0
    for p in from_yaml['proxies']:
        id += 1

        n = {
            'name': "",
            'type': "",
            'latency': benchmark.PLACEHOLDER_NOT_TESTED_YET,
            'conf': {},
        }
        assert 'type' in p

        match p['type']:

            case "trojan":
                n['type'] = "trojan"
                n['conf'] = deepcopy(default_trojan)
                for k, v in p.items():
                    match k:
                        case 'type':             assert v == "trojan"
                        case 'skip-cert-verify': assert v == True
                        case 'udp':              assert v == True
                        case 'alpn':             assert str(v) == "['h2', 'http/1.1']"
                        case 'name':             n['name'] = v
                        case 'server':           n['conf']['remote_addr'] = v
                        case 'port':             n['conf']['remote_port'] = v
                        case 'password':         n['conf']['password'] = [ v ]
                        case _:                  print(f"unknown field ['{k}']: \"{v}\""); raise RuntimeError

            case "ss":
                n['type'] = "ss"
                for k, v in p.items():
                    match k:
                        case 'cipher':   assert v == "aes-256-cfb"
                        case 'type':     assert "ss" == v
                        case 'udp':      assert v == True
                        case 'name':     n['name'] = v
                        case 'server':   n['conf']['server'] = v
                        case 'port':     n['conf']['server_port'] = v
                        case 'password': n['conf']['password'] = v
                        case _:          print(f"unknown field ['{k}']: \"{v}\""); raise RuntimeError

        storage['nodes'].append(n)

# g_pull
def list():
    d = {
        'active': storage['active'],
        'benchmarking': benchmark.benchmarking,
        'list1': [ ],
        'list2': [ ]
    }
    for (id, n) in enumerate(storage['nodes']):
        row = [ id, n['name'], n['latency'] ]
        if not is_blacklisted(n):
            d['list1'].append(row)
        else:
            d['list2'].append(row)
    return d

def is_blacklisted(n):
    c = n['conf']
    match n['type']:
        case 'trojan': return any([ ( c['remote_addr'], c['remote_port'] ) == ( b['canonical_ip'], b['canonical_port'] ) for b in blacklist ])
        case 'ss':     return any([ ( c['server'],      c['server_port'] ) == ( b['canonical_ip'], b['canonical_port'] ) for b in blacklist ])

# g_ban
def blacklist_append(id):
    n = storage['nodes'][id]
    c = n['conf']
    match n['type']:
        case 'trojan': blacklist.append({ 'canonical_ip': c['remote_addr'], 'canonical_port': c['remote_port'] })
        case 'ss':     blacklist.append({ 'canonical_ip': c['server'],      'canonical_port': c['server_port'] })
    blacklist_save()

# g_allow
def blacklist_remove(id):
    c = storage['nodes'][id]['conf']
    blacklist[:] = [ b for b in blacklist if not b.items() <= c.items() ]
    blacklist_save()

# g_upload [2/2]
# g_activate
# g_deactivate
def storage_save():
    with open("storage.json", 'w') as f:
        json.dump(storage, f, ensure_ascii=True, indent="  ")

def blacklist_save():
    with open("blacklist.json", 'w') as f:
        json.dump(blacklist, f, ensure_ascii=True, indent="  ")
