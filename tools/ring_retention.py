#!/usr/bin/env python3
"""⛔⛔ RETIRED 2026-08-11. THIS DECODER IS WRONG AND IT REFUSES TO RUN.
USE `tools/ring_read.py`.

IT DOES NOT APPLY AN ENTITY-KIND FILTER. Every BUILDING of ours on an enemy-ring
tile counts as ring occupancy, permanently, until destroyed. Measured over 65
games, our entity-rounds on the enemy ring: barrier 48.8% / builder_bot 33.6% /
conveyor 17.5% / sentinel 0.2% -- **66.4% of what this file calls "a body on the
ring" is not a body.**

AND IT DOES NOT ADD AN OFFSET, IT FLIPS THE SIGN, because the control lays MORE
ring buildings than the treatment on all four 12-ring maps, so the contaminant
enters opposite to the signal. Decomposed on fjordgate: as-shipped -0.201 -> add
the kind filter -> +0.174. The kind filter alone accounts for +0.375 of a 0.383
gap. Measured again in HEAD on 60 archived games: 0.284 as shipped vs 0.139
filtered -- **103% high against a +0.15 bar.**

THE FORCED-ANSWER CELL THAT SETTLES IT: a BARRIER on the ring with zero
builder-rounds must read 0.000. This file reads 0.900. `ring_read.py` reads
0.000. Seven cells, floor and ceiling, both decoders imported unmodified.

⚠ AND ITS `--selftest` PASSED THE WHOLE TIME. It exercised 12-on-open /
5-in-corner / walls-reduce -- THE RING GEOMETRY -- and never the OCCUPANCY RULE,
which is the part that was wrong. A green selftest testing the geometry of a
metric while leaving its definition untested. That is why this file now refuses
at import rather than carrying a warning nobody reads: a wrong decoder sitting in
tools/ with a passing selftest is the single most likely way the 2026-08-11
adjudication gets silently undone.

A KNOCKDOWN ARGUMENT FROM INSIDE PREREG-loki16b ITSELF: that document lists
"enemy-ring tiles holding our building at game end, 2.64 vs 3.65" as the COST
SIDE. A quantity pre-registered as the COST cannot simultaneously be the PRIMARY.
This file's number was 97.9% that cost metric wearing the primary's name, sign
reversed.

Kept rather than deleted so its git history and this explanation stay reachable.
Set RING_RETENTION_I_KNOW_IT_IS_WRONG=1 to run it anyway (forensics only; any
number it emits is void).
"""
from __future__ import annotations

import os as _os
import sys as _sys

if not _os.environ.get("RING_RETENTION_I_KNOW_IT_IS_WRONG"):
    _sys.stderr.write(
        "\nring_retention.py: RETIRED AND WRONG -- refusing to run.\n"
        "  66.4% of what it counts as 'a body on the ring' is barriers/conveyors,\n"
        "  and it FLIPS THE SIGN (fjordgate -0.201 -> +0.174 with the kind filter).\n"
        "  Its --selftest passed throughout: it tested the RING, never the OCCUPANCY RULE.\n"
        "  USE tools/ring_read.py (blessed by the 2026-08-11 adjudication, 7 forced cells).\n\n")
    raise SystemExit(2)

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

US = "379a5d80-9921-4c9e-949b-f9b1dcba16be"
_OVERRIDE: dict = {}


def ring_of(core, w, h, rows):
    """The 4x4 box around the 2x2 footprint, minus the footprint. 12 when open."""
    cx, cy = core
    foot = {(cx + a, cy + b) for a in (0, 1) for b in (0, 1)}
    out = set()
    for (fx, fy) in foot:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                t = (fx + dx, fy + dy)
                if t in foot or not (0 <= t[0] < w and 0 <= t[1] < h):
                    continue
                if rows and rows[t[1]][t[0]] == 1:      # WALL
                    continue
                out.add(t)
    return out


def longest_hold(path: Path, our_team: int):
    """(longest unbroken ring-occupancy run, rounds, ring size) for one game."""
    data = path.read_bytes()
    mb, turns = None, []
    for num, wire, val in fields(data):
        if num == 1 and wire == WIRE_LEN and mb is None:
            mb = val
        elif num == 3 and wire == WIRE_LEN:
            turns.append(val)
    if mb is None:
        return None
    w = h = 0
    rows, cores = [], {}
    for num, wire, val in fields(mb):
        if num == 1:
            w = val
        elif num == 2:
            h = val
        elif num == 3 and wire == WIRE_LEN:
            for rn, _rw, rv in fields(val):
                if rn == 1:
                    rows.append(list(rv))
        elif num == 4 and wire == WIRE_LEN:
            t, p = 0, None
            for cn, _cw, cv in fields(val):
                if cn == 1:
                    t = cv
                elif cn == 3:
                    p = read_pos(cv)
            if p is not None:
                cores[t] = p
    if len(cores) < 2:
        return None
    ordered = [cores[k] for k in sorted(cores)]          # {1,2} local vs {0,1} platform
    ring = ring_of(ordered[1 - our_team], w, h, rows)

    pos: dict[int, tuple] = {}
    team: dict[int, int] = {}
    best = run = 0
    for tb in turns:
        for _n, _w2, ub in fields(tb):
            for un, _uw, uv in fields(ub):
                if un == 1:                                  # placeEntity
                    for en, _ew, ev in fields(uv):
                        if en != 1:
                            continue
                        e = parse_entity(ev, 0)
                        if e is None:
                            continue
                        pos[e.id] = tuple(e.pos)
                        team[e.id] = e.team
                elif un == 2:                                # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(uv):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid is not None and to is not None:
                        pos[eid] = tuple(to)
                elif un == 3:                                # removeEntity
                    for rn, _rw, rv in fields(uv):
                        if rn == 1:
                            pos.pop(rv, None)
                            team.pop(rv, None)
        on = any(p in ring for i, p in pos.items() if team.get(i) == our_team)
        run = run + 1 if on else 0
        best = max(best, run)
    return best, max(len(turns), 1), len(ring)


def selftest() -> int:
    print("RING RETENTION SELFTEST\n")
    bad = 0
    rows = [[0] * 12 for _ in range(12)]
    r = ring_of((5, 5), 12, 12, rows)
    ok = len(r) == 12
    print(f"  [{'ok' if ok else 'FAIL'}] open-terrain ring = {len(r)} (must be 12)")
    bad += not ok
    r0 = ring_of((0, 0), 12, 12, rows)
    ok = len(r0) == 5
    print(f"  [{'ok' if ok else 'FAIL'}] corner-clipped ring = {len(r0)} (must be 5, the jackpot shape)")
    bad += not ok
    # THE FIXTURE, NOT THE CODE, WAS WRONG FIRST TIME: a wall row at y=3 does
    # not touch the ring of a core at (5,5), whose box spans y=4..7. The test
    # failed and the geometry was correct -- the same "fixture rotted, check was
    # fine" family as the audit_trigger timestamps this morning. Wall y=4, which
    # is inside the ring.
    walled = [[0] * 12 for _ in range(12)]
    for x in range(12):
        walled[4][x] = 1
    rw = ring_of((5, 5), 12, 12, walled)
    ok = len(rw) < 12
    print(f"  [{'ok' if ok else 'FAIL'}] a wall row shrinks the ring to {len(rw)} (< 12)")
    bad += not ok
    print()
    if bad:
        print(f"*** {bad} wrong ***")
        return 1
    print("PASS: 12 on open terrain, 5 in a corner, and walls reduce it.")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if not argv:
        print(__doc__)
        return 2
    ids = re.findall(r'"matchId": "([0-9a-f-]+)"', Path(argv[0]).read_text())
    # PER-MATCH LOOKUP, NOT THE 200-MATCH LIST. Older legs age out of
    # `match list --mine --limit 200` -- LOKI-16's morning matches did, and the
    # tool reported "no games decoded" as though the data were missing when it
    # was only the INDEX that had moved on. Ask about each id directly.
    info = {}
    maps_by_match = {}
    for mid in ids:
        rr = subprocess.run([str(ROOT / ".venv/bin/fcode"), "match", "info", mid, "--json"],
                            capture_output=True, text=True)
        try:
            d = json.loads(rr.stdout[rr.stdout.find("{"):])
        except Exception:
            continue
        m = d.get("match") or {}
        if not m:
            continue
        info[mid] = (0 if m.get("teamAId") == US else 1,
                     m.get("teamBName") if m.get("teamAId") == US else m.get("teamAName"))
        maps_by_match[mid] = [g["mapName"] for g in d.get("games", [])]
    by_ring: dict[int, list] = {}
    by_map: dict[str, list] = {}
    n = 0
    for mid, (seat, _opp) in info.items():
        for f in sorted((ROOT / "replay_archive").glob(f"{mid}_game_*.replay26")):
            got = longest_hold(f, seat)
            if not got:
                continue
            best, rounds, ringsz = got
            by_ring.setdefault(ringsz, []).append(best / rounds)
            gi = int(f.name.split('_game_')[1].split('.')[0]) - 1
            mp = maps_by_match.get(mid, [])
            by_map.setdefault(mp[gi] if gi < len(mp) else '?', []).append(best / rounds)
            n += 1
    if not n:
        print("no games decoded")
        return 1
    print(f"longest-hold / game-length, game-mean, {n} games\n")
    for rs in sorted(by_ring, reverse=True):
        v = by_ring[rs]
        tag = "  <- 12-RING STRATUM (the bar lives here)" if rs >= 12 else "  (clipped: reported, NEVER pooled)"
        print(f"  ring {rs:>2}/12   n={len(v):>4}   mean {sum(v)/len(v):.3f}{tag}")
    if by_map:
        print("\n  per map:")
        for mp in sorted(by_map):
            v = by_map[mp]
            print(f"    {mp:<12} n={len(v):>4}  mean {sum(v)/len(v):.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
