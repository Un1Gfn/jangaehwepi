#!/bin/env python3

from argparse import ArgumentParser
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from os import environ
from os.path import isfile, split
from threading import Thread
from urllib.parse import urlparse
import json
import storage
import trojan

class FrontendHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="../frontend", **kwargs)
    def log_message(self, format, *args):
        pass

def frontend(parsed):
    HTTPServer((parsed.a, int(parsed.f)), FrontendHTTPRequestHandler).serve_forever()

class BackendHTTPRequestHandler(BaseHTTPRequestHandler):

    # def log_message(self, format, *args):
    #     pass

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def success(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):

        p = split(urlparse(self.path).path)
        match(p[0]):

            case "/":
                self.send_error(400, "E_NOROOT")

            case "/g_update":
                if storage.storage['active'] >= 0:
                    trojan.deactivate()
                storage.from_clash()
                storage.save()
                self.success()

            case "/g_deactivate":
                if storage.storage['active'] >= 0:
                    trojan.deactivate()
                    storage.storage['active'] = -1
                    self.send_response(200, "deactivated"); self.end_headers()
                self.success()

            case "/g_activate":
                if storage.storage['active'] >= 0:
                    trojan.deactivate()
                    storage.storage['active'] = -1
                id = int(p[1])
                assert id >= 0
                trojan.activate(id)
                storage.storage['active'] = id
                storage.save()
                self.success()

            case "/g_blacklist":
                storage.add_blacklist(int(p[1]))
                print("add_blacklist()")
                self.success()

            case "/g_list":
                self.send_response(200, "listing nodes ...")
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(storage.list()).encode())

            case _:
                self.send_error(404, "E_INVALID", f'request "{urlparse(self.path)}" not implemented')
                print(urlparse(self.path))

if __name__ == "__main__":

    ban_env = [ 'http_proxy', 'https_proxy', 'all_proxy', 'no_proxy', ]
    ban_env += [ e.upper() for e in ban_env ]
    if any([ e in environ for e in ban_env ]):
        raise RuntimeError

    parser = ArgumentParser()
    parser.add_argument("-a")
    parser.add_argument("-f")
    parser.add_argument("-b")
    parsed = parser.parse_args()

    storage.load()
    id = storage.storage['active']
    if id >= 0:
        trojan.activate(id)

    Thread(target=frontend, args=(parsed,)).start()
    HTTPServer((parsed.a, int(parsed.b)), BackendHTTPRequestHandler).serve_forever()
