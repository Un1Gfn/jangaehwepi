#!/dev/null

# https://stackoverflow.com/questions/4145775/how-do-i-convert-a-python-list-into-a-c-array-by-using-ctypes
# https://stackoverflow.com/questions/26277322/passing-arrays-with-ctypes
# https://stackoverflow.com/questions/18679264/how-to-use-malloc-and-free-with-python-ctypes

from copy import deepcopy
from time import sleep
from ctypes import c_char_p, c_int64, c_long, CDLL
from datetime import datetime
from errno import EADDRINUSE
from lnk_conf import *
from pathlib import Path
from random import shuffle
from signal import SIGINT
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from subprocess import Popen, DEVNULL
import json
import storage

PLACEHOLDER_NOT_TESTED_YET =  77777 # 78s
PLACEHOLDER_TIMEOUT        =  88888 # 89s

ff = None

benchmarking = False

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
        # print("wait until port is open ...")
        while avail():
            pass

def wait_until_avail():
    if not avail():
        # print("wait until port is available ...")
        while not avail():
            pass

def init():
    global ff
    dll = CDLL("./httping.so")
    dll.init()
    ff = dll.ff
    ff.argtypes = [ c_char_p, c_char_p, c_long ]
    ff.restype = c_int64

def httping():
    minimum = PLACEHOLDER_TIMEOUT
    global ff
    url = BENCHMARK_URL.encode()
    proxy = f"socks5h://127.0.0.1:{BENCHMARK_PORT}".encode()
    for _ in range(3):
        lns = ff(url, proxy, BENCHMARK_TIMEOUT_MS)
        lms = int(lns/(1000*1000))
        if lns == -1:
            print("CURLE_OPERATION_TIMEDOUT")
            return minimum
        print(f"{lms} ms ... {lns} ns")
        if lms < minimum: minimum = lms
    return minimum

def benchmark():

    global benchmarking
    benchmarking = True
    sleep(1)
    for n in storage.storage['nodes']:
        n['latency'] = PLACEHOLDER_NOT_TESTED_YET
    print()

    l = list(range(len(storage.storage['nodes'])))
    shuffle(l)
    wait_until_avail()

    t0 = datetime.now()

    for (index, id,) in enumerate(l):

        n = storage.storage['nodes'][id]
        c = n['conf']

        if storage.is_blacklisted(c):
            print(f"[{index + 1}/{len(l)}] #{index} {n['name']} ... banned\n")
            continue
        else:
            print(f"[{index + 1}/{len(l)}] #{index} {n['name']} ... 127.0.0.1:{BENCHMARK_PORT} => {c['remote_addr']}:{c['remote_port']}")

        with open("benchmark.json", 'w') as f:
            c2 = deepcopy(c)
            c2['local_addr'] = "127.0.0.1"
            c2['local_port'] = BENCHMARK_PORT
            json.dump(c2, f, ensure_ascii=True, indent="  ", )

        p = Popen([CPPTROJAN_PATH, "-c", "benchmark.json"], stdout=DEVNULL, stderr=DEVNULL)
        wait_until_open()

        # print("httping ...")
        n['latency'] = httping()

        p.send_signal(SIGINT)
        # print("wait until trojan exits ...")
        p.wait()
        wait_until_avail()
        print()

        Path("benchmark.json").unlink(missing_ok=False)

    benchmarking = False
    print(f"total: {datetime.now() - t0}")
    print()
    storage.storage_save()
