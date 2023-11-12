#!/dev/null

from pprint import pprint

breakpoint()

code.interact(local=locals())

print("client_address .", self.client_address)
print("command        .", self.command)
print("path           .", self.path)
print("rfile          .", self.rfile)
print("wfile          .", self.wfile)
print("headers        ...")
print(self.headers)
print("...")
print()

print("address_string   .", self.address_string())
print("date_time_string .", self.date_time_string())
print("version_string   .", self.version_string())
print()

# send response without stderr log
self.send_response_only(404, "err0")

ruamel.yaml.YAML().dump(...)

DEBUG_JSON = """{
    "active": -1,
    "nodes": [
        [0, -1, "\\ud83c\\uddf7\\ud83c\\uddfa \\u4fc4\\u7f57\\u65af Edge", ""],
        [1, -1, "\\ud83c\\uddf7\\ud83c\\uddfa \\u4fc4\\u7f57\\u65af IEPL [01] [Air]", ""],
        [2, -1, "\\ud83c\\uddf7\\ud83c\\uddfa \\u4fc4\\u7f57\\u65af IEPL [02] [Air]", ""]
    ]
}"""

DEBUG_JSON = """{
    "active": -1,
    "nodes": [
        [0, -1, "\\ud83c", ""]
    ]
}"""

self.wfile.write(DEBUG_JSON.encode())

from urllib.parse import urlparse, urlsplit
U1 = "http://1.2.3.4/x/y/z/?q=nnn&f1=k&t1=j#g"
U2 = "http://1.2.3.4/x/y/z?q=nnn&f1=k&t1=j#g"
print(urlparse(U1))
print(urlparse(U2))

if __name__ == "__main__":
    loadconf()
    from code import interact
    interact(local=locals())
    from pprint import pprint
    pprint(storage)
    data = [ [ n['id'], n['name'], -1, "" ] for n in storage['nodes'] ]
    pprint(data)
    breakpoint()

print(json.dumps(d))
json.dump(d, sys.stdout)

print(getcwd())
print(environ['PWD'])

parser = ArgumentParser()
parser.add_argument("-a")
parser.add_argument("-f")
parser.add_argument("-b")
parsed = parser.parse_args()

class BackendHTTPRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

print(proc.poll())

socket(AF_INET, SOCK_STREAM).bind(("127.0.0.1", port,))
# print(detect(1080))

def avail():
    try:
        s = create_server(("127.0.0.1", BENCHMARK_PORT,), family=AF_INET)
        s.close()
        print(f"[EE] trojan not running on port {port}")
        r = True
    except OSError as e:
        assert e.errno == EADDRINUSE
        print(f"[..] trojan detected on port {port}")
        r = False
    return r

def avail0():
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", BENCHMARK_PORT,))
    s.close()

from inspect import currentframe
def WAI(): # where am i
    print(f"line {currentframe().f_back.f_lineno}")
