#!/usr/bin/env python3
"""v526 battery runner.  PAR=2 STRICT across ALL arms (the two full-pool
shards PINCERPOOL and FLIPPOOL own the cores), arms INTERLEAVED inside a block
so the three arms share the same wall-clock slice -- v518 finding 2 measured a
4.6pp FALSE POSITIVE at n=810/arm on byte-identical play from pooling
non-time-adjacent local fixtures.

One row per game:
  tag map seed seat arm ours winner cond turn tracebacks ours_mined opp_mined

Env:
  ARMS   "name=path,name=path,..."      MAPS  comma list
  SEEDS  comma list                     PAR   worker count (default 2)
  OUT    output dir
"""
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

REPO = "/Users/junghard/Projects/Work/florent-code-game"
FC = os.path.join(REPO, ".venv/bin/fcode")
OPP = os.environ.get("OPP") or os.path.join(REPO, "bots/_v488beltbreak2")
KEEP_ERR = os.environ.get("KEEP_ERR", "0") == "1"


def one(job):
    arm_name, arm_path, mp, seed, ord_a, out = job
    tag = "%s_%s_s%d_%s" % (arm_name, mp, seed, "A" if ord_a else "B")
    rp = os.path.join(out, "rep", tag + ".replay26")
    first, second = (arm_path, OPP) if ord_a else (OPP, arm_path)
    cmd = [FC, "run", first, second,
           os.path.join(REPO, "maps", mp + ".map26"),
           "--seed", str(seed), "--tle", "10", "--replay", rp]
    try:
        pr = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    except subprocess.TimeoutExpired:
        return "%s\t%s\tTIMEOUT" % (tag, mp)
    if KEEP_ERR:
        open(os.path.join(out, "log", tag + ".err"), "w").write(pr.stderr)
    win, turn, cond = "NOWINNER", -1, "-"
    for line in pr.stdout.splitlines():
        if "Winner:" in line:
            m = re.search(r"Winner:\s+(\S+)\s+\((.*), turn (\d+)\)", line)
            if m:
                win, cond, turn = m.group(1), m.group(2), int(m.group(3))
            break
    mined_a = mined_b = -1
    m = re.search(
        r"Titanium\s+(\d+)\s+\((\d+) mined\)\s+(\d+)\s+\((\d+) mined\)",
        pr.stdout)
    if m:
        mined_a, mined_b = int(m.group(2)), int(m.group(4))
    ours_mined = mined_a if ord_a else mined_b
    opp_mined = mined_b if ord_a else mined_a
    armbase = os.path.basename(arm_path)
    ours = "US" if armbase == win else ("OPP" if win != "NOWINNER" else "NONE")
    tb = len(re.findall(r"Traceback", pr.stderr))
    return "\t".join(str(x) for x in [
        tag, mp, seed, "A" if ord_a else "B", arm_name, ours, win, cond,
        turn, tb, ours_mined, opp_mined])


def main():
    out = os.environ["OUT"]
    os.makedirs(os.path.join(out, "rep"), exist_ok=True)
    os.makedirs(os.path.join(out, "log"), exist_ok=True)
    arms = [a.split("=", 1) for a in os.environ["ARMS"].split(",")]
    maps = os.environ["MAPS"].split(",")
    seeds = [int(x) for x in os.environ["SEEDS"].split(",")]
    jobs = []
    # interleave: for each (map, seed, seat) cell, all arms adjacent
    for mp in maps:
        for seed in seeds:
            for ord_a in (True, False):
                for name, path in arms:
                    jobs.append((name, os.path.join(REPO, path), mp, seed,
                                 ord_a, out))
    tsv = os.path.join(out, "results.tsv")
    new = not os.path.exists(tsv)
    with open(tsv, "a") as fh:
        if new:
            fh.write("tag\tmap\tseed\tseat\tarm\tours\twinner\tcond\tturn"
                     "\ttracebacks\tours_mined\topp_mined\n")
            fh.flush()
        with ThreadPoolExecutor(
                max_workers=int(os.environ.get("PAR", "2"))) as ex:
            for r in ex.map(one, jobs):
                fh.write(r + "\n")
                fh.flush()
    print("DONE %s (%d games)" % (out, len(jobs)), flush=True)


if __name__ == "__main__":
    main()
