#!/dev/null
# https://github.com/trojan-gfw/trojan/blob/master/docs/usage.md

import json
from storage import storage
from subprocess import Popen

p = None

def deactivate():
    p.kill()
    storage['active'] = -1
    print("deactivated.")

def activate(id):
    global p
    with open("/tmp/jangaehwepi.active.json", 'w') as f:
        json.dump(storage['nodes'][id]['conf'], f, ensure_ascii=True, indent="  ", )
    p = Popen(["/usr/bin/trojan", "-c", "/tmp/jangaehwepi.active.json"])
    print("activated.")
