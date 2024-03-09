#!/dev/null

# https://stackoverflow.com/questions/4145775/how-do-i-convert-a-python-list-into-a-c-array-by-using-ctypes
# https://stackoverflow.com/questions/26277322/passing-arrays-with-ctypes
# https://stackoverflow.com/questions/18679264/how-to-use-malloc-and-free-with-python-ctypes

from copy import deepcopy
from ctypes import c_char_p, c_int64, c_long, CDLL
from datetime import datetime
from errno import EADDRINUSE
from lnk_conf import *
from os import uname
from pathlib import Path
from proxy import ss_args
from random import shuffle
from signal import SIGINT
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from subprocess import Popen, DEVNULL
from threading import Thread
from time import sleep
import json
import storage

ff = None

PLACEHOLDER_NOT_TESTED_YET = -128

benchmarking = 0

exit_request_checkport = False

exit_request_benchmark = False

from inspect import currentframe
def WAI(): # where am i
    print(f"line {currentframe().f_back.f_lineno}")

def avail():
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    try:
        s.bind(("127.0.0.1", BENCHMARK_PORT,))
        r = True
    except OSError as e:
        assert e.errno == EADDRINUSE
        r = False
    s.close()
    return r

def wait_until_open():
    global exit_request_checkport
    exit_request_checkport = False
    if avail():
        # print("wait until port is open ...")
        while ( not exit_request_checkport ) and avail():
            sleep(0.1)

def wait_until_avail():
    global exit_request_checkport
    exit_request_checkport = False
    if not avail():
        # print("wait until port is available ...")
        while ( not exit_request_checkport ) and ( not avail() ):
            sleep(0.1)

def init():
    global ff
    match uname().sysname:
        case 'Darwin': dll = CDLL("./httping.dylib")
        case 'Linux':  dll = CDLL("./httping.so")
        case _: raise RuntimeError
    dll.init()
    ff = dll.ff
    ff.argtypes = [ c_char_p, c_char_p, c_long ]
    ff.restype = c_int64

def httping():
    minimum = BENCHMARK_TIMEOUT_MS
    global ff
    url = BENCHMARK_URL.encode()
    proxy = f"socks5h://127.0.0.1:{BENCHMARK_PORT}".encode()
    for _ in range(3):
        lns = ff(url, proxy, BENCHMARK_TIMEOUT_MS)
        lms = int(lns/(1000*1000))
        if lns < 0 :
            return lns
        print(f"{lms} ms ... {lns} ns")
        if lms < minimum:
            minimum = lms
    return minimum

def benchmark():

    global benchmarking
    global exit_request_checkport
    global exit_request_benchmark

    benchmarking = 1
    sleep(1)
    for n in storage.storage['nodes']:
        n['latency'] = PLACEHOLDER_NOT_TESTED_YET
    print()

    length = len(storage.storage['nodes'])
    l = list(range(length))
    shuffle(l)
    wait_until_avail()

    exit_request_benchmark = False
    t0 = datetime.now()

    for (index, id,) in enumerate(l):

        if exit_request_benchmark:
            break

        n = storage.storage['nodes'][id]
        c = n['conf']
        header = f"[{index + 1}/{length}] #{id} {n['name']}\n"
        if storage.is_blacklisted(n):
            print(f"{header}banned\n")
            continue
        else:
            match n['type']:
                case 'trojan':
                    print(f"{header}127.0.0.1:{BENCHMARK_PORT} => {c['remote_addr']}:{c['remote_port']}")
                case 'ss':
                    print(f"{header}127.0.0.1:{BENCHMARK_PORT} => {c['server']}:{c['server_port']}")

        match n['type']:
            case 'trojan':
                with open("benchmark.json", 'w') as f:
                    c2 = deepcopy(c)
                    c2['local_addr'] = "127.0.0.1"
                    c2['local_port'] = BENCHMARK_PORT
                    json.dump(c2, f, ensure_ascii=True, indent="  ", )
                p = Popen([PATH_CPPTROJAN, "-c", "benchmark.json"], stdout=DEVNULL, stderr=DEVNULL)
            case 'ss':
                l = ss_args(c, BENCHMARK_PORT)
                p = Popen(l, stdout=DEVNULL, stderr=DEVNULL)
            case _:
                raise RuntimeError

        t = Thread(target=wait_until_open)
        t.start()
        t.join(timeout=int(BENCHMARK_TIMEOUT_MS/1000))
        exit_request_checkport = True
        n['latency'] = httping()
        p.send_signal(SIGINT)
        p.wait()
        wait_until_avail()
        print()
        try: Path("benchmark.json").unlink(missing_ok=False)
        except FileNotFoundError: pass

    match benchmarking:
        case 1:
            benchmarking = 0
            print(f"total: {datetime.now() - t0}")
            storage.storage_save()
        case _:
            raise RuntimeError()

    print()
