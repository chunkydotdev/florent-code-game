#!/usr/bin/env python3
"""Launcher lifecycle census: where do our launchers get built, and do they die?

Reads replays; for every launcher of OURS records build round, death round (or
None = stood to game end), tile, dsq to enemy core centre and to our own core
centre.  Classifies by site:
    RING   dsq_opp <= 8      (eviction-only by construction)
    HOP    otherwise, and beyond FS_HOME_NEAR of our own core
    HOME   near our own core (the chassis home-ferry launcher)

Usage: launcher_census.py <replaydir> [--tag-seat]
Emits TSV to stdout, one row per launcher.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game/scratchpad/s51_rush_autopsy")
from tools.replay_census import WIRE_LEN, fields, parse_entity, read_pos  # noqa: E402


def dsq(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def run(path: Path, our_team: int):
    data = path.read_bytes()
    mb = None
    turns = []
    for n, w, v in fields(data):
        if n == 1 and w == WIRE_LEN:
            mb = v
        elif n == 3 and w == WIRE_LEN:
            turns.append(v)
    cores = []
    for n, _w, v in fields(mb):
        if n == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(v):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    ctr = {c["team"]: (c["pos"][0] + .5, c["pos"][1] + .5) for c in cores}
    lau = {}
    ents = set()
    for rnd, tb in enumerate(turns):
        for _n, _w, ub in fields(tb):
            for un, _uw, ubuf in fields(ub):
                if un == 1:
                    for en, _ew, eb in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None or e.id in ents:
                            continue
                        ents.add(e.id)
                        if e.kind == "launcher" and e.team == our_team:
                            lau[e.id] = dict(
                                id=e.id, pos=e.pos, built=rnd, died=None,
                                dsq_opp=dsq(e.pos, ctr[1 - our_team]),
                                dsq_own=dsq(e.pos, ctr[our_team]))
                elif un == 3:
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            ents.discard(rv)
                            if rv in lau and lau[rv]["died"] is None:
                                lau[rv]["died"] = rnd
    end = len(turns) - 1
    for r in lau.values():
        r["end"] = end
        r["life"] = (r["died"] if r["died"] is not None else end) - r["built"]
        r["stood"] = 1 if r["died"] is None else 0
        if r["dsq_opp"] <= 8:
            r["site"] = "RING"
        elif r["dsq_own"] <= 12:
            r["site"] = "HOME"
        else:
            r["site"] = "HOP"
    return lau


COLS = ["tag", "id", "x", "y", "site", "built", "died", "life", "stood",
        "dsq_opp", "dsq_own", "end"]


def main():
    d = Path(sys.argv[1])
    print("\t".join(COLS))
    for p in sorted(d.glob("*.replay26")):
        tag = p.stem
        our_team = 0 if tag.endswith("_A") else 1
        try:
            lau = run(p, our_team)
        except Exception as exc:            # noqa: BLE001
            print("# ERR %s %s" % (tag, exc), file=sys.stderr)
            continue
        for r in sorted(lau.values(), key=lambda z: z["built"]):
            print("\t".join(str(x) for x in [
                tag, r["id"], r["pos"][0], r["pos"][1], r["site"], r["built"],
                r["died"] if r["died"] is not None else -1, r["life"],
                r["stood"], r["dsq_opp"], r["dsq_own"], r["end"]]))


if __name__ == "__main__":
    main()
