#!/usr/bin/env python3
"""Resource-flow census — where does each titanium stack actually GO?

`distributeResources` (Update field 4) carries every physical resource move as
`ResourceMove { Pos from = 1; Pos to = 2; optional int32 resourceId = 3 }`.
49,440 events per 120 replays, never decoded until now.

This answers a question no other stream can: **how much of a team's titanium is
delivered into the OPPONENT'S network?** The engine allows pushing resources onto
an opposing conveyor network or core, so a mis-facing conveyor at a contact point
is not merely dead weight — it is a pump feeding the enemy's tiebreak key #1.

Classification of each move, by who owns the building on the destination tile:
    OWN_CORE     delivered home (this is tiebreak key #1)
    OWN_NET      moved along own conveyor/splitter
    ENEMY_CORE   delivered into the ENEMY core -- a scored own-goal
    ENEMY_NET    pushed onto enemy conveyors -- likely to become ENEMY_CORE
    GROUND       destination holds no building we know of

Emits one row per file x source-team x band x class.
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
from replay_census import guard_out, fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

CARRIERS = ("conveyor", "splitter", "harvester")


def band(r):
    return "r0-150" if r < 150 else "r150-200" if r < 200 else "r200-300" if r < 300 else "r300+"


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
    cores = []
    for num, _w, value in fields(map_buf):
        if num == 4:
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
    # tile -> (team, kind); cores seeded as their 4 footprint tiles
    tile = {}
    for c in cores:
        x, y = c["pos"]
        for dx in (0, 1):
            for dy in (0, 1):
                tile[(x + dx, y + dy)] = (c["team"], "core")
    counts = {}

    def bump(team, b, cls, n=1):
        counts[(team, b, cls)] = counts.get((team, b, cls), 0) + n

    for rnd, turn_buf in enumerate(turn_bufs):
        b = band(rnd)
        for _n, _w2, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None or e.kind == "builder_bot":
                            continue
                        tile[e.pos] = (e.team, e.kind)
                elif unum == 3:
                    pass  # removal leaves a stale tile owner; see LIMITS in the doc
                elif unum == 4:
                    for _mn, _mw, mv in fields(ubuf):
                        src = dst = None
                        for pn, _pw, pval in fields(mv):
                            if pn == 1:
                                src = read_pos(pval)
                            elif pn == 2:
                                dst = read_pos(pval)
                        if src is None or dst is None:
                            continue
                        s = tile.get(src)
                        d = tile.get(dst)
                        if s is None:
                            continue                 # unknown origin, skip
                        team = s[0]
                        if d is None:
                            bump(team, b, "GROUND")
                        elif d[1] == "core":
                            bump(team, b, "OWN_CORE" if d[0] == team else "ENEMY_CORE")
                        elif d[1] in CARRIERS:
                            bump(team, b, "OWN_NET" if d[0] == team else "ENEMY_NET")
                        else:
                            bump(team, b, "GROUND")
    for (t, bb, cls), n in counts.items():
        out.write(f"{path.name}\t{t}\t{bb}\t{cls}\t{n}\n")


def main(argv):
    guard_out(argv[0])
    out = open(argv[0], "w")
    out.write("file\tteam\tband\tclass\tn\n")
    bad = 0
    for i, p in enumerate(Path(x) for x in argv[1:]):
        try:
            census(p, out)
        except Exception as exc:                                # noqa: BLE001
            bad += 1
            print(f"ERR {p.name}: {exc}", file=sys.stderr)
        if (i + 1) % 500 == 0:
            print(f"  ...{i+1}/{len(argv)-1} ({bad} err)", file=sys.stderr, flush=True)
    out.close()
    print(f"done {len(argv)-1} files, {bad} errors", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
