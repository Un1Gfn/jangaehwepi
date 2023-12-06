#!/dev/null
# https://github.com/trojan-gfw/trojan/blob/master/docs/usage.md

from lnk_conf import *
from pathlib import Path
from subprocess import Popen
import json
import storage

p = None

def deactivate():
    p.terminate()
    print(p.poll())
    try: Path("active.json").unlink(missing_ok=False)
    except FileNotFoundError: pass
    storage.storage['active'] = -1
    print("deactivated.")

def ss_args(config, port):
    # aes-256-cfb has been removed from shadowsocks-rust
    # l = [
    #     PATH_SHADOWSOCKSRUST,
    #     "-b", f"{SOCKS5_ADDR}:{SOCKS5_PORT}",
    #     "-U",
    #     "-s", f"{c['mjm3lo_ip']}:{c['mjm3lo_port']}",
    #     "-k", c['mjm3lo_secret'],
    #     "-m", "aes-256-cfb",
    #     "--tcp-fast-open",
    # ]
    l = [
        PATH_SHADOWSOCKSLIBEV,
        "-s", config['mjm3lo_ip'],
        "-p", str(config['mjm3lo_port']),
        "-l", str(port),
        "-k", config['mjm3lo_secret'],
        "-m", "aes-256-cfb",
        "-b", SOCKS5_ADDR,
        "-u",
        "--reuse-port",
        "--fast-open",
        "-v",
    ]
    return l

def activate(id):

    global p
    n = storage.storage['nodes'][id]
    c = n['conf']

    match n['type']:

        case 'trojan':
            with open("active.json", 'w') as f:
                json.dump(c, f, ensure_ascii=True, indent="  ", )
                p = Popen([PATH_CPPTROJAN, "-c", "active.json"])
                print("activated.")

        case 'ss':
            l = ss_args(c, SOCKS5_PORT)
            print(l)
            p = Popen(l)
            print("activated.")

        case _:
            raise RuntimeError
