#!/usr/bin/env python3
"""GATED-LEG FALSIFIER: does seat 3 still walk to the enemy ring on a board the
ferry-siege refuses?

v520 open item 7: two `fs_crew_on()` read sites sit OUTSIDE the map gate, so on
a gated board seat 3 was issued as a RAIDER rather than an eco expander.  The
engine-side signature of that is a builder body of ours crossing into the enemy
half; the replay-side count is the falsifier for v521 change 0.

  fwd_bodies   distinct builder bots of ours that ever reach d^2 <= 50 of the
               enemy core centre (the ATRING envelope seatrate.py uses)
  harv         harvesters of ours built (the thing an eco seat buys instead)

⛔ GUARD, DRIVEN BOTH WAYS: a team-swap control must MOVE both columns; and a
d^2 threshold of 0 must return fwd_bodies = 0 on the same replay (an instrument
that ignored the envelope returns the same number).
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from ringwalk import dsq_centre, replay_map, walk  # noqa: E402


def analyse(replay, our_team, dsq=50):
    _w, _h, _rows, cores = replay_map(replay)
    E = {c["team"]: c["pos"] for c in cores}[1 - our_team]
    fwd, harv = set(), set()
    for _rnd, ents in walk(replay):
        for eid, (kind, team, pos, _b) in ents.items():
            if team != our_team:
                continue
            if kind == "builder_bot" and dsq_centre(pos, E) <= dsq:
                fwd.add(eid)
            elif kind == "harvester":
                harv.add(eid)
    return len(fwd), len(harv)


def main():
    if sys.argv[1] == "--selftest":
        rp = sys.argv[2]
        a = analyse(rp, 0)
        b = analyse(rp, 1)
        z = analyse(rp, 0, dsq=0)
        ok = (a != b) and z[0] == 0
        print("team0", a, "team1", b, "dsq0", z)
        print("SELFTEST", "PASS" if ok else "FAIL")
        sys.exit(0 if ok else 1)
    grid, repdir, label = sys.argv[1], sys.argv[2], sys.argv[3]
    rows = list(csv.DictReader(open(grid), delimiter="\t"))
    tot_f = tot_h = n = 0
    for r in rows:
        rp = Path(repdir) / (r["tag"] + ".replay26")
        if not rp.exists():
            continue
        our = 0 if r["seat"] == "A" else 1
        f, h = analyse(str(rp), our)
        tot_f += f
        tot_h += h
        n += 1
    print("%-14s n=%d  fwd_bodies/game=%.2f  harvesters/game=%.2f"
          % (label, n, tot_f / n if n else 0, tot_h / n if n else 0))


if __name__ == "__main__":
    main()
