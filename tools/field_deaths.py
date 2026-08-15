#!/usr/bin/env python3
"""Field mechanism read: our builder deaths per 1k rounds, by OUR version.

Closes the loop a local battery cannot. `mech_battery.py` measures the plank
against imitations; this measures the SHIPPED bot against real opponents, from
the replays the archiver already has. Same decode as the battery
(placeEntity -> removeEntity on builder ids), so the two numbers are
commensurable.

Seat is read from each match's `.meta.json` (`teamAId` vs our team id), which
is the platform's own record and needs no corpus join -- so this works on
matches that landed minutes ago and are not yet in `corpus/join.tsv`.

Usage:
  .venv/bin/python tools/field_deaths.py --versions 92 91 90 [--since ISO]
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, parse_entity, WIRE_LEN  # noqa: E402

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

OUR_TEAM_ID = "379a5d80-9921-4c9e-949b-f9b1dcba16be"


def decode(job):
    path, our_seat = job
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
    team_of, is_bot = {}, set()
    deaths = spawns = 0
    for rnd, turn_buf in enumerate(turn_bufs):
        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None or e.id in team_of:
                            continue
                        team_of[e.id] = e.team
                        if e.kind == "builder_bot":
                            is_bot.add(e.id)
                            if e.team == our_seat:
                                spawns += 1
                elif unum == 3:
                    rid = None
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            rid = rv
                    if rid in is_bot and team_of.get(rid) == our_seat:
                        deaths += 1
    return (len(turn_bufs), deaths, spawns)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--versions", nargs="+", type=int, required=True)
    ap.add_argument("--archive", default="replay_archive")
    ap.add_argument("--jobs", type=int, default=5)
    ap.add_argument("--opponent", help="hold the opponent constant -- without "
                                       "this the version rows are not comparable")
    args = ap.parse_args()

    want = set(args.versions)
    jobs, meta_of = [], {}
    for mp in Path(args.archive).glob("*.meta.json"):
        try:
            m = json.loads(mp.read_text())
        except Exception:
            continue
        if m.get("teamAId") == OUR_TEAM_ID:
            ver, seat, opp = m.get("teamAVersion"), 0, m.get("teamBName")
        elif m.get("teamBId") == OUR_TEAM_ID:
            ver, seat, opp = m.get("teamBVersion"), 1, m.get("teamAName")
        else:
            continue
        if ver not in want or m.get("triggeredBy") != "ladder":
            continue
        if args.opponent and opp != args.opponent:
            continue
        for g in sorted(Path(args.archive).glob(f"{m['id']}_game_*.replay26")):
            jobs.append((g, seat))
            meta_of[g.name] = (ver, opp)
    print(f"{len(jobs)} ladder games across versions {sorted(want)}", file=sys.stderr)
    if not jobs:
        return 1

    agg = defaultdict(lambda: [0, 0, 0, 0])   # ver -> games, rounds, deaths, spawns
    with Pool(args.jobs) as pool:
        for job, res in zip(jobs, pool.map(decode, jobs)):
            if res is None:
                continue
            rounds, deaths, spawns = res
            ver = meta_of[job[0].name][0]
            a = agg[ver]
            a[0] += 1
            a[1] += rounds
            a[2] += deaths
            a[3] += spawns

    print(f"\nOUR BUILDER DEATHS vs REAL OPPONENTS, by shipped version")
    print(f"  {'ver':>4s} {'games':>6s} {'rounds':>8s} {'deaths':>7s} "
          f"{'per 1k rounds':>14s} {'per spawn':>10s}")
    for ver in sorted(agg, reverse=True):
        g, r, d, s = agg[ver]
        print(f"  v{ver:<3d} {g:6d} {r:8d} {d:7d} {1000 * d / max(1, r):14.3f} "
              f"{d / max(1, s):10.3f}")
    if args.opponent:
        print(f"\nOpponent held constant ({args.opponent}). Version rows are "
              f"comparable, subject to n.")
    else:
        print("\n*** OPPONENT NOT HELD CONSTANT -- these rows are NOT comparable. ***"
              "\n  Builder-death hazard varies ~7x across opponents (Ouroboros 4.16 vs"
              "\n  Team 48 0.6 per game), so a version that happened to draw gentle"
              "\n  opponents looks better for that reason alone. Measured instance, s24:"
              "\n  v92's first ladder match read 1.250/1k against v91's pooled 19.257 --"
              "\n  a 15x 'improvement' that vanished to 1.250 vs 1.572 the moment the"
              "\n  opponent was fixed. Re-run with --opponent before quoting anything.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
