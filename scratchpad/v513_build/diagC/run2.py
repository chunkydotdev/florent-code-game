#!/usr/bin/env python3
"""diagC: 6 instrumented games on the two failing maps, vs _v488beltbreak2."""
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

REPO = "/Users/junghard/Projects/Work/florent-code-game"
FC = os.path.join(REPO, ".venv/bin/fcode")
SCR = os.path.dirname(os.path.abspath(__file__))
REP = os.path.join(SCR, "replays2")
os.makedirs(REP, exist_ok=True)

ARM = os.path.join(SCR, "arm2")
OPP = os.path.join(REPO, "bots/_v488beltbreak2")
JOBS = [("glacierkeep", 5), ("glacierkeep", 7), ("glacierkeep", 0)]
        


def one(job):
    mp, i = job
    seed = 7300 + i
    tag = "%s_g%d" % (mp, i)
    rp = os.path.join(REP, tag + ".replay26")
    ord_a = (i % 2 == 0)
    first, second = (ARM, OPP) if ord_a else (OPP, ARM)
    cmd = [FC, "run", first, second, os.path.join(REPO, "maps", mp + ".map26"),
           "--seed", str(seed), "--tle", "10", "--replay", rp]
    pr = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    open(os.path.join(REP, tag + ".err"), "w").write(pr.stderr)
    win, turn, cond = "NOWINNER", -1, "-"
    for line in pr.stdout.splitlines():
        if "Winner:" in line:
            m = re.search(r"Winner:\s+(\S+)\s+\((.*), turn (\d+)\)", line)
            if m:
                win, cond, turn = m.group(1), m.group(2), int(m.group(3))
            break
    return "\t".join(str(x) for x in [tag, mp, seed, "A" if ord_a else "B",
                                      win, cond, turn])


if __name__ == "__main__":
    with open(os.path.join(SCR, "batch2.tsv"), "w") as fh:
        fh.write("tag\tmap\tseed\tord\twinner\tcond\tturn\n")
        with ThreadPoolExecutor(max_workers=6) as ex:
            for r in ex.map(one, JOBS):
                fh.write(r + "\n")
                fh.flush()
                print(r, flush=True)
