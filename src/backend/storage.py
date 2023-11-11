#!/dev/null

# https://stackoverflow.com/questions/1207406/how-to-remove-items-from-a-list-while-iterating

# do not import storage from storage
# always use it with "storage.storage"
# otherwise assignment of the global var takes no effect

# do not put blacklist in storage
# blacklist data shall preserve if clash.yaml and storage.json are removed

from copy import deepcopy
from lnk_conf import *
from os.path import isfile
from ruamel.yaml import YAML
from lnk_conf import *
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
        default_conf = json.load(f)
        default_conf['local_addr'] = SOCKS5_ADDR
        default_conf['local_port'] = SOCKS5_PORT
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

# g_pull
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

# g_ban
def blacklist_append(id):
    c = storage['nodes'][id]['conf']
    blacklist.append({
        'remote_addr': c['remote_addr'],
        'remote_port': c['remote_port']
    })
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
