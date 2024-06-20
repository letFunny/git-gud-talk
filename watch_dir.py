import os
import sys
import hashlib
from time import sleep

from blessings import Terminal

t = Terminal()

def get_dir_snapshot(path: str):
    snapshot = {}
    for root, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            with open(filepath, "rb") as fp:
                snapshot[filepath] = hashlib.blake2b(fp.read()).digest()
    return snapshot
def get_snapshot_diff(prev, curr):
    changed = []
    deleted = []
    added = []
    for p in prev:
        if not p in curr:
            deleted.append(p)
        elif curr[p] != prev[p]:
            changed.append(p)
    for p in curr:
        if not p in prev:
            added.append(p)
    return added, deleted, changed


if len(sys.argv) <= 1:
    print("Expected a directory")
    exit(-1)

print(t.clear())

dir_path = sys.argv[1]
last_snapshot = get_dir_snapshot(dir_path)
while True:
    snapshot = get_dir_snapshot(dir_path)
    added, deleted, changed = get_snapshot_diff(last_snapshot, snapshot)
    last_snapshot = snapshot
    if len(added) + len(deleted) + len(changed) == 0:
        sleep(1)
        continue

    print(t.clear())
    with t.location(0, 0):
        for f in sorted(added):
            print(t.green("+ {}".format(f)))
        for f in sorted(changed):
            print(t.blue("* {}".format(f)))
        for f in sorted(deleted):
            print(t.red("- {}".format(f)))

    sleep(1)

