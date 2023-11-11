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
    Path("active.json").unlink(missing_ok=False)
    storage.storage['active'] = -1
    print("deactivated.")

def activate(id):
    global p
    with open("active.json", 'w') as f:
        json.dump(storage.storage['nodes'][id]['conf'], f, ensure_ascii=True, indent="  ", )
    p = Popen([CPPTROJAN_PATH, "-c", "active.json"])
    print("activated.")
