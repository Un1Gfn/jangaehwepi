#!/bin/env python3

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from sys import argv
from urllib.parse import urlparse
from storage import storage, loadconf

ADDR = ""
PORT = -1

class AjaxRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        p = urlparse(self.path).path
        match(p):
            case "/":
                self.send_error(400, "b9ftoi", "This is the API, not the Web UI.")
            case "/list":
                self.send_response(200, "listing nodes ...")
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                data = {
                    'active': storage['active'],
                    'nodes': [
                        [ n['id'], -1, n['name'], "" ] for n in storage['nodes']
                    ]
                }
                self.wfile.write(json.dumps(data).encode())
            case _:
                self.send_error(404, "mz5b90", f'request "{urlparse(self.path)}" not implemented')

if __name__ == "__main__":
    ADDR = argv[1]
    PORT = argv[2]
    loadconf()
    print(f"http://{ADDR}:{PORT}/")
    print()
    HTTPServer((ADDR, int(PORT)), AjaxRequestHandler).serve_forever()
