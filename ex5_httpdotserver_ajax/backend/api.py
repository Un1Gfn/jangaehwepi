#!/bin/env python3

# https://poe.com/s/llYF37LR6dnZc7odgehm

# /list
# /activate/{ID}

# import http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
from sys import argv
from urllib.parse import urlparse

ADDR = ""
PORT = -1

JSON = """
{
  "active": -1,
  "nodes": [
    [ 1, 2001, "SImXqA0Q3DeUt5eEaV8dNVXAm0gHE4fL" ],
    [ 2, 31,   "OyWdLqU1L65P6Iy6O6VwowZ1aGVoD3zI" ],
    [ 3, 51,   "yDbQEIo2TIp5F2KGpSJHCYamC7Wf5MUi" ],
    [ 4, 6001, "njgqp42wgr7oMEIofImDk99bDsZf1Lhz" ],
    [ 5, 4001, "KwAZvwHOCzwRgWXluNuBTtoGRsS3yVHm" ]
  ]
}"""

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
                self.wfile.write(JSON.encode())
            case _:
                self.send_error(404, "mz5b90", f'request path "{p}" not implemented')

def main():
    ADDR = argv[1]
    PORT = argv[2]
    print(f"http://{ADDR}:{PORT}/")
    print()
    HTTPServer((ADDR, int(PORT)), AjaxRequestHandler).serve_forever()

if __name__ == "__main__":
    main()
