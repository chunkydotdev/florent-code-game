#!/usr/bin/env python3
"""IDLE-AND-FREE, DECOMPOSED BY STATE — how much of bucket A can a MOVE actually reach?

WHY.  QUEUE #70's fallback is "if no verb is available, MOVE to a denial tile".
Its sizing rests on bucket A (idle AND free) running 3.31% -> 17.77% -> 29.01%.
**But bucket A is not one state, and a move cannot help all of it.** The builder
named three reproducible ones; this cuts the two that are decidable off the wire:

  NO-LEGAL-STEP   all four cardinal neighbours are off-map / WALL / occupied by a
                  building / occupied by any bot. **A move fallback provably
                  cannot help these rounds — it is a HARD CEILING on the plank.**
  FORWARD-PARKED  idle in the ENEMY half. Proxy for "raider on its ring station",
                  where #70's fallback is a deliberate NO-OP (it is already where
                  we want a body). Not a defect, but not addressable headroom.
  ADDRESSABLE     idle, has >=1 legal step, and is in OUR half. This is the only
                  population the plank can convert.

⛔ WHY "NO VERB" IS SUFFICIENT FOR "IDLE AND FREE", so no cooldown decode is
needed: `scratchpad/idle_split_s31.py` measured bucket D (ON COOLDOWN) at
**0.00% across all three windows and both arms**, over 894,638 builder-rounds —
every SetActionCooldown/SetMoveCooldown ever written for a builder is `1`, and
placement is `(0,0)` in 115,624 of 115,624. A cooldown of 1 decrements at end of
round, so a builder is free every round and "emitted no verb" ⟹ "idle AND free".

TILE ENCODING: 0=EMPTY 1=WALL 2=ORE, confirmed against `eco.py:69`'s own
`".#o"[cells[...]]` render. ORE is WALKABLE (we walk onto ore to build a
harvester); only WALL blocks.

⛔ WHAT THIS IS NOT.  The builder's state (b) — "adjacent to `link_queue[0]` with
a bank too poor for a conveyor" — is INTERNAL and not on the wire; it is not
separated here and falls inside ADDRESSABLE. So **ADDRESSABLE is an UPPER BOUND
on the plank's reach**, and the direction is declared.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "tools"))

import replay_census as RC  # noqa: E402
import nav_lock_census as NLC  # noqa: E402

CARD = ((0, -1), (0, 1), (1, 0), (-1, 0))
UPD_PLACE, UPD_MOVE, UPD_REMOVE = 1, 2, 3
UPD_ACTIONS = (13, 15, 16)


def analyse(path, our_team):
    data = Path(path).read_bytes()
    map_buf = None
    turn_bufs = []
    for n, w, v in RC.fields(data):
        if n == 1 and w == RC.WIRE_LEN:
            map_buf = v
        elif n == 3 and w == RC.WIRE_LEN:
            turn_bufs.append(v)
    if map_buf is None:
        return None

    width = height = 0
    tiles = []
    cores = []
    for n, w, v in RC.fields(map_buf):
        if n == 1:
            width = v
        elif n == 2:
            height = v
        elif n == 3:
            row = []
            for rn, rw, rv in RC.fields(v):
                if rn == 1:
                    row.extend(RC.packed_varints(rv) if rw == RC.WIRE_LEN else [rv])
            tiles.append(tuple(row))
        elif n == 4:
            pos = None
            team = 0
            for cn, _cw, cv in RC.fields(v):
                if cn == 2:
                    team = cv
                elif cn == 3:
                    pos = RC.read_pos(cv)
            cores.append((team, pos))
    walls = {(x, y) for y, row in enumerate(tiles)
             for x, t in enumerate(row) if t == 1}
    ours = next((p for t, p in cores if t == our_team and p), None)
    theirs = next((p for t, p in cores if t != our_team and p), None)
    if ours is None or theirs is None:
        return None

    # ⛔ BUILDINGS ARE REMOVED BY ID, SO THEY MUST BE KEYED BY ID. The first
    # version keyed them by POSITION and "removed" with a no-op dict rebuild, so
    # a destroyed building stayed occupied for the rest of the game — which
    # UNDER-counts legal steps and OVER-counts the no-step class, i.e. it
    # inflated exactly the headline ("a move cannot help these rounds").
    # Caught before publication; the first run read no-step 25.8%.
    buildings = {}      # id  -> pos
    bpos = {}           # pos -> refcount of live buildings on it
    bots = {}           # id -> pos
    bot_team = {}
    agg = defaultdict(int)
    for rnd, tb in enumerate(turn_bufs):
        acted = set()
        moved = set()
        for _n, _w, upd in RC.fields(tb):
            for unum, _uw, ub in RC.fields(upd):
                if unum == UPD_PLACE:
                    for en, _ew, eb in RC.fields(ub):
                        if en != 1:
                            continue
                        e = RC.parse_entity(eb, rnd)
                        if e is None or e.pos is None:
                            continue
                        if e.kind == "builder_bot":
                            bots[e.id] = e.pos
                            bot_team[e.id] = e.team
                        else:
                            buildings[e.id] = e.pos
                            bpos[e.pos] = bpos.get(e.pos, 0) + 1
                elif unum == UPD_MOVE:
                    eid = to = None
                    for mn, _mw, mv in RC.fields(ub):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = RC.read_pos(mv)
                    if to is not None and eid in bots:
                        bots[eid] = to
                        moved.add(eid)
                elif unum == UPD_REMOVE:
                    for rn, _rw, rv in RC.fields(ub):
                        if rn == 1:
                            bots.pop(rv, None)
                            gone = buildings.pop(rv, None)
                            if gone is not None and bpos.get(gone):
                                bpos[gone] -= 1
                                if bpos[gone] <= 0:
                                    bpos.pop(gone, None)
                elif unum in UPD_ACTIONS:
                    for an, _aw, av in RC.fields(ub):
                        if an == 1:
                            acted.add(av)
                            break
        occupied = set(bots.values())
        for eid, pos in bots.items():
            if bot_team.get(eid) != our_team:
                continue
            agg["rounds"] += 1
            if eid in acted or eid in moved:
                agg["active"] += 1
                continue
            agg["idle"] += 1
            x, y = pos
            legal = 0
            for dx, dy in CARD:
                n2 = (x + dx, y + dy)
                if not (0 <= n2[0] < width and 0 <= n2[1] < height):
                    continue
                if n2 in walls or n2 in bpos or n2 in occupied:
                    continue
                legal += 1
            d_ours = (x - ours[0]) ** 2 + (y - ours[1]) ** 2
            d_theirs = (x - theirs[0]) ** 2 + (y - theirs[1]) ** 2
            if legal == 0:
                agg["idle_nostep"] += 1
            elif d_theirs < d_ours:
                agg["idle_forward"] += 1
            else:
                agg["idle_addressable"] += 1
    return agg


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ourver", action="append", required=True)
    ap.add_argument("--limit", type=int, default=120)
    args = ap.parse_args()

    tot = defaultdict(int)
    print("%-6s %6s %11s %8s   %11s %11s %13s" % (
        "ver", "games", "b-rounds", "idle%", "no-step", "fwd-parked", "ADDRESSABLE"))
    for v in args.ourver:
        a = defaultdict(int)
        for p, team, _c, _vv in NLC.population(ourver=v, meta=str(NLC.DEFAULT_META),
                                               archive=str(NLC.DEFAULT_ARCHIVE),
                                               limit=args.limit):
            r = analyse(p, team)
            if r is None:
                continue
            a["games"] += 1
            for k, x in r.items():
                a[k] += x
        for k, x in a.items():
            tot[k] += x
        i = a["idle"] or 1
        print("v%-5s %6d %11d %7.2f%%   %11s %11s %13s" % (
            v, a["games"], a["rounds"], 100 * a["idle"] / max(a["rounds"], 1),
            "%d (%.1f%%)" % (a["idle_nostep"], 100 * a["idle_nostep"] / i),
            "%d (%.1f%%)" % (a["idle_forward"], 100 * a["idle_forward"] / i),
            "%d (%.1f%%)" % (a["idle_addressable"], 100 * a["idle_addressable"] / i)))
    i = tot["idle"] or 1
    print("-" * 76)
    print("%-6s %6d %11d %7.2f%%   %11s %11s %13s" % (
        "TOTAL", tot["games"], tot["rounds"], 100 * tot["idle"] / max(tot["rounds"], 1),
        "%d (%.1f%%)" % (tot["idle_nostep"], 100 * tot["idle_nostep"] / i),
        "%d (%.1f%%)" % (tot["idle_forward"], 100 * tot["idle_forward"] / i),
        "%d (%.1f%%)" % (tot["idle_addressable"], 100 * tot["idle_addressable"] / i)))
    print("\nidle-and-free builder-rounds: %d of %d = %.2f%% of all our builder-rounds"
          % (tot["idle"], tot["rounds"], 100 * tot["idle"] / max(tot["rounds"], 1)))
    print("⛔ HARD CEILING — a MOVE cannot help the no-step rounds: %.1f%% of bucket A"
          % (100 * tot["idle_nostep"] / i))
    print("   plank's UPPER-BOUND reach (addressable, own half, >=1 legal step): %.1f%% of bucket A"
          " = %.2f%% of all builder-rounds"
          % (100 * tot["idle_addressable"] / i,
             100 * tot["idle_addressable"] / max(tot["rounds"], 1)))


if __name__ == "__main__":
    main()
