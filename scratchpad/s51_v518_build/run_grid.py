#!/usr/bin/env python3
"""s51 RUSH-AUTOPSY grid: 5 maps x 3 seeds x 2 seats = 30 games, replays+logs kept.

Adapted from scratchpad/s51_v515_build/run_grid.py.  Difference: seeds and seats
are a full cross product (3 x 2), not interleaved by index, and BOTH stdout and
stderr are written per game.
"""
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

REPO = "/Users/junghard/Projects/Work/florent-code-game"
FC = os.path.join(REPO, ".venv/bin/fcode")
SCR = os.path.dirname(os.path.abspath(__file__))
OPP = os.environ.get("OPP") or os.path.join(REPO, "bots/_v488beltbreak2")
MAPS = (os.environ.get("MAPS") or
        "atoll,drakkarfjord,glacierkeep,midgard,nordkap").split(",")
SEEDS = [int(x) for x in (os.environ.get("SEEDS") or "1,2,3").split(",")]


def one(job):
    arm, mp, seed, ord_a, repdir, logdir = job
    tag = "%s_s%d_%s" % (mp, seed, "A" if ord_a else "B")
    rp = os.path.join(repdir, tag + ".replay26")
    first, second = (arm, OPP) if ord_a else (OPP, arm)
    cmd = [FC, "run", first, second,
           os.path.join(REPO, "maps", mp + ".map26"),
           "--seed", str(seed), "--tle", "10", "--replay", rp]
    try:
        pr = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    except subprocess.TimeoutExpired:
        return "%s\tTIMEOUT" % tag
    out = pr.stdout
    open(os.path.join(logdir, tag + ".err"), "w").write(pr.stderr)
    open(os.path.join(logdir, tag + ".out"), "w").write(out)
    win, turn, cond = "NOWINNER", -1, "-"
    for line in out.splitlines():
        if "Winner:" in line:
            m = re.search(r"Winner:\s+(\S+)\s+\((.*), turn (\d+)\)", line)
            if m:
                win, cond, turn = m.group(1), m.group(2), int(m.group(3))
            break
    mined_a = mined_b = -1
    m = re.search(r"Titanium\s+(\d+)\s+\((\d+) mined\)\s+(\d+)\s+\((\d+) mined\)",
                  out)
    if m:
        mined_a, mined_b = int(m.group(2)), int(m.group(4))
    ours_mined = mined_a if ord_a else mined_b
    opp_mined = mined_b if ord_a else mined_a
    armname = os.path.basename(arm)
    ours = "US" if armname == win else ("OPP" if win != "NOWINNER" else "NONE")
    tb = len(re.findall(r"Traceback", pr.stderr))
    return "\t".join(str(x) for x in [
        tag, mp, seed, "A" if ord_a else "B", ours, win, cond,
        turn, tb, ours_mined, opp_mined])


def main():
    arm = sys.argv[1]
    outp = sys.argv[2]
    repdir = sys.argv[3]
    logdir = sys.argv[4]
    os.makedirs(repdir, exist_ok=True)
    os.makedirs(logdir, exist_ok=True)
    jobs = []
    for mp in MAPS:
        for seed in SEEDS:
            for ord_a in (True, False):
                jobs.append((arm, mp, seed, ord_a, repdir, logdir))
    with open(outp, "w") as fh:
        fh.write("tag\tmap\tseed\tseat\tours\twinner\tcond\tturn"
                 "\ttracebacks\tours_mined\topp_mined\n")
        fh.flush()
        with ThreadPoolExecutor(max_workers=int(os.environ.get("PAR", "4"))) as ex:
            for r in ex.map(one, jobs):
                fh.write(r + "\n")
                fh.flush()
                print(r, flush=True)


if __name__ == "__main__":
    main()
