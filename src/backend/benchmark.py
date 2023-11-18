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
from random import shuffle
from signal import SIGINT
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from subprocess import Popen, DEVNULL
from threading import Thread
from time import sleep
import json
import storage

PLACEHOLDER_NOT_TESTED_YET =  77777 # 78s
PLACEHOLDER_TIMEOUT        =  88888 # 89s

ff = None

benchmarking = 0

# from inspect import currentframe
# def WAI(): # where am i
#     print(f"line {currentframe().f_back.f_lineno}")

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

exit_request = False

def wait_until_open():
    global exit_request
    exit_request = False
    if avail():
        # print("wait until port is open ...")
        while ( not exit_request ) and avail():
            pass

def wait_until_avail():
    global exit_request
    exit_request = False
    if not avail():
        # print("wait until port is available ...")
        while ( not exit_request ) and ( not avail() ):
            pass

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
    global exit_request
    benchmarking = 1
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
        t = Thread(target=wait_until_open)
        t.start()
        t.join(timeout=int(BENCHMARK_TIMEOUT_MS/1000))
        timeout = True if t.is_alive() else False
        exit_request = True
        # WAI()
        if not timeout:
            # WAI()
            # print("httping ...")
            n['latency'] = httping()
        p.send_signal(SIGINT)
        # print("wait until trojan exits ...")
        p.wait()
        wait_until_avail()
        print()
        Path("benchmark.json").unlink(missing_ok=False)
        # WAI()
        if timeout:
            # WAI()
            benchmarking = 2
            break
        # WAI()

    match benchmarking:
        case 2:
            print("error a9gh4z - benchmark stopped")
        case 1:
            benchmarking = 0
            print(f"total: {datetime.now() - t0}")
            storage.storage_save()
        case _:
            raise RuntimeError()

    print()
