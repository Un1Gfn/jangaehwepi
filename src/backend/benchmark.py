#!/dev/null

# https://stackoverflow.com/questions/4145775/how-do-i-convert-a-python-list-into-a-c-array-by-using-ctypes
# https://stackoverflow.com/questions/26277322/passing-arrays-with-ctypes
# https://stackoverflow.com/questions/18679264/how-to-use-malloc-and-free-with-python-ctypes

from copy import deepcopy
from ctypes import c_char_p, c_int64, c_long, CDLL
from errno import EADDRINUSE
from lnk_conf import *
from pathlib import Path
from random import shuffle
from signal import SIGINT
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from subprocess import Popen, DEVNULL
import json
import storage

ff = None

def avail():
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    try:
        s.bind(("127.0.0.1", BENCHMARK_PORT,))
        s.close()
        return True
    except OSError as e:
        assert e.errno == EADDRINUSE
    return False

def wait_until_open():
    if avail():
        print("wait until port is open ...")
        while avail():
            pass

def wait_until_avail():
    if not avail():
        print("wait until port is available ...")
        while not avail():
            pass

def init():
    global ff
    dll = CDLL("./httping.so")
    dll.init()
    ff = dll.ff
    ff.argtypes = [ c_char_p, c_char_p, c_long ]
    ff.restype = c_int64

def httping(n):
    if n <= 0: return
    url = BENCHMARK_URL.encode()
    proxy = f"socks5h://127.0.0.1:{BENCHMARK_PORT}".encode()
    # https://github.com/iputils/iputils/blob/0cc6da796b9a64113152c071088701cb95a72ae8/ping/ping.h#L65
    # 4000
    # this value should be sent from frontend
    timeout_ms = 4000
    latency = ff(url, proxy, timeout_ms)
    match latency:
        case -1:
            print("CURLE_OPERATION_TIMEDOUT")
            return False
        case _:
            print(f"{latency/(1000*1000)} ms ... {latency} ns")
            httping(n-1)
            return True

def benchmark():

    print()

    assert len(storage.storage['nodes']) == 118
    l = list(range(len(storage.storage['nodes'])))
    shuffle(l)

    wait_until_avail()
    for (index, id,) in enumerate(l):

        print(f"[{index + 1}/{len(l) - 1}]")
        with open("benchmark.json", 'w') as f:
            c = deepcopy(storage.storage['nodes'][id]['conf'])
            c['local_addr'] = "127.0.0.1"
            c['local_port'] = BENCHMARK_PORT
            print(f"{c['local_addr']}:{c['local_port']} => {c['remote_addr']}:{c['remote_port']}")
            json.dump(c, f, ensure_ascii=True, indent="  ", )
        # p = Popen([CPPTROJAN_PATH, "-c", "benchmark.json"])
        p = Popen([CPPTROJAN_PATH, "-c", "benchmark.json"], stdout=DEVNULL, stderr=DEVNULL)
        wait_until_open()

        global ff
        print("httping ...")
        httping(3)

        # p.kill()
        # p.terminate()
        p.send_signal(SIGINT)
        print("wait until trojan exits ...")
        p.wait()
        wait_until_avail()
        print()

        Path("benchmark.json").unlink(missing_ok=False)
