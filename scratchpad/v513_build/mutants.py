#!/usr/bin/env python3
"""Build flag-mutant copies of bots/_v513siegecrew under scratch, run a small
paired set of each with FS_LOG on, and tally the stderr mechanism counters.

EVERY GUARD IS DRIVEN BOTH WAYS: the ON arm must show the behaviour and the
mutant arm must show its absence.  These are MECHANISM probes at small n, not
currency reads -- the currency read is the 60-game grid.
"""
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

REPO = "/Users/junghard/Projects/Work/florent-code-game"
FC = os.path.join(REPO, ".venv/bin/fcode")
SCR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(REPO, "bots/_v513siegecrew")
OPP = os.path.join(REPO, "bots/_v488beltbreak2")
MAPS = ["glacierkeep", "nordkap", "atoll", "midgard", "drakkarfjord"]

MUTANTS = {
    "on": [],
    "door_off": [("FS_HOME_TURRET_RESPONSE = True", "FS_HOME_TURRET_RESPONSE = False")],
    "salt_off": [("FS_SALT_GATE = True", "FS_SALT_GATE = False")],
    "belt_off": [("FS_BELT_LASTLINK = True", "FS_BELT_LASTLINK = False")],
    "crew_var": [("FS_CREW_ON = False", "FS_CREW_ON = True")],
    "evict_off": [("FS_CREW_EVICT_NOWAIT = True", "FS_CREW_EVICT_NOWAIT = False")],
    "prestand_off": [("FS_PRESTAND_AVOID = True", "FS_PRESTAND_AVOID = False")],
    "retreat_off": [("FS_RETREAT_ON = True", "FS_RETREAT_ON = False")],
    "spawn_off": [("FS_SPAWN_PURPOSE = True", "FS_SPAWN_PURPOSE = False")],
    "convert_var": [("FS_CREW_CONVERT = False", "FS_CREW_CONVERT = True")],
    "latch_var": [("FS_SALT_LATCH = False", "FS_SALT_LATCH = True")],
    "crewflag_off": [("LOKI_FS_CREW = True ", "LOKI_FS_CREW = False")],
}

TAGS = ("DOOR ", "DOORSEEN", "SEAL ", "SENTINEL ", "EVICTOR ", "RUNG ",
        "DODGE ", "RETREAT ", "PROMOTE ", "DEGRADE ", "PHASE ", "STAT ")


def build(name):
    dst = os.path.join(SCR, "mut", name)
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    p = os.path.join(dst, "doctrine.py")
    s = open(p).read()
    s = s.replace("FS_LOG = False ", "FS_LOG = True  ", 1)
    for a, b in MUTANTS[name]:
        assert s.count(a) >= 1, (name, a)
        s = s.replace(a, b, 1)
    open(p, "w").write(s)
    return dst


def one(job):
    arm, name, mp, i, seed, ord_a = job
    first, second = (arm, OPP) if ord_a else (OPP, arm)
    cmd = [FC, "run", first, second,
           os.path.join(REPO, "maps", mp + ".map26"),
           "--seed", str(seed), "--tle", "10"]
    try:
        pr = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return name, mp, {}, "TIMEOUT", -1, -1, 0
    err = pr.stderr
    counts = {t.strip(): err.count("FS " + t) for t in TAGS}
    counts["Traceback"] = err.count("Traceback")
    win, turn, cond = "NOWINNER", -1, "-"
    m = re.search(r"Winner:\s+(\S+)\s+\((.*), turn (\d+)\)", pr.stdout)
    if m:
        win, cond, turn = m.group(1), m.group(2), int(m.group(3))
    mined = -1
    m2 = re.search(r"Titanium\s+(\d+)\s+\((\d+) mined\)\s+(\d+)\s+\((\d+) mined\)",
                   pr.stdout)
    if m2:
        mined = int(m2.group(2)) if ord_a else int(m2.group(4))
    ours = 1 if os.path.basename(arm) == win else 0
    # sentinels bought BEFORE the collar closed: a SENTINEL line with no
    # preceding "orth 0" STAT for that game
    pre = 0
    sealed = False
    for line in err.splitlines():
        if "FS STAT" in line and " orth 0 " in line:
            sealed = True
        if "FS PHASE" in line and (" ph 3 " in line or " ph 4 " in line):
            sealed = True
        if "FS SENTINEL" in line and not sealed:
            pre += 1
    counts["SENT_PRESEAL"] = pre
    return name, mp, counts, cond, turn, mined, ours


def main():
    names = sys.argv[1:] or list(MUTANTS)
    reps = int(os.environ.get("REPS", "2"))
    jobs = []
    for name in names:
        arm = build(name)
        for mp in MAPS:
            for i in range(reps):
                jobs.append((arm, name, mp, i, 7400 + i, i % 2 == 0))
    agg = {}
    with ThreadPoolExecutor(max_workers=int(os.environ.get("PAR", "6"))) as ex:
        for name, mp, counts, cond, turn, mined, ours in ex.map(one, jobs):
            a = agg.setdefault(name, {"games": 0, "wins": 0, "tic0": 0,
                                      "r1000": 0, "kill300": 0})
            a["games"] += 1
            a["wins"] += ours
            if mined == 0:
                a["tic0"] += 1
            if turn >= 999:
                a["r1000"] += 1
            if ours and "Core" in cond and turn <= 300:
                a["kill300"] += 1
            for k, v in counts.items():
                a[k] = a.get(k, 0) + v
    keys = ["games", "wins", "tic0", "r1000", "kill300", "Traceback", "DOOR",
            "DOORSEEN", "SEAL", "SENTINEL", "SENT_PRESEAL", "EVICTOR", "RUNG",
            "DODGE", "RETREAT", "PROMOTE", "DEGRADE"]
    print("\t".join(["arm"] + keys))
    for name in names:
        a = agg.get(name, {})
        print("\t".join([name] + [str(a.get(k, 0)) for k in keys]))


if __name__ == "__main__":
    main()
