#!/bin/env python3

from ruamel.yaml import YAML
from sys import stdout
import json

h = YAML()
dump = h.dump
load = h.load

class Node:
    def __init__(self):
        self.name = ""
        with open("default.json", 'r') as fp:
            self.conf = json.load(fp)

with open("clash.yaml", "r") as fp:
    y = load(fp)
    for p in y['proxies']:
        n = Node()
        c = n.conf
        print(".")
        for k, v in p.items():
            match k:
                case 'skip-cert-verify': assert True == v
                case 'udp':              assert True == v
                case 'type':             assert "trojan" == v
                case 'alpn':             assert "['h2', 'http/1.1']" == str(v)
                case 'name':             n.name = v
                case 'server':           c['remote_addr'] = v
                case 'port':             c['remote_port'] = v
                case 'password':         c['password'] = [ v ]
                case _:                  print(k, v)
        print(".")
        print(json.dumps(c))
        print()
