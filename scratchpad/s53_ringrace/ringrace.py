#!/usr/bin/env python3
"""s53 RING RACE decode: does our raid arrive before the enemy seals its Core ring?

Adapted from the two validated s52 instruments and deliberately NOT a new
decoder: `scratchpad/s52_diffstudy/ringtime.py` (ring sockets = the tiles
orthogonally adjacent to a 2x2 Core footprint, walls excluded) and
`scratchpad/s52_launchtime/launchtime.py` (launcher/throw/arrival clock, the
`arr2` arrival definition = first round an own builder bot sits at d^2 <= 2 of
the enemy Core footprint).  The raid clock itself is read by RUNNING
launchtime.py unmodified; this file adds the three channels it does not carry:

  * RING OCCUPANCY per round, per team, over the ring sockets  (from ringtime)
  * RING GEOMETRY: histogram of a team's buildings by min d^2 to own Core
    footprint, so a perimeter built farther out is visible instead of assumed
  * DAMAGE, per round, from update field 5 `UpdateHp {id=1, delta=2}` with the
    two's-complement fold (`replay_census.parse_update_hp`), which is how
    "first damage to the enemy Core" and "first damage to a ring building" are
    measured rather than inferred from HP-at-build.

DEFINITIONS (every number in the report carries one of these):
  ring_socket   in-bounds, NON-WALL tile orthogonally adjacent to a Core
                footprint tile.  Denominator is per map and is printed.
  occ(r)        ring sockets holding a building (any non-builder-bot entity) of
                the OWNING team, at end of round r.
  ring_close_r  first r with occ(r) == denominator.  -1 = never.
  ring_half_r   first r with occ(r) >= ceil(denominator/2).
  ring_max      max occ over the game.
  arr_r         (from launchtime) first round an own builder bot is at
                d^2 <= 2 of the ENEMY Core footprint.
  dmg_core_r    first round with a NEGATIVE UpdateHp on the enemy Core id.
  dmg_ring_r    first round with a NEGATIVE UpdateHp on an enemy building whose
                position is a ring socket of the enemy Core.
Rounds are the 0-indexed engine rounds (turns[i] IS round i).

Usage: ringrace.py <replay> [...]        TSV to stdout
       ringrace.py --report <replay>     per-round narrative to stdout
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import (  # noqa: E402
    Replay, fields, parse_entity, parse_update_hp, read_pos, ENV_WALL,
    ENV_ORE_TITANIUM, CARDINALS)

BUILDING_KINDS = {"core", "harvester", "conveyor", "splitter", "barrier",
                  "sentinel", "gunner", "launcher"}


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def mind2(p, tiles):
    return min(d2(p, t) for t in tiles)


def ring_tiles(r, team):
    foot = set(r.core_footprint(team))
    out = []
    for (x, y) in foot:
        for dx, dy in CARDINALS:
            n = (x + dx, y + dy)
            if n in foot or n in out:
                continue
            if 0 <= n[0] < r.width and 0 <= n[1] < r.height:
                out.append(n)
    return out


def walk(path: Path):
    """One pass over the turn stream; returns everything both channels need."""
    r = Replay(path, track_flow=False)
    foot = {t: sorted(r.core_footprint(t)) for t in (0, 1)}
    core_id = {c["team"]: c["id"] for c in r.cores}
    rings, walls, ore = {}, {}, {}
    for t in (0, 1):
        tiles = ring_tiles(r, t)
        walls[t] = {p for p in tiles if r.tiles[p[1]][p[0]] == ENV_WALL}
        ore[t] = {p for p in tiles if r.tiles[p[1]][p[0]] == ENV_ORE_TITANIUM}
        rings[t] = [p for p in tiles if p not in walls[t]]

    raw = path.read_bytes()
    turn_bufs = [buf for num, _w, buf in fields(raw) if num == 3]

    ents = {}                       # live: id -> [team, kind, pos]
    ever = {}                       # never popped: id -> (team, kind)
    for c in r.cores:
        ents[c["id"]] = [c["team"], "core", c["pos"]]
        ever[c["id"]] = (c["team"], "core")

    occ_hist = {0: [], 1: []}       # per round: sockets held by owner
    plug_hist = {0: [], 1: []}      # per round: sockets held by the ENEMY
    dmg = []                        # (rnd, victim_id, delta, team, kind, pos)
    place = []                      # (rnd, id, team, kind, pos)
    remove = []                     # (rnd, id, team, kind, pos_at_death)
    bots_near = {0: [], 1: []}      # per round: [(id, mind2_to_enemy_core)]
    nrounds = 0

    for rnd, tb in enumerate(turn_bufs):
        nrounds = rnd + 1
        for _n, _w, ub in fields(tb):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                  # placeEntity
                    for en, _ew, eb in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None:
                            continue
                        ents[e.id] = [e.team, e.kind, e.pos]
                        ever[e.id] = (e.team, e.kind)
                        place.append((rnd, e.id, e.team, e.kind, e.pos))
                elif unum == 2:                                # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in ents and to is not None:
                        ents[eid][2] = to
                elif unum == 3:                                # removeEntity
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            rec = ents.pop(rv, None)
                            if rec is not None:
                                remove.append((rnd, rv, rec[0], rec[1], rec[2]))
                elif unum == 5:                                # updateHp
                    eid, delta = parse_update_hp(ubuf, f" {path.name} r{rnd}")
                    team, kind = ever.get(eid, (None, "?"))
                    pos = ents[eid][2] if eid in ents else None
                    dmg.append((rnd, eid, delta, team, kind, pos))

        occ = {}
        for (t, k, p) in ents.values():
            if k in BUILDING_KINDS:
                occ[p] = (t, k)
        for team in (0, 1):
            own = sum(1 for p in rings[team]
                      if occ.get(p) and occ[p][0] == team)
            plug = sum(1 for p in rings[team]
                       if occ.get(p) and occ[p][0] != team)
            occ_hist[team].append(own)
            plug_hist[team].append(plug)
            near = [(eid, mind2(rec[2], foot[1 - team]))
                    for eid, rec in ents.items()
                    if rec[0] == team and rec[1] == "builder_bot"]
            bots_near[team].append(sorted(near, key=lambda z: z[1]))

    return dict(replay=r, path=path, rounds=nrounds, foot=foot,
                core_id=core_id, rings=rings, walls=walls, ore=ore,
                occ=occ_hist, plug=plug_hist, dmg=dmg, place=place,
                remove=remove, bots_near=bots_near, ever=ever)


def first_ge(seq, thresh):
    for i, v in enumerate(seq):
        if v >= thresh:
            return i
    return -1


def geometry(w, team, at_round=None):
    """Histogram of that team's buildings by min d^2 to own Core footprint,
    as of `at_round` (None = end of game).  Uses the place/remove streams."""
    live = {}
    for (rnd, eid, t, k, p) in w["place"]:
        if at_round is not None and rnd > at_round:
            continue
        if t == team and k in BUILDING_KINDS and k != "core":
            live[eid] = p
    for (rnd, eid, t, k, p) in w["remove"]:
        if at_round is not None and rnd > at_round:
            continue
        live.pop(eid, None)
    hist = {}
    for p in live.values():
        hist[mind2(p, w["foot"][team])] = hist.get(mind2(p, w["foot"][team]), 0) + 1
    return hist


def row(path: Path):
    w = walk(path)
    r = w["replay"]
    out = {"file": path.name, "rounds": w["rounds"], "winner": r.winner,
           "cond": r.win_condition, "w": r.width, "h": r.height}
    for team in (0, 1):
        tag = "a" if team == 0 else "b"
        den = len(w["rings"][team])
        occ = w["occ"][team]
        out[f"{tag}_ring_den"] = den
        out[f"{tag}_ring_walls"] = len(w["walls"][team])
        out[f"{tag}_ring_ore"] = len(w["ore"][team])
        out[f"{tag}_ring_close_r"] = first_ge(occ, den) if den else -1
        out[f"{tag}_ring_half_r"] = first_ge(occ, math.ceil(den / 2)) if den else -1
        out[f"{tag}_ring_1st_r"] = first_ge(occ, 1)
        out[f"{tag}_ring_max"] = max(occ) if occ else 0
        out[f"{tag}_plugmax"] = max(w["plug"][team]) if w["plug"][team] else 0
        # damage clocks against THIS team's core / ring, i.e. the ENEMY's raid
        cid = w["core_id"][team]
        ring = set(w["rings"][team])
        dcore = [d[0] for d in w["dmg"] if d[1] == cid and d[2] < 0]
        dring = [d[0] for d in w["dmg"]
                 if d[2] < 0 and d[3] == team and d[4] in BUILDING_KINDS
                 and d[4] != "core" and d[5] in ring]
        out[f"{tag}_dmg_core_r"] = dcore[0] if dcore else -1
        out[f"{tag}_dmg_ring_r"] = dring[0] if dring else -1
        out[f"{tag}_dmg_core_n"] = len(dcore)
        out[f"{tag}_dmg_core_total"] = sum(-d[2] for d in w["dmg"]
                                           if d[1] == cid and d[2] < 0)
    return out


def report(path: Path):
    w = walk(path)
    r = w["replay"]
    print(f"=== {path.name}  {r.width}x{r.height}  rounds={w['rounds']}  "
          f"winner={r.winner} cond={r.win_condition}")
    for team in (0, 1):
        tag = "A(us)" if team == 0 else "B(Erebus)"
        print(f"  {tag} core at {sorted(w['foot'][team])[0]}  "
              f"ring sockets={len(w['rings'][team])} "
              f"(walls excluded={len(w['walls'][team])}, ore={len(w['ore'][team])})")
    d = row(path)
    for k, v in d.items():
        print(f"    {k}\t{v}")
    print("  -- B ring occupancy by round (first 60) --")
    print("   ", " ".join(str(v) for v in w["occ"][1][:60]))
    print("  -- B building geometry (min d^2 to own core -> count) --")
    for at in (20, 40, 80, w["rounds"] - 1):
        if at < 0 or at >= w["rounds"]:
            continue
        h = geometry(w, 1, at)
        print(f"    r{at}: " + " ".join(f"d2={k}:{v}" for k, v in sorted(h.items())))
    print("  -- our builders' distance to enemy core, by round --")
    for rnd in range(0, w["rounds"], max(1, w["rounds"] // 25)):
        near = w["bots_near"][0][rnd]
        print(f"    r{rnd}: n={len(near)} " +
              " ".join(f"#{i}@d2={m}" for i, m in near[:6]))


def main(argv):
    if argv and argv[0] == "--report":
        for a in argv[1:]:
            report(Path(a))
        return
    hdr = None
    for a in argv:
        try:
            d = row(Path(a))
        except Exception as exc:                     # noqa: BLE001
            print(f"ERR\t{a}\t{exc}", file=sys.stderr)
            continue
        if hdr is None:
            hdr = list(d)
            print("\t".join(hdr))
        print("\t".join(str(d[k]) for k in hdr))


if __name__ == "__main__":
    main(sys.argv[1:])


# ---------------------------------------------------------------------------
# SOCKET RACE (added after the first pass showed NEITHER team ever closes an
# 8/8 core-adjacent ring, so "ring closure" alone cannot decide the race).
# Per socket of a team's Core, who put a building there FIRST and when.
# ---------------------------------------------------------------------------

def socket_race(path: Path, team: int = 1):
    w = walk(path)
    ring = w["rings"][team]
    first = {}                       # tile -> (rnd, owner_team, kind, eid)
    hist = {}                        # tile -> [(rnd, evt, team, kind)]
    live = {}
    for (rnd, eid, t, k, p) in sorted(
            w["place"] + [(x[0], x[1], x[2], x[3], x[4]) for x in []]):
        if k not in BUILDING_KINDS or p not in ring:
            continue
        hist.setdefault(p, []).append((rnd, "place", t, k))
        if p not in first:
            first[p] = (rnd, t, k, eid)
        live[eid] = p
    for (rnd, eid, t, k, p) in w["remove"]:
        if k in BUILDING_KINDS and p in ring:
            hist.setdefault(p, []).append((rnd, "remove", t, k))
    return w, ring, first, hist


def socket_report(path: Path, team: int = 1):
    w, ring, first, hist = socket_race(path, team)
    who = {0: "US(A)", 1: "EREBUS(B)"}
    print(f"--- {path.name}: sockets of team {who[team]} core "
          f"{sorted(w['foot'][team])[0]} ---")
    us_first = them_first = never = 0
    for p in sorted(ring):
        f = first.get(p)
        if f is None:
            never += 1
            print(f"  {p}  NEVER BUILT ON")
            continue
        rnd, t, k, _ = f
        if t == team:
            them_first += 1
        else:
            us_first += 1
        ev = " ".join(f"r{r}:{e}:{who[tt][0]}:{kk}"
                      for r, e, tt, kk in sorted(hist.get(p, []))[:6])
        print(f"  {p}  FIRST r{rnd} by {who[t]} ({k})   | {ev}")
    print(f"  => owner-first {them_first}/{len(ring)} · "
          f"enemy-first {us_first}/{len(ring)} · never {never}/{len(ring)}")
