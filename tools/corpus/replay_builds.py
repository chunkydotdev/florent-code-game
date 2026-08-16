#!/usr/bin/env python3
"""Per-band, per-team build + aggression census — where does each team put its turrets?

One row per BUILD event (first placeEntity per entity id only — the rotation
re-emit guard from replay_census.py: rotate() re-emits placeEntity for gunners,
so counting every place inflates gunner builds ~3x).

Columns include d2 to the builder's OWN core and to the ENEMY core, which is the
direct test of "the top tier's gunners are OFFENSIVE, ours sit at home".

Also emits per-file/per-team/per-band aggregate counters for builderAttack and
fireTurret on a second stream (prefix AGG).
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


def d2(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def band(r):
    return "r0-150" if r < 150 else "r150-200" if r < 200 else "r200-300" if r < 300 else "r300+"


def census(path: Path, out, agg):
    data = path.read_bytes()
    map_buf, turn_bufs, winner = None, [], None
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
        elif num == 4 and wire == WIRE_VARINT:
            winner = value
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
    corepos = {c["team"]: c["pos"] for c in cores}
    if len(corepos) != 2:
        return
    foot = {t: {(p[0] + dx, p[1] + dy) for dx in (0, 1) for dy in (0, 1)}
            for t, p in corepos.items()}

    ents = {c["id"]: (c["team"], "core", c["pos"]) for c in cores}
    pos = {c["id"]: c["pos"] for c in cores}
    counts = {}          # (team, band, metric) -> n
    name = path.name

    def bump(team, b, metric, n=1):
        counts[(team, b, metric)] = counts.get((team, b, metric), 0) + n

    for rnd, turn_buf in enumerate(turn_bufs):
        b = band(rnd)
        for _n, _w2, update_buf in fields(turn_buf):
            for unum, _uw, ubuf in fields(update_buf):
                if unum == 1:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None:
                            continue
                        if e.id in ents:                     # rotation re-emit
                            pos[e.id] = e.pos
                            continue
                        ents[e.id] = (e.team, e.kind, e.pos)
                        pos[e.id] = e.pos
                        own = corepos[e.team]
                        enemy = corepos[1 - e.team]
                        bump(e.team, b, "build_" + e.kind)
                        if e.kind in ("gunner", "sentinel", "launcher"):
                            do, de = d2(e.pos, own), d2(e.pos, enemy)
                            out.write(f"{name}\t{rnd}\t{b}\t{e.team}\t{e.kind}\t"
                                      f"{e.pos[0]}\t{e.pos[1]}\t{do}\t{de}\t"
                                      f"{'FORWARD' if de < do else 'HOME'}\t"
                                      f"{-1 if winner is None else winner}\n")
                elif unum == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid in pos and to:
                        pos[eid] = to
                elif unum == 3:
                    for rn, _rw, rv in fields(ubuf):
                        ents.pop(rv, None)
                        pos.pop(rv, None)
                elif unum == 12:                              # fireTurret
                    frm = None
                    for fn, _fw, fv in fields(ubuf):
                        if fn == 1:
                            frm = read_pos(fv)
                    if frm is None:
                        continue
                    for eid, (t, k, _p) in ents.items():
                        if k in ("gunner", "sentinel") and pos.get(eid) == frm:
                            bump(t, b, "shot")
                            break
                elif unum == 13:                              # builderAttack
                    aid = tgt = None
                    for an, _aw, av in fields(ubuf):
                        if an == 1:
                            aid = av
                        elif an == 2:
                            tgt = read_pos(av)
                    ent = ents.get(aid)
                    if ent is None or tgt is None:
                        continue
                    t = ent[0]
                    bump(t, b, "batk")
                    if tgt in foot[1 - t]:
                        bump(t, b, "batk_core")
    for (t, bb, metric), n in counts.items():
        agg.write(f"{name}\t{t}\t{bb}\t{metric}\t{n}\n")


def main(argv):
    guard_out(argv[0])
    out = open(argv[0], "w")
    agg = open((guard_out(argv[1]) or argv[1]), "w")
    out.write("file\trnd\tband\tteam\tkind\tx\ty\td2_own\td2_enemy\tside\twinner\n")
    agg.write("file\tteam\tband\tmetric\tn\n")
    bad = 0
    for i, p in enumerate(Path(x) for x in argv[2:]):
        try:
            census(p, out, agg)
        except Exception as exc:                              # noqa: BLE001
            bad += 1
            print(f"ERR {p.name}: {exc}", file=sys.stderr)
        if (i + 1) % 500 == 0:
            print(f"  ...{i+1}/{len(argv)-2} ({bad} err)", file=sys.stderr, flush=True)
    out.close(); agg.close()
    print(f"done {len(argv)-2} files, {bad} errors", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
