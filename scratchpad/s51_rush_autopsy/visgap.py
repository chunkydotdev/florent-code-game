#!/usr/bin/env python3
"""Is the siege sentinel INSIDE a raider's vision when the phase reads RING?

`_fs_live_sentinels` (siege.py:2585) counts our sentinels via the RAIDER's
`get_nearby_buildings()` — i.e. builder-bot vision, r^2 = 20 — and the phase it
feeds (siege.py:885) is what the Core's magazine arms on (main.py:504).  So a
standing, firing siege sentinel that no living builder bot of ours can SEE
cannot raise the phase to KILL, and the magazine stays on the 16/24-ammo home
target.

This measures, per round, with a core-hitting sentinel of ours alive:
  * whether ANY living builder bot of ours is within d^2 <= 20 of it
  * joined to the core's own MAGTRACE phase for the same round

GUARD (driven both ways): the same computation is run with the vision radius
set to the whole map (d^2 <= 10^6).  Under that control "no bot can see it"
must fall to ~0 — if it does not, the bot-position decode is broken rather than
the vision being the binder.
"""
from __future__ import annotations

import glob
import os
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
from tools.replay_census import (  # noqa: E402
    WIRE_LEN, fields, parse_entity, read_pos,
)
from tape import dsq  # noqa: E402
from turrets import run  # noqa: E402

MAG = HERE / "mag"
VIS = 20


def bot_tracks(path):
    """round -> list of our-and-their builder bot (team, pos)."""
    data = path.read_bytes()
    turns = []
    for n, w, v in fields(data):
        if n == 3 and w == WIRE_LEN:
            turns.append(v)
    ents = {}
    per = []
    for rnd, tb in enumerate(turns):
        for _n, _w, ub in fields(tb):
            for un, _uw, ubuf in fields(ub):
                if un == 1:
                    for en, _ew, eb in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is not None and e.kind == "builder_bot":
                            ents[e.id] = [e.team, e.pos]
                elif un == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in ents and to is not None:
                        ents[eid][1] = to
                elif un == 3:
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            ents.pop(rv, None)
        per.append([tuple(v) for v in ents.values()])
    return per


def trace(path):
    out = {}
    for line in open(path, errors="replace"):
        if not line.startswith("MAGTRACE"):
            continue
        p = line.split()
        out[int(p[1])] = {k: int(v) for k, v in zip(p[2::2], p[3::2])}
    return out


def main():
    for radius, label in ((VIS, "builder vision r^2=20"),
                          (10 ** 6, "CONTROL: whole map")):
        seen = Counter()
        by_ph = Counter()
        for err in sorted(glob.glob(str(MAG / "*.err"))):
            tag = os.path.basename(err)[:-4]
            rep = MAG / (tag + ".replay26")
            if not rep.exists():
                continue
            our = 0 if tag.endswith("_A") else 1
            r = run(rep, our)
            siege = [t for t in r["turrets"].values()
                     if t["team"] == our and t["core_shots"] > 0]
            if not siege:
                continue
            bots = bot_tracks(rep)
            tr = trace(err)
            for rnd in range(min(len(bots), r["rounds"])):
                live = [t for t in siege
                        if t["built"] <= rnd
                        and (t["died"] is None or rnd < t["died"])]
                if not live:
                    continue
                ours_bots = [p for (tm, p) in bots[rnd] if tm == our]
                vis = any(dsq(b, t["pos"]) <= radius
                          for t in live for b in ours_bots)
                seen["visible" if vis else "blind"] += 1
                m = tr.get(rnd)
                if m is not None:
                    by_ph[("vis" if vis else "blind", m["ph"])] += 1
        n = sum(seen.values())
        print("== %s ==  rounds with a core-hitting sentinel alive: %d" % (label, n))
        print("   a living builder bot of ours within range: %d (%.1f%%)"
              % (seen["visible"], 100 * seen["visible"] / n))
        print("   NONE within range                        : %d (%.1f%%)"
              % (seen["blind"], 100 * seen["blind"] / n))
        if by_ph:
            for k in sorted(by_ph):
                print("      %-6s ph%d : %d" % (k[0], k[1], by_ph[k]))
        print()


if __name__ == "__main__":
    main()
