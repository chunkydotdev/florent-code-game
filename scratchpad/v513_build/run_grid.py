#!/usr/bin/env python3
"""s50 v513 grid runner.  Paired maps x reps vs a fixed opponent, local --tle 10.

Children are synchronous subprocess.run() owned by this one process; the only
PID a cleanup needs is this script's own (written to PIDS by the caller).
"""
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

REPO = "/Users/junghard/Projects/Work/florent-code-game"
FC = os.path.join(REPO, ".venv/bin/fcode")
SCR = os.path.dirname(os.path.abspath(__file__))
OPP = os.path.join(REPO, "bots/_v488beltbreak2")
MAPS = ["glacierkeep", "nordkap", "atoll", "midgard", "drakkarfjord"]


def one(job):
    arm, tag_pfx, mp, i, seed, ord_a, repdir = job
    tag = "%s_%s_g%d" % (tag_pfx, mp, i)
    rp = os.path.join(repdir, tag + ".replay26") if repdir else None
    first, second = (arm, OPP) if ord_a else (OPP, arm)
    cmd = [FC, "run", first, second,
           os.path.join(REPO, "maps", mp + ".map26"),
           "--seed", str(seed), "--tle", "10"]
    if rp:
        cmd += ["--replay", rp]
    try:
        pr = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return "%s\tTIMEOUT" % tag
    out = pr.stdout
    if repdir:
        open(os.path.join(repdir, tag + ".err"), "w").write(pr.stderr)
    win, turn, cond = "NOWINNER", -1, "-"
    for line in out.splitlines():
        if "Winner:" in line:
            m = re.search(r"Winner:\s+(\S+)\s+\((.*), turn (\d+)\)", line)
            if m:
                win, cond, turn = m.group(1), m.group(2), int(m.group(3))
            break
    # "  Titanium     16 (300 mined)    80 (1960 mined)" -- left column is the
    # bot listed FIRST on the command line.
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
        tag, tag_pfx, mp, i, seed, "A" if ord_a else "B", ours, win, cond,
        turn, tb, ours_mined, opp_mined])


def main():
    arm = sys.argv[1]
    tag_pfx = sys.argv[2]
    outp = sys.argv[3]
    reps = int(sys.argv[4])
    seed0 = int(sys.argv[5])
    repdir = sys.argv[6] if len(sys.argv) > 6 and sys.argv[6] != "-" else None
    if repdir:
        os.makedirs(repdir, exist_ok=True)
    jobs = []
    for mp in MAPS:
        for i in range(reps):
            jobs.append((arm, tag_pfx, mp, i, seed0 + i, i % 2 == 0, repdir))
    with open(outp, "w") as fh:
        fh.write("tag\tarm\tmap\tg\tseed\tord\tours\twinner\tcond\tturn"
                 "\ttracebacks\tours_mined\topp_mined\n")
        fh.flush()
        with ThreadPoolExecutor(max_workers=int(os.environ.get("PAR", "6"))) as ex:
            for r in ex.map(one, jobs):
                fh.write(r + "\n")
                fh.flush()
                print(r)


if __name__ == "__main__":
    main()
