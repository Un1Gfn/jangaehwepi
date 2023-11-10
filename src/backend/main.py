#!/bin/env python3

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from sys import argv
from urllib.parse import urlparse
from storage import storage, loadconf
from os import environ
import trojan
from os.path import split

ADDR = ""
PORT = -1

class AjaxRequestHandler(BaseHTTPRequestHandler):

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):

        p = urlparse(self.path).path

        match(p):

            case "/":
                self.send_error(400, "E_NOROOT")

            case "/g_deactivate":
                if storage['active'] >= 0:
                    trojan.deactivate()
                    self.send_response(200, "deactivated"); self.end_headers()
                else:
                    self.send_error(400, "E_COLD")

            case "/g_list":
                self.send_response(200, "listing nodes ...")
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                data = {
                    'active': storage['active'],
                    'nodes': [
                        [ id, -1, node['name'], "" ] for (id, node) in enumerate(storage['nodes'])
                    ]
                }
                self.wfile.write(json.dumps(data).encode())

            case _:
                ss = split(p)
                print(ss[0])
                print(ss[1])
                if ss[0] == "/g_activate":
                    if storage['active'] >= 0:
                        self.send_error(400, "E_DUP")
                    else:
                        id = int(ss[1])
                        assert id >= 0
                        trojan.activate(id)
                        storage['active'] = id
                        self.send_response(200, f"activated node {id}"); self.end_headers()
                else:
                    self.send_error(404, "E_INVALID", f'request "{urlparse(self.path)}" not implemented')
                    print(urlparse(self.path))

if __name__ == "__main__":
    ban_env = [ 'http_proxy', 'https_proxy', 'all_proxy', 'no_proxy', ]
    ban_env += [ e.upper() for e in ban_env ]
    if any([ e in environ for e in ban_env ]): raise RuntimeError
    ADDR = argv[1]
    PORT = argv[2]
    loadconf()
    print(f"http://{ADDR}:{PORT}/")
    print()
    HTTPServer((ADDR, int(PORT)), AjaxRequestHandler).serve_forever()
