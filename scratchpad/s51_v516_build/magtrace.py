#!/usr/bin/env python3
"""Ammunition under a live core-hitting sentinel -- change 2's currency.

Replay-only, no bot-side print (platform replays strip stdout anyway, and a
local instrument that only exists in one arm cannot compare arms).

Per game:
  siege_r    rounds in which a sentinel of OURS that ever hit the enemy core is
             ALIVE and has already landed its first core hit
  ammo_med   median team ammo over those rounds        (autopsy baseline: 5)
  lt10       share of those rounds with ammo < 10      (baseline: 78.3%)
  ge10       share with ammo >= 10 (one sentinel shot) (baseline: 21.7%)
  ge120      share with ammo >= FS_AMMO_KILL_MIN
  idle_med   median ammo over rounds with NO such sentinel alive (baseline: 20)

GUARD: `--guard` mutates the ammo series to a constant 0 and to a constant 999
and asserts the shares move to 1.0 / 0.0 respectively; and asserts a game with
no core-hitting sentinel reports siege_r = 0 rather than a share of 0.0.
"""
from __future__ import annotations

import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, "/Users/junghard/Projects/Work/florent-code-game")
from tools.replay_census import (  # noqa: E402
    WIRE_LEN, fields, parse_entity, read_pos, scalars,
)


def load(path: Path, our_team: int):
    data = path.read_bytes()
    mb, turns = None, []
    for n, w, v in fields(data):
        if n == 1 and w == WIRE_LEN:
            mb = v
        elif n == 3 and w == WIRE_LEN:
            turns.append(v)
    cores = []
    for n, _w, v in fields(mb):
        if n == 4:
            c = {"team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(v):
                if cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    foot = {c["team"]: {(c["pos"][0] + dx, c["pos"][1] + dy)
                        for dx in (0, 1) for dy in (0, 1)} for c in cores}
    turrets, by_tile, ents = {}, {}, set()
    ammo = {0: 0, 1: 0}
    series = []            # per round: (ammo_ours, n_live_core_hitters)
    live_hitters = set()
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
                        if e.kind in ("sentinel", "gunner"):
                            by_tile[e.pos] = e.id
                            turrets[e.id] = dict(team=e.team, pos=e.pos,
                                                 core_shots=0)
                elif un == 3:
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            ents.discard(rv)
                            live_hitters.discard(rv)
                            t = turrets.get(rv)
                            if t is not None and by_tile.get(t["pos"]) == rv:
                                del by_tile[t["pos"]]
                elif un == 6:
                    for pn, _pw, pv in fields(ubuf):
                        if pn != 1:
                            continue
                        for tn, _tw, tv in fields(pv):
                            if tn in (1, 2):
                                ammo[tn - 1] = scalars(tv).get(7, 0)
                elif un == 12:
                    frm = to = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                        elif fn == 2:
                            to = read_pos(fv)
                    tid = by_tile.get(frm)
                    if tid is not None:
                        t = turrets[tid]
                        if to in foot.get(1 - t["team"], ()):
                            t["core_shots"] += 1
                            if t["team"] == our_team:
                                live_hitters.add(tid)
        series.append((ammo[our_team], len(live_hitters)))
    return series


def summarise(series):
    sieg = [a for a, n in series if n > 0]
    idle = [a for a, n in series if n == 0]
    d = dict(siege_r=len(sieg), idle_r=len(idle))
    d["ammo_med"] = st.median(sieg) if sieg else -1
    d["lt10"] = (sum(1 for a in sieg if a < 10) / len(sieg)) if sieg else -1
    d["ge10"] = (sum(1 for a in sieg if a >= 10) / len(sieg)) if sieg else -1
    d["ge120"] = (sum(1 for a in sieg if a >= 120) / len(sieg)) if sieg else -1
    d["idle_med"] = st.median(idle) if idle else -1
    return d


def guard():
    ok = True
    s = [(0, 1)] * 50
    if summarise(s)["lt10"] != 1.0:
        print("GUARD FAIL zero-ammo"); ok = False
    s = [(999, 1)] * 50
    if summarise(s)["lt10"] != 0.0 or summarise(s)["ge120"] != 1.0:
        print("GUARD FAIL high-ammo"); ok = False
    s = [(5, 0)] * 50
    r = summarise(s)
    if r["siege_r"] != 0 or r["lt10"] != -1:
        print("GUARD FAIL no-sentinel case reports a share"); ok = False
    s = [(5, 1)] * 30 + [(200, 0)] * 30
    r = summarise(s)
    if not (r["ammo_med"] == 5 and r["idle_med"] == 200):
        print("GUARD FAIL split"); ok = False
    print("GUARD:", "PASS" if ok else "FAIL")
    return ok


COLS = ["tag", "siege_r", "idle_r", "ammo_med", "lt10", "ge10", "ge120",
        "idle_med"]


def main():
    if "--guard" in sys.argv:
        sys.exit(0 if guard() else 1)
    if not guard():
        sys.exit(1)
    print("\t".join(COLS))
    for d in sys.argv[1:]:
        for p in sorted(Path(d).glob("*.replay26")):
            tag = p.stem
            our = 0 if tag.endswith("_A") else 1
            r = summarise(load(p, our))
            print("\t".join([tag] + [str(r[c]) for c in COLS[1:]]))


if __name__ == "__main__":
    main()
