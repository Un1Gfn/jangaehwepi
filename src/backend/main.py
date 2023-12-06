#!/usr/bin/env python3

# https://stackoverflow.com/questions/6063416/python-basehttpserver-how-do-i-catch-trap-broken-pipe-errors

from hashlib import sha1
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from lnk_conf import *
from multipart import multipart, parse_form
from os import environ
from os.path import split
from pathlib import Path
from threading import Thread
from urllib.parse import urlparse
import benchmark
import json
import storage
import proxy

class BackendHTTPRequestHandler(BaseHTTPRequestHandler):

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def success(self):
        self.send_response(200)
        self.end_headers()

    def on_field(self, field):
        assert False

    def on_file(self, file):

        assert type(file) == multipart.File
        assert type(file.file_object) == BytesIO
        assert file.actual_file_name == None
        assert len(file.file_name) > 0
        assert file.field_name.decode() == "fd_file"
        assert file.size > 0
        print(f"{file.size} bytes")

        b = file.file_object.getvalue()
        assert type(b) == bytes
        assert len(b) == file.size
        print(sha1(b).digest().hex())

        assert Path(file.file_name.decode()).suffix in [ ".list", ".yaml", ".yml", ".conf", ".txt" ]
        with open("clash.yaml", 'wb') as f:
            f.write(b)

    def mfd(self):
        ct = self.headers.get('Content-Type')
        cl = int(self.headers.get('Content-Length'))
        assert ct.startswith("multipart/form-data")
        assert cl >= 1
        mfd = multipart.FormParser.DEFAULT_CONFIG
        assert 'MAX_MEMORY_FILE_SIZE' in mfd
        mfd['MAX_MEMORY_FILE_SIZE'] = 128*1024*1024
        parse_form({
            'Content-Type': ct,
            'Content-Length': cl
        }, self.rfile, self.on_field, self.on_file)

    def do_POST(self):
        assert self.path == "/g_upload/"
        self.mfd()
        if storage.storage['active'] >= 0:
            proxy.deactivate()
        storage.storage_from_clash()
        storage.storage_save()
        self.success()

    def do_GET(self):

        p = split(urlparse(self.path).path)
        match(p[0]):

            case "/":
                self.send_error(400, "E_NOROOT")

            case "/g_deactivate":
                if storage.storage['active'] >= 0:
                    proxy.deactivate()
                    storage.storage['active'] = -1
                    self.send_response(200, "deactivated"); self.end_headers()
                self.success()

            case "/g_activate":
                if storage.storage['active'] >= 0:
                    proxy.deactivate()
                    storage.storage['active'] = -1
                id = int(p[1])
                assert id >= 0
                proxy.activate(id)
                storage.storage['active'] = id
                storage.storage_save()
                self.success()

            case "/g_ban":
                storage.blacklist_append(int(p[1]))
                self.success()

            case "/g_allow":
                storage.blacklist_remove(int(p[1]))
                self.success()

            case "/g_pull":
                self.send_response(200, "listing nodes ...")
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(storage.list()).encode())

            case "/g_benchmark":
                if 1 != benchmark.benchmarking:
                    Thread(target=benchmark.benchmark).start()
                print()
                self.success()

            case _:
                self.send_error(404, "E_INVALID", f'request "{urlparse(self.path)}" not implemented')
                print(urlparse(self.path))

if __name__ == "__main__":

    ban_env = [ 'http_proxy', 'https_proxy', 'socks_proxy', 'socks5_proxy', 'socks5h_proxy', 'all_proxy', 'no_proxy', ]
    ban_env += [ e.upper() for e in ban_env ]
    if any([ e in environ for e in ban_env ]):
        raise RuntimeError

    storage.init()
    benchmark.init()
    id = storage.storage['active']
    if id >= 0:
        proxy.activate(id)

    HTTPServer((BACKEND_ADDR, BACKEND_PORT,), BackendHTTPRequestHandler).serve_forever()
