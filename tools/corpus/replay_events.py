#!/usr/bin/env python3
"""Every build and every death, with round / team / kind / position.

The general form of `replay_builds.py` (which only kept turrets). This is what
answers "play the players" questions:

  OPENING DETERMINISM  per (team, map): is the first harvester always on the
                       same tile? Anything highly modal is PRE-EMPTABLE, and a
                       barrier on an ore tile makes `can_build_harvester` false
                       for 3 Ti (builder-probed 2026-08-09).
  REACTION LATENCY     rounds from a building's death to that team's next build
                       of the same kind. A measured latency is a blindness
                       window, and a blindness window is timeable.

Rotation guard: `rotate()` re-emits `placeEntity` for an existing entity, which
inflates gunner builds ~3x. A build is the FIRST placeEntity carrying an id.

Emits BUILD and DEATH rows on one stream.
"""
from __future__ import annotations

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY THIS FILE NEEDED IT (measured 2026-08-16, s47). `tools/corpus/` sat
# OUTSIDE the help-contract sweep, which globbed `tools/*.py` only. Probed:
# 11 of 18 corpus tools violated the contract, and three of the failures are
# the dangerous classes the sweep exists to catch —
#   * `unrated_games.py --help` REWROTE corpus/unrated_games.tsv (1.1 MB)
#   * `ladder_meta.py`, `league_maps.py`, `league_matches.py`, `meta_attrib.py`
#     --help went to the NETWORK and ran until killed at 20 s
#   * `replay_autopsy.py --help` raised TypeError out of replay_census.fields()
# and the rest printed verdict-shaped text in this repo's own vocabulary
# ("no *.replay26 under --help", "sides loaded: 0 (from 0 matches) — --help").
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by build_corpus /
# keeper. Ungated, this would fire during that import and make the PARENT exit 0
# mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: the guard must not depend on what the host file
# happens to import, or on the order its imports appear in.
# ⛔ MUST SIT AFTER `from __future__ import ...`, which the language requires to
# be the first statement after the docstring.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

import sys
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import guard_out, fields, read_pos, parse_entity, WIRE_LEN, WIRE_VARINT  # noqa: E402


def census(path: Path, out):
    data = path.read_bytes()
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return
    w = h = 0
    cores = []
    tiles = []
    for num, wire, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
        elif num == 3:
            row = []
            for rn, rw, rv in fields(value):
                if rn == 1:
                    row.extend(_packed(rv) if rw == WIRE_LEN else [rv])
            tiles.append(row)
        elif num == 4:
            c = {"id": 0, "team": 0, "pos": (0, 0)}
            for cn, _cw, cv in fields(value):
                if cn == 1:
                    c["id"] = cv
                elif cn == 2:
                    c["team"] = cv
                elif cn == 3:
                    c["pos"] = read_pos(cv)
            cores.append(c)
    if len(cores) != 2:
        return
    corepos = {c["team"]: c["pos"] for c in cores}
    name = path.name
    ents = {c["id"]: (c["team"], "core", c["pos"]) for c in cores}

    def d2(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w2, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:                     # rotation re-emit
                            t, k, _p = ents[e.id]
                            ents[e.id] = (t, k, e.pos)
                            continue
                        ents[e.id] = (e.team, e.kind, e.pos)
                        own, enemy = corepos[e.team], corepos[1 - e.team]
                        out.write(f"{name}\tBUILD\t{rnd}\t{e.team}\t{e.kind}\t"
                                  f"{e.pos[0]}\t{e.pos[1]}\t{d2(e.pos, own)}\t"
                                  f"{d2(e.pos, enemy)}\t{w}\t{h}\n")
                elif unum == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in ents and to:
                        t, k, _p = ents[eid]
                        ents[eid] = (t, k, to)
                elif unum == 3:
                    for rn, _rw, rv in fields(ubuf):
                        e = ents.pop(rv, None)
                        if e is None:
                            continue
                        t, k, p = e
                        own, enemy = corepos[t], corepos[1 - t]
                        out.write(f"{name}\tDEATH\t{rnd}\t{t}\t{k}\t{p[0]}\t{p[1]}\t"
                                  f"{d2(p, own)}\t{d2(p, enemy)}\t{w}\t{h}\n")


def _packed(buf):
    out, i = [], 0
    while i < len(buf):
        r = s = 0
        while True:
            b = buf[i]
            i += 1
            r |= (b & 0x7F) << s
            if not (b & 0x80):
                break
            s += 7
        out.append(r)
    return out


def main(argv):
    guard_out(argv[0])
    out = open(argv[0], "w")
    out.write("file\tev\trnd\tteam\tkind\tx\ty\td2_own\td2_enemy\tmw\tmh\n")
    bad = 0
    for i, p in enumerate(Path(x) for x in argv[1:]):
        try:
            census(p, out)
        except Exception as exc:                             # noqa: BLE001
            bad += 1
            print(f"ERR {p.name}: {exc}", file=sys.stderr)
        if (i + 1) % 500 == 0:
            print(f"  ...{i+1}/{len(argv)-1} ({bad} err)", file=sys.stderr, flush=True)
    out.close()
    print(f"done {len(argv)-1} files, {bad} errors", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
