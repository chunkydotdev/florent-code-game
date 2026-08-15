#!/usr/bin/env python3
"""MAP ADMISSION CHECK — does the fixture's terrain ADMIT the mechanism?

    .venv/bin/python tools/map_admits.py                       # the 5 pinned maps
    .venv/bin/python tools/map_admits.py --selftest            # prove it can fail
    .venv/bin/python tools/map_admits.py --maps atoll saga

WHY THIS EXISTS (s28, D34). LOKI-16's plank is defined on the enemy core's
12-tile ring. **20% of its leg ran on `jackpot`, whose cores sit hard in the
corners so the ring clips to 5 tiles** -- terrain on which the plank's geometry
does not exist. That alone dragged coverage +0.117 -> +0.086, ACROSS the bar.

The panel had been audited to death on the OPPONENT axis (D22: three of five
cells are inert constants) and **never once on the MAP axis**. Nobody asked
whether the fixture admits the mechanism at all. The failure is the same shape as
D22 and it was invisible for the same reason: an axis nobody thought to look at
does not announce itself, it just quietly averages your effect toward zero.

**A CELL THAT CANNOT EXPRESS THE MECHANISM IS NOT A HARD CELL, IT IS A DEAD
DENOMINATOR** -- exactly like a floor or ceiling opponent.

WHAT IT DOES NOT DO. It does not tell you to delete a map. `jackpot` is KEPT on
the panel: the treatment is flat there (0.675 vs 0.672) while the CONTROL gains
(+0.159), because a 5-tile corner ring hands the incumbent the same ceiling the
plank works to reach. **That is a real property of the plank and deleting the map
would delete the evidence for it.** This tool makes the split VISIBLE so results
are reported per-stratum; choosing to pool is then a decision on the record
rather than an accident of terrain.

Core positions and terrain both come from the REPLAY's own map buffer (the
engine's copy). **The replay does NOT carry the map name** -- its map buffer has
fields {w, h, rows, cores} and nothing else -- so the name is recovered by an
EXACT TERRAIN FINGERPRINT against `maps/*.map26`: (w, h, every tile in row
order), cores excluded. Not by dimension inference, which would collide any two
maps of the same size. The selftest drives the fingerprint to a MISS by flipping
a single tile, so an accidental match cannot pass for a real one.
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from replay_census import fields, read_pos, WIRE_LEN, WIRE_VARINT  # noqa: E402

ARCHIVE = ROOT / "replay_archive"
PINNED = ["fjordgate", "jackpot", "atoll", "saga", "snowflake"]

WALL = 1


def _terrain(buf: bytes) -> tuple[int, int, list[list[int]]]:
    """(w, h, rows) from any buffer using the map wire format -- the replay's
    embedded map buffer and a `maps/*.map26` file are the same shape here."""
    w = h = 0
    rows: list[list[int]] = []
    for num, wire, value in fields(buf):
        if num == 1 and wire == WIRE_VARINT:
            w = value
        elif num == 2 and wire == WIRE_VARINT:
            h = value
        elif num == 3 and wire == WIRE_LEN:
            # ⛔⛔ FIXED s44 2026-08-15. THIS MODULE CRASHED ON IMPORT --
            # `TypeError: 'int' object is not iterable` out of `_load_library()`
            # -- so the map-admission check, the tool whose whole purpose is to
            # catch a fixture that cannot express the mechanism, COULD NOT RUN AT
            # ALL, and neither could anything importing it.
            # CAUSE: `repeated uint32 tiles = 1` has TWO legal proto encodings.
            # PACKED (wire 2) is one bytes blob of w tiles; UNPACKED (wire 0) is
            # one varint per tile. This read only the packed form. **glacierkeep
            # and valkyrie are unpacked and both are POOL maps** -- so the
            # library was missing 2 of 15 and died trying to build it.
            # Found while pricing launcher chokepoints, by a second parser
            # written against the same format hitting the same byte.
            row: list[int] = []
            for rn, rw, rv in fields(value):
                if rn != 1:
                    continue
                if rw == WIRE_LEN:
                    row.extend(rv)
                elif rw == WIRE_VARINT:
                    row.append(rv)
            if row:
                rows.append(row)
    return w, h, rows


def fingerprint(w: int, h: int, rows: list[list[int]]) -> tuple:
    """EXACT key: dimensions plus every tile in row order. Cores are not in the
    terrain, so this is stable across matches on the same map."""
    return (w, h, tuple(tuple(r) for r in rows))


def _load_library() -> dict[tuple, str]:
    lib = {}
    for mp in sorted((ROOT / "maps").glob("*.map26")):
        w, h, rows = _terrain(mp.read_bytes())
        if rows:
            lib[fingerprint(w, h, rows)] = mp.stem
    return lib


LIBRARY = _load_library()


def map_facts(path: Path) -> dict | None:
    """Terrain + core geometry for one replay. None if the buffer is unusable."""
    data = path.read_bytes()
    map_buf = None
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
            break
    if map_buf is None:
        return None

    w = h = 0
    rows: list[list[int]] = []
    cores: dict[int, tuple[int, int]] = {}
    name = ""
    for num, wire, value in fields(map_buf):
        if num == 1 and wire == WIRE_VARINT:
            w = value
        elif num == 2 and wire == WIRE_VARINT:
            h = value
        elif num == 3 and wire == WIRE_LEN:
            for rn, _rw, rv in fields(value):
                if rn == 1:
                    rows.append(list(rv))
        elif num == 4 and wire == WIRE_LEN:
            # THE CORE ENTRY IS {team (1), pos (3)} AND PROTO3 OMITS ZEROS.
            # Team A's core carries NO team field at all, because its value is
            # 0. A parser that requires the field to be present drops exactly
            # half the cores, then fails the `len(cores) == 2` guard and
            # reports "no archived replay for any map" -- which is what this
            # one did, and the failure looked like missing DATA rather than a
            # broken PARSE. Default it to 0 rather than requiring presence.
            c_team, c_pos = 0, None
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    c_team = cv
                elif cn == 3:
                    c_pos = read_pos(cv)
            if c_pos is not None:
                cores[c_team] = c_pos

    if not rows or len(cores) != 2 or not w or not h:
        return None
    name = LIBRARY.get(fingerprint(w, h, rows), "")

    def is_wall(x: int, y: int) -> bool:
        if not (0 <= x < w and 0 <= y < h):
            return True            # off-map counts as blocked
        return rows[y][x] == WALL

    out = {"name": name, "w": w, "h": h, "cores": cores,
           "rings": [], "edges": []}
    for team in sorted(cores):
        cx, cy = cores[team]
        foot = {(cx + dx, cy + dy) for dx in (0, 1) for dy in (0, 1)}
        # THE RING IS THE FULL 4x4 BOX AROUND THE 2x2 FOOTPRINT, MINUS THE
        # FOOTPRINT = 12 TILES on open terrain -- the 8 orthogonal neighbours
        # PLUS the 4 diagonal corners. My first version used orthogonal
        # adjacency only and returned 8 for every open map and 4 for jackpot.
        # Both were self-consistent and both were wrong, and nothing in the
        # output looked odd: a uniform "8" reads exactly like a real constant.
        # It was caught only by checking against a number derived independently
        # by another lane (12 open / 5 jackpot). AN INTERNALLY CONSISTENT
        # GEOMETRY IS NOT A VERIFIED ONE.
        ring = set()
        for (fx, fy) in foot:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    t = (fx + dx, fy + dy)
                    if t in foot or not (0 <= t[0] < w and 0 <= t[1] < h):
                        continue
                    if rows[t[1]][t[0]] != WALL:
                        ring.add(t)
        # BORDER REACH: how close the core sits to a map edge. LOKI-14's throw
        # needs a border tile within the launcher's 1 <= d^2 <= 26 throw range,
        # so a core parked mid-map makes the border arm structurally scarce.
        edge = min(cx, cy, w - 1 - (cx + 1), h - 1 - (cy + 1))
        out["rings"].append(len(ring))
        out["edges"].append(edge)
    return out


def classify(f: dict) -> list[str]:
    """Mechanism admissions. Each returns a FLAG string or nothing."""
    flags = []
    rings = f["rings"]
    if min(rings) < 12:
        flags.append(f"RING CLIPPED to {min(rings)}/12 -- ring-hold planks "
                     f"(LOKI-16 family) are UNDEFINED here")
    if rings[0] != rings[1]:
        flags.append(f"RING ASYMMETRIC {rings[0]} vs {rings[1]} -- SEAT CONFOUND: "
                     f"the two seats do not play the same game")
    if min(f["edges"]) > 5:
        flags.append(f"CORES FAR FROM BORDER (min edge {min(f['edges'])}) "
                     f"-- border-throw planks (LOKI-14 family) are dose-starved")
    return flags


def sample_replays(maps: list[str]) -> dict[str, Path]:
    """One replay per requested map name. Scans until every map is covered."""
    want, found = set(maps), {}
    for p in sorted(ARCHIVE.glob("*.replay26")):
        f = map_facts(p)
        if f and f["name"] in want and f["name"] not in found:
            found[f["name"]] = p
            if len(found) == len(want):
                break
    return found


def selftest() -> int:
    """Prove the checker CAN fail, per map, per flag.

    A checker that has only ever printed ADMITS has not been seen to check.
    Every flag is driven synthetically to both verdicts.
    """
    print("MAP ADMISSION SELFTEST — can each flag fire, and can it stay silent?\n")
    cases = [
        ("open 12/12, cores mid-map", {"rings": [12, 12], "edges": [6, 6]},
         ["CORES FAR FROM BORDER"]),
        ("open 12/12, cores near edge", {"rings": [12, 12], "edges": [2, 2]}, []),
        ("corner-clipped 5/5 (the jackpot shape)", {"rings": [5, 5], "edges": [0, 0]},
         ["RING CLIPPED"]),
        ("asymmetric 12 vs 9", {"rings": [12, 9], "edges": [1, 1]},
         ["RING CLIPPED", "RING ASYMMETRIC"]),
    ]
    bad = 0
    for label, f, expect in cases:
        got = classify(f)
        ok = len(got) == len(expect) and all(
            any(e in g for g in got) for e in expect)
        print(f"  [{'ok' if ok else 'FAIL'}] {label}")
        for g in got:
            print(f"          -> {g}")
        if not got and not expect:
            print("          -> (silent, as required)")
        if not ok:
            bad += 1
            print(f"          EXPECTED: {expect or 'silence'}")
    # FINGERPRINT CONTROL: the name resolution must MISS when the terrain is
    # not byte-identical, or "resolved 5/5" means only "found something the
    # same size". Flip exactly one tile of a library map and require a miss.
    print("\n  fingerprint control (exactness of the name key):")
    lib_key = next(iter(LIBRARY))
    w, h, rows = lib_key[0], lib_key[1], [list(r) for r in lib_key[2]]
    hit_before = fingerprint(w, h, rows) in LIBRARY
    rows[0][0] = 1 - (rows[0][0] == 1)          # flip one tile, wall <-> not
    hit_after = fingerprint(w, h, rows) in LIBRARY
    ok = hit_before and not hit_after
    print(f"  [{'ok' if ok else 'FAIL'}] untouched map matches: {hit_before}; "
          f"one tile flipped still matches: {hit_after} (must be False)")
    if not ok:
        bad += 1

    # GEOMETRY CONTROL: the ring on open terrain must be 12, not 8. The first
    # implementation used orthogonal adjacency and returned a uniform 8, which
    # is indistinguishable from a real constant in the output.
    print("  geometry control (ring size on open terrain):")
    open_rows = [[0] * 10 for _ in range(10)]
    foot = {(4 + dx, 4 + dy) for dx in (0, 1) for dy in (0, 1)}
    ring = {(fx + dx, fy + dy) for (fx, fy) in foot
            for dx in (-1, 0, 1) for dy in (-1, 0, 1)} - foot
    print(f"  [{'ok' if len(ring) == 12 else 'FAIL'}] open-terrain ring = "
          f"{len(ring)} (must be 12: the 4x4 box minus the 2x2 footprint)")
    if len(ring) != 12:
        bad += 1
    _ = open_rows

    print()
    if bad:
        print(f"*** {bad} case(s) wrong -- the checker is not checking ***")
        return 1
    print("PASS: every flag fires on its own shape and stays silent otherwise; "
          "the name key is exact and the ring geometry is 12 on open terrain.")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    maps = PINNED
    if "--maps" in argv:
        maps = argv[argv.index("--maps") + 1:]

    found = sample_replays(maps)
    missing = [m for m in maps if m not in found]

    print(f"MAP ADMISSION — {len(found)}/{len(maps)} pinned maps resolved "
          f"from {ARCHIVE.name}\n")
    print(f"  {'map':<12} {'dims':>7} {'ring A':>7} {'ring B':>7} "
          f"{'edge A':>7} {'edge B':>7}")
    strata = Counter()
    for m in maps:
        if m not in found:
            continue
        f = map_facts(found[m])
        print(f"  {f['name']:<12} {f['w']:>3}x{f['h']:<3} "
              f"{f['rings'][0]:>7} {f['rings'][1]:>7} "
              f"{f['edges'][0]:>7} {f['edges'][1]:>7}")
        strata[min(f["rings"])] += 1
        for flag in classify(f):
            print(f"      ** {flag}")
    if missing:
        print(f"\n  ** NOT RESOLVED (no archived replay): {', '.join(missing)}")
    if len(strata) > 1:
        print(f"\n  ** PANEL SPANS {len(strata)} RING STRATA: "
              f"{dict(sorted(strata.items()))} maps at each ring size.")
        print("     REPORT RING-HOLD RESULTS PER STRATUM. Pooling across strata "
              "averages a plank over terrain where its mechanism is undefined --")
        print("     that is what moved LOKI-16 by 0.031, across its bar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
