#!/usr/bin/env python3
"""Join the core's own MAGTRACE decision variables to a REPLAY-derived
'a core-hitting sentinel of ours is alive this round' flag.

Two independent instruments per round:
  * the bot's stderr MAGTRACE line (fs_live, phase, ti, ammo, target, floor)
  * the replay's turret ledger (which of our sentinels ever hit the enemy core,
    and its build/death rounds)

Answers exactly: while a sentinel that DEMONSTRABLY can hit the enemy core is
standing, how often is the siege magazine armed, and what is in the bank?

GUARD: the number of MAGTRACE lines must equal the replay's round count for
every game (one core turn per round); a mismatch means the trace is not
per-round and every rate below is wrong.  Mismatches are reported by name
rather than averaged over.
"""
from __future__ import annotations

import glob
import os
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
from turrets import run  # noqa: E402

MAG = HERE / "mag"


def trace(path):
    out = {}
    for line in open(path, errors="replace"):
        if not line.startswith("MAGTRACE"):
            continue
        p = line.split()
        rnd = int(p[1])
        d = dict(zip(p[2::2], p[3::2]))
        out[rnd] = {k: int(v) for k, v in d.items()}
    return out


def main():
    fails = []
    rows = []
    for err in sorted(glob.glob(str(MAG / "*.err"))):
        tag = os.path.basename(err)[:-4]
        rep = MAG / (tag + ".replay26")
        if not rep.exists():
            continue
        our = 0 if tag.endswith("_A") else 1
        r = run(rep, our)
        tr = trace(err)
        if len(tr) != r["rounds"]:
            fails.append("%s: %d MAGTRACE lines vs %d replay rounds"
                         % (tag, len(tr), r["rounds"]))
        siege = [t for t in r["turrets"].values()
                 if t["team"] == our and t["core_shots"] > 0]
        for rnd in range(r["rounds"]):
            m = tr.get(rnd)
            if m is None:
                continue
            live = any(t["built"] <= rnd
                       and (t["died"] is None or rnd < t["died"])
                       for t in siege)
            rows.append((tag, rnd, live, m))
    if fails:
        sys.stderr.write("TRACE/REPLAY LENGTH MISMATCH (reported by name, not "
                         "averaged over):\n  " + "\n  ".join(fails) + "\n")
    live = [m for _t, _r, l, m in rows if l]
    dead = [m for _t, _r, l, m in rows if not l]
    print("games: %d   rounds joined: %d"
          % (len({t for t, _r, _l, _m in rows}), len(rows)))
    for label, xs in (("CORE-HITTING SENTINEL ALIVE", live),
                      ("no such sentinel alive", dead)):
        if not xs:
            continue
        n = len(xs)
        armed = sum(1 for m in xs if m["fslive"])
        print("\n== %s : %d rounds ==" % (label, n))
        print("   siege magazine ARMED : %d (%.1f%%)" % (armed, 100 * armed / n))
        print("   team ammo < 10       : %d (%.1f%%)"
              % (sum(1 for m in xs if m["ammo"] < 10),
                 100 * sum(1 for m in xs if m["ammo"] < 10) / n))
        print("   median ammo/ti/target/floor : %d / %d / %d / %d"
              % (statistics.median([m["ammo"] for m in xs]),
                 statistics.median([m["ti"] for m in xs]),
                 statistics.median([m["target"] for m in xs]),
                 statistics.median([m["floor"] for m in xs])))
        c = Counter(m["ph"] for m in xs)
        for ph in sorted(c):
            sub = [m for m in xs if m["ph"] == ph]
            print("      ph%d n=%-5d armed=%-5d med ammo=%-4d med ti=%-4d "
                  "med floor=%-4d med target=%d"
                  % (ph, len(sub), sum(1 for m in sub if m["fslive"]),
                     statistics.median([m["ammo"] for m in sub]),
                     statistics.median([m["ti"] for m in sub]),
                     statistics.median([m["floor"] for m in sub]),
                     statistics.median([m["target"] for m in sub])))


if __name__ == "__main__":
    main()
