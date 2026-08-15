#!/usr/bin/env python3
"""How much of the available headroom does the shipped DODGE rule capture?

The corpus can bound the OPPORTUNITY -- 89-91% of our builder deaths are
preceded by a round standing in an enemy turret's ray, and the genuinely
unpreventable floor is 0.97%. It cannot say what fraction of that the live
code actually takes, because the corpus only contains bots that never had the
rule. That needs a paired battery with both arms instrumented, which is what
this reads.

Metric: OUR builder-rounds spent inside an enemy gunner/sentinel ray, per 1,000
builder-rounds lived. The plank's whole claim is that it lowers this; deaths
are downstream of it. If exposure barely moves while deaths do, the deaths were
moving for some other reason and the mechanism story is wrong.

The ray reconstruction is IMPORTED from the research arm's `dwell_decode.py`
rather than re-derived. It is validated against 485,925 real `fireTurret`
events -- 99.991% of gunner shots and 100.000% of sentinel shots land on the
reconstructed ray -- and re-deriving geometry is exactly how two measurements
of the same thing silently stop agreeing.

Matches what v92 ships: the RAY rule (facing, blocking IGNORED), because
`get_attackable_tiles_from` returns the raw pattern "even behind walls". The
exact-LINE variant is a different, narrower rule and is NOT what is live.

Usage:
  .venv/bin/python tools/dodge_capture.py scratchpad/dodge/replays
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, "tools")
sys.path.insert(0, "docs/research/scripts/side-lane-2026-08-09")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402
from dwell_decode import ray  # noqa: E402  -- validated, do not re-derive

# ---- `--help` CONTRACT (enforced by tests/test_instruments.py) --------------
# Side-effect-free, prints this module's docstring, exits 0.
#
# ⛔ WHY. Probing an unknown tool with `--help` is the first thing anyone does.
# Before 2026-08-15, 40 of 86 tools here had no argparse, so `--help` was just an
# unrecognised argument and THE TOOL RAN FOR REAL -- printing VERDICT-SHAPED text
# that reads as a finding:
#     tools/freshness.py --help  ->  "BLIND: --help has no parseable timestamp"
#     tools/leg_read.py  --help  ->  "LEG: no completed games"
# Both are this repo's own verdict vocabulary. A reader asking a harmless
# question got an authoritative-looking sentence about nothing.
#
# ⛔ GATED ON `__main__`: several of these modules are IMPORTED by other tools
# (freshness by now.py). Ungated, this would fire during that import and make the
# PARENT exit 0 mid-run while printing the CHILD's docstring.
# ⛔ SELF-CONTAINED `import sys`: a first attempt used the file's own import, and
# broke on `import sys as _sys` (NameError) and on files whose imports come in
# two blocks. The guard must not depend on what the host file happens to import.
if __name__ == "__main__":
    import sys as _hg_sys
    if "-h" in _hg_sys.argv[1:] or "--help" in _hg_sys.argv[1:]:
        print(__doc__ or ("usage: " + __file__ + "  (no module docstring)"))
        raise SystemExit(0)

GUN_R2, SEN_R2 = 13, 32


def decode(path: Path):
    """-> (arm, our_builder_rounds, in_envelope_rounds, deaths)."""
    name = path.name
    arm = "variant" if name.startswith("variant__") else "control"
    our_seat = 0 if name.endswith("__a.replay26") else 1
    try:
        data = path.read_bytes()
    except OSError:
        return None
    map_buf, turn_bufs = None, []
    for num, wire, value in fields(data):
        if num == 1 and wire == WIRE_LEN:
            map_buf = value
        elif num == 3 and wire == WIRE_LEN:
            turn_bufs.append(value)
    if map_buf is None:
        return None
    w = h = 0
    for num, _wire, value in fields(map_buf):
        if num == 1:
            w = value
        elif num == 2:
            h = value
    if not w or not h:
        return None

    team_of, kind_of, dir_of, pos_of = {}, {}, {}, {}
    bots, turrets = set(), set()
    lived = exposed = deaths = 0
    for _rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, 0)
                        if e is None:
                            continue
                        team_of[e.id] = e.team
                        kind_of[e.id] = e.kind
                        pos_of[e.id] = e.pos
                        if e.direction is not None:
                            dir_of[e.id] = e.direction
                        if e.kind == "builder_bot":
                            bots.add(e.id)
                        elif e.kind in ("gunner", "sentinel"):
                            turrets.add(e.id)
                elif unum == 2:
                    eid = to = None
                    for mn, _mw, mv in fields(ubuf):
                        if mn == 1:
                            eid = mv
                        elif mn == 2:
                            to = read_pos(mv)
                    if eid is not None and to is not None:
                        pos_of[eid] = to
                elif unum == 3:
                    rid = None
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            rid = rv
                    if rid is None:
                        continue
                    if rid in bots:
                        bots.discard(rid)
                        if team_of.get(rid) == our_seat:
                            deaths += 1
                    turrets.discard(rid)
                    pos_of.pop(rid, None)

        # End-of-round board, matching the dwell census's own convention.
        danger = set()
        for tid in turrets:
            if team_of.get(tid) == our_seat:
                continue
            p = pos_of.get(tid)
            if p is None:
                continue
            r2 = GUN_R2 if kind_of[tid] == "gunner" else SEN_R2
            danger.update(ray(p, dir_of.get(tid), r2, w, h))
        for bid in bots:
            if team_of.get(bid) != our_seat:
                continue
            lived += 1
            if pos_of.get(bid) in danger:
                exposed += 1
    return (arm, lived, exposed, deaths)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("replays")
    ap.add_argument("--jobs", type=int, default=5)
    args = ap.parse_args()
    files = sorted(Path(args.replays).glob("*.replay26"))
    print(f"{len(files)} replays", file=sys.stderr)
    if not files:
        return 1
    agg = defaultdict(lambda: [0, 0, 0, 0])
    with Pool(args.jobs) as pool:
        for r in pool.map(decode, files):
            if r is None:
                continue
            arm, lived, exposed, deaths = r
            a = agg[arm]
            a[0] += 1
            a[1] += lived
            a[2] += exposed
            a[3] += deaths

    print("\nEXPOSURE — our builder-rounds spent inside an enemy turret's ray")
    print(f"  {'arm':9s} {'games':>6s} {'builder-rounds':>15s} {'in envelope':>12s} "
          f"{'per 1k':>8s} {'deaths':>7s} {'deaths/1k exposed':>18s}")
    for arm in ("control", "variant"):
        g, lived, exp, d = agg[arm]
        if not lived:
            continue
        print(f"  {arm:9s} {g:6d} {lived:15d} {exp:12d} {1000 * exp / lived:8.2f} "
              f"{d:7d} {1000 * d / max(1, exp):18.2f}")
    c, v = agg["control"], agg["variant"]
    if c[1] and v[1]:
        ce, ve = 1000 * c[2] / c[1], 1000 * v[2] / v[1]
        print(f"\n  EXPOSURE CHANGE: {ce:.2f} -> {ve:.2f} per 1k builder-rounds "
              f"({100 * (ve - ce) / ce:+.1f}%)")
        print("  If exposure barely moves while deaths do, the deaths moved for some")
        print("  other reason and the mechanism story is wrong. That is the check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
