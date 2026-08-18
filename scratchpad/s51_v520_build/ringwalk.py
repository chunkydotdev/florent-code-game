#!/usr/bin/env python3
"""s51 v520 -- SHARED per-round state walk for seatrate / termcov / nobody.

⛔ COPIED, NOT REWRITTEN.  `dsq_core()`, `geom()`, `walk()` and the occupancy
fold are `scratchpad/s51_closure_autopsy/ferry.py` (lines 53-58, 61-73, 76-127,
147-179) and `scratchpad/s51_closure_autopsy/seattape.py` (`ring_tiles`,
BLOCKING/BUILDINGS, the D/d/o/E/b/. alphabet).  The wire primitives are
`tools/replay_census.py`.  Nothing here re-derives a seat, a distance or a
turn-stream field number that those files already fixed.

⭐ ONE CORRECTION, AND IT IS A REAL BUG IN THE ORIGINALS.  Both `seattape.py`
(line 80) and `ferry.py` (line 87) seed the two Cores from map-message field
**5**.  `tools/replay_schema.md:40` says `repeated CorePosition cores = 4`, and
every real replay agrees -- measured on `smoke/atoll_i.replay26`, the map
message carries fields {1:width, 2:height, 3:TileRow x18, 4:CorePosition x2}
and **field 5 does not exist**.  So in the originals the core seeding loop
NEVER FIRED and neither Core was ever in `occ`.  Harmless for the 8 orthogonal
heal seats (they are disjoint from the 2x2 footprint) which is why it survived,
but it made the `D`-by-our-Core branch unreachable.  Corrected here to field 4
and GUARDED: `walk()` refuses a replay that does not seed exactly 2 cores, and
`--selftest` drives that guard the other way by renumbering the field back to 5
on a real replay and requiring the failure.

DISTANCE CONVENTIONS -- two live in this repo and mixing them silently is how a
presence share moves without anything happening:
  * `dsq_core(p, o)`  footprint-aware, min over the 4 Core tiles, INTEGER.
    This is the bot's own `eco.dsq_core` (verified equivalent) and the closure
    autopsy's `FS_RING_DSQ = 8` envelope.  Used for launcher siting.
  * `dsq_centre(p, o)` distance to the 2x2 CENTRE (o+0.5, o+0.5), FLOAT.
    This is `reel/tape.py`'s `near_bot`/`near_sent` convention and therefore
    `phase.marks` and `gapdecomp`'s window.  Used for every presence radius so
    those numbers stay comparable.
Each emitted column says which one it used.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
from tools.replay_census import (  # noqa: E402
    WIRE_LEN, fields, packed_varints, parse_entity, read_pos,
)
from map_encode import parse_map26  # noqa: E402

# -- seattape.py alphabet, verbatim -------------------------------------------
BLOCKING = {"barrier", "harvester", "gunner", "sentinel", "launcher", "core"}
BUILDINGS = BLOCKING | {"conveyor", "splitter"}

FS_RING_DSQ = 8          # closure autopsy / siege.py:2401
PICKUP_DSQ = 2           # launcher pickup envelope (engine)
THROW_DSQ_MAX = 26       # launcher throw envelope (engine)

MAPS = ("atoll", "midgard", "drakkarfjord", "glacierkeep", "nordkap",
        "yulerune")


class GuardFail(Exception):
    pass


# -- ferry.py:53-58, verbatim -------------------------------------------------
def dsq_core(p, o):
    dx = abs(p[0] - o[0])
    dx = dx - 1 if dx > 1 else (0 if p[0] in (o[0], o[0] + 1) else dx)
    dy = abs(p[1] - o[1])
    dy = dy - 1 if dy > 1 else (0 if p[1] in (o[1], o[1] + 1) else dy)
    return dx * dx + dy * dy


def dsq(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def dsq_centre(p, o):
    """reel/tape.py's convention: distance to the 2x2 core CENTRE."""
    return (p[0] - (o[0] + 0.5)) ** 2 + (p[1] - (o[1] + 0.5)) ** 2


# -- seattape.ring_tiles, verbatim --------------------------------------------
def ring_tiles(ox, oy, mw, mh):
    seats = [(ox, oy - 1), (ox + 1, oy - 1), (ox + 2, oy), (ox + 2, oy + 1),
             (ox + 1, oy + 2), (ox, oy + 2), (ox - 1, oy + 1), (ox - 1, oy)]
    corners = [(ox - 1, oy - 1), (ox + 2, oy - 1), (ox - 1, oy + 2),
               (ox + 2, oy + 2)]
    inb = lambda t: 0 <= t[0] < mw and 0 <= t[1] < mh  # noqa: E731
    return [t for t in seats if inb(t)], [t for t in corners if inb(t)]


# -- ferry.geom, verbatim (map26 path) ----------------------------------------
def geom(mapname, seat):
    w, h, rows, cores = parse_map26(ROOT / "maps" / f"{mapname}.map26")
    an = {c[0]: (c[1], c[2]) for c in cores}
    ours = 0 if seat == "A" else 1
    ox, oy = an[1 - ours]
    seats, corners = ring_tiles(ox, oy, w, h)
    ok = lambda t: rows[t[1]][t[0]] != 1  # noqa: E731
    return (w, h, rows, ours, (ox, oy),
            [t for t in seats if ok(t)], [t for t in corners if ok(t)])


# -- the replay's OWN map message (the cross-check for geom) -------------------
def replay_map(path, _core_field=4):
    data = Path(path).read_bytes()
    mb = None
    for n, w, v in fields(data):
        if n == 1 and w == WIRE_LEN:
            mb = v
            break
    if mb is None:
        raise GuardFail(f"{path}: no map message (top field 1)")
    w = h = 0
    rows, cores = [], []
    for n, wt, v in fields(mb):
        if n == 1:
            w = v
        elif n == 2:
            h = v
        elif n == 3:
            row = []
            for rn, rw, rv in fields(v):
                if rn == 1:
                    row.extend(packed_varints(rv) if rw == WIRE_LEN else [rv])
            rows.append(row)
        elif n == _core_field and wt == WIRE_LEN:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(v):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    return w, h, rows, cores


def check_geom(path, mapname, seat):
    """GUARD: the map26 geometry and the replay's own map message must agree.

    Driven the other way in --selftest by passing the WRONG map name.
    """
    w, h, rows, ours, E, seats, corners = geom(mapname, seat)
    rw, rh, rrows, rcores = replay_map(path)
    if len(rcores) != 2:
        raise GuardFail(f"{path}: replay seeded {len(rcores)} cores, expected 2 "
                        f"(the field-5 bug -- see module docstring)")
    if (rw, rh) != (w, h):
        raise GuardFail(f"{path}: map26 {mapname} is {w}x{h}, replay is "
                        f"{rw}x{rh}")
    anchors = {c["team"]: c["pos"] for c in rcores}
    if anchors[1 - ours] != E:
        raise GuardFail(f"{path}: map26 {mapname} puts the enemy core at {E}, "
                        f"the replay says {anchors[1 - ours]}")
    walls_26 = sum(1 for y in range(h) for x in range(w) if rows[y][x] == 1)
    walls_rp = sum(1 for y in range(rh) for x in range(rw) if rrows[y][x] == 1)
    if walls_26 != walls_rp:
        raise GuardFail(f"{path}: wall count {walls_26} (map26) vs {walls_rp} "
                        f"(replay)")
    return w, h, rows, ours, E, seats, corners


# -- ferry.walk, verbatim except the core-seed field ---------------------------
def walk(replay, core_field=4):
    """yield (round, {eid: (kind, team, pos, birth_round)}) at END OF ROUND."""
    data = Path(replay).read_bytes()
    mb, turns = None, []
    for n, wt, v in fields(data):
        if n == 1 and wt == WIRE_LEN:
            mb = v
        elif n == 3 and wt == WIRE_LEN:
            turns.append(v)
    ents = {}
    seeded = 0
    if mb is not None:
        for mn, mw, mv in fields(mb):
            if mn == core_field and mw == WIRE_LEN:
                cid = team = 0
                pos = None
                for cn, cw, cv in fields(mv):
                    if cn == 1:
                        cid = cv
                    elif cn == 2:
                        team = cv
                    elif cn == 3 and cw == WIRE_LEN:
                        pos = read_pos(cv)
                if pos is not None:
                    ents[cid] = ["core", team, pos, 0]
                    seeded += 1
    if seeded != 2:
        raise GuardFail(f"{replay}: seeded {seeded} cores from map field "
                        f"{core_field}, expected 2")
    for rnd, tb in enumerate(turns):
        for _n, _w, u0 in fields(tb):
            for un, _uw, ub in fields(u0):
                if un == 1:                                  # placeEntity
                    for en, _ew, eb in fields(ub):
                        if en != 1:
                            continue
                        e = parse_entity(eb, rnd)
                        if e is None:
                            continue
                        if e.id in ents:
                            ents[e.id][2] = e.pos
                            ents[e.id][0] = e.kind
                        else:
                            ents[e.id] = [e.kind, e.team, e.pos, rnd]
                elif un == 2:                                # moveBuilderBot
                    eid = to = None
                    for mn, _mw, mv in fields(ub):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in ents and to is not None:
                        ents[eid][2] = to
                elif un == 3:                                # removeEntity
                    for rn, _rw, rv in fields(ub):
                        if rn == 1:
                            ents.pop(rv, None)
        yield rnd, {k: tuple(v) for k, v in ents.items()}


# -- ferry.py:147-165 occupancy fold, verbatim --------------------------------
def occupancy(ents):
    """tile -> (kind, team).  A BUILDING outranks a body on the same tile."""
    occ = {}
    for _eid, (k, t, p, _b) in ents.items():
        if k == "core":
            for dx in (0, 1):
                for dy in (0, 1):
                    occ[(p[0] + dx, p[1] + dy)] = (k, t)
        else:
            prev = occ.get(p)
            if prev is None or (k in BUILDINGS and prev[0] not in BUILDINGS):
                occ[p] = (k, t)
    return occ


def denied_by(occ, seats, ourteam):
    """seattape's D|d: OUR blocking building, or OUR builder body, on a seat."""
    out = set()
    for s in seats:
        o = occ.get(s)
        if o is None:
            continue
        if o[1] == ourteam and (o[0] in BLOCKING or o[0] == "builder_bot"):
            out.add(s)
    return out


# =============================== SELFTEST ====================================

def _fixture_replay():
    for c in (HERE / "smoke", HERE / "grid"):
        if c.exists():
            g = sorted(c.rglob("*.replay26"))
            if g:
                return g[0]
    raise SystemExit("no .replay26 fixture found under %s" % HERE)


def selftest():
    ok = True

    def chk(name, cond, detail=""):
        nonlocal ok
        print("  [%s] %s%s" % ("PASS" if cond else "FAIL", name,
                               ("  " + detail) if detail else ""))
        if not cond:
            ok = False

    print("=== ringwalk selftest ===")

    # 1. dsq_core, both ways, against the bot's own definition -----------------
    o = (5, 5)
    chk("dsq_core on a core tile is 0", dsq_core((5, 5), o) == 0
        and dsq_core((6, 6), o) == 0)
    chk("dsq_core on an orthogonal seat is 1", dsq_core((5, 4), o) == 1
        and dsq_core((7, 5), o) == 1)
    chk("dsq_core on a corner is 2", dsq_core((4, 4), o) == 2)
    chk("dsq_core OTHER WAY: a far tile is NOT <= FS_RING_DSQ",
        dsq_core((0, 0), o) > FS_RING_DSQ, "dsq_core((0,0))=%d" % dsq_core((0, 0), o))

    # 2. ring_tiles, both ways -------------------------------------------------
    s, c = ring_tiles(5, 5, 20, 20)
    chk("8 seats + 4 corners in open field", (len(s), len(c)) == (8, 4))
    s2, c2 = ring_tiles(0, 0, 20, 20)
    chk("OTHER WAY: a corner-anchored core loses seats to the border",
        (len(s2), len(c2)) == (4, 1), "got %d seats %d corners" % (len(s2), len(c2)))

    # 3. occupancy precedence, both ways --------------------------------------
    ents = {1: ("builder_bot", 0, (3, 3), 0), 2: ("barrier", 1, (3, 3), 0)}
    chk("a BUILDING outranks a body on the same tile",
        occupancy(ents)[(3, 3)] == ("barrier", 1))
    ents_rev = {1: ("barrier", 1, (3, 3), 0), 2: ("builder_bot", 0, (3, 3), 0)}
    chk("...in either insertion order",
        occupancy(ents_rev)[(3, 3)] == ("barrier", 1))
    chk("OTHER WAY: a body-only tile reads as the body",
        occupancy({1: ("builder_bot", 0, (3, 3), 0)})[(3, 3)]
        == ("builder_bot", 0))
    chk("a core expands to its 4 footprint tiles",
        all(occupancy({9: ("core", 1, (7, 7), 0)}).get(t) == ("core", 1)
            for t in ((7, 7), (8, 7), (7, 8), (8, 8))))

    # 4. denied_by, both ways --------------------------------------------------
    seats = [(5, 4), (6, 4), (7, 5)]
    occ_us = {(5, 4): ("barrier", 0), (6, 4): ("builder_bot", 0),
              (7, 5): ("conveyor", 0)}
    d = denied_by(occ_us, seats, 0)
    chk("our barrier + our body DENY; our conveyor does NOT (seattape 'o')",
        d == {(5, 4), (6, 4)}, str(sorted(d)))
    chk("OTHER WAY: the same occupancy read as team 1 denies NOTHING",
        denied_by(occ_us, seats, 1) == set())
    occ_them = {(5, 4): ("barrier", 1), (6, 4): ("builder_bot", 1)}
    chk("OTHER WAY: enemy bodies/buildings on the seats deny nothing for us",
        denied_by(occ_them, seats, 0) == set())

    # 5. THE CORE-SEED GUARD, driven both ways on a real replay ---------------
    rp = _fixture_replay()
    try:
        rnd, ents = next(walk(rp))
        cores = [e for e in ents.values() if e[0] == "core"]
        chk("real replay seeds 2 cores from field 4", len(cores) == 2,
            "%s -> %s" % (rp.name, sorted((e[1], e[2]) for e in cores)))
    except GuardFail as e:
        chk("real replay seeds 2 cores from field 4", False, str(e))
    try:
        next(walk(rp, core_field=5))
        chk("OTHER WAY: the ORIGINAL field-5 seed must FAIL the guard", False,
            "field 5 seeded cores -- the bug story is wrong")
    except GuardFail as e:
        chk("OTHER WAY: the ORIGINAL field-5 seed FAILS the guard", True,
            str(e).split(": ", 1)[-1])

    # 6. geom cross-check, driven both ways ------------------------------------
    tag = rp.stem
    mapname = next((m for m in MAPS if tag.startswith(m)), None)
    if mapname is None:
        print("  [skip] geom cross-check: %s has no map name in its tag" % tag)
    else:
        seat = tag.rsplit("_", 1)[-1] if tag.rsplit("_", 1)[-1] in ("A", "B") else "A"
        try:
            w, h, _r, ours, E, seats, corners = check_geom(rp, mapname, seat)
            chk("geom(map26) agrees with the replay's own map message", True,
                "%s %dx%d enemy core %s seats=%d" % (mapname, w, h, E, len(seats)))
        except GuardFail as e:
            chk("geom(map26) agrees with the replay's own map message", False,
                str(e))
        wrong = next(m for m in MAPS if m != mapname
                     and (ROOT / "maps" / (m + ".map26")).exists())
        try:
            check_geom(rp, wrong, seat)
            chk("OTHER WAY: the WRONG map name must be refused", False,
                "check_geom(%s) accepted a %s replay" % (wrong, mapname))
        except GuardFail as e:
            chk("OTHER WAY: the WRONG map name is refused", True,
                str(e).split(": ", 1)[-1][:90])

    print("=== ringwalk selftest %s ===" % ("PASS" if ok else "FAIL"))
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        raise SystemExit(0 if selftest() else 1)
    print(__doc__)
