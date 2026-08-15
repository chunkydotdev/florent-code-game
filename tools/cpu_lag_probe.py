#!/usr/bin/env python3
"""Per-round CPU trace: does OUR entity count drive the OPPONENT's exec time?

The pooled/within-opponent cuts (see the s24 builder notes) show
r(our_entity_count, their_TLE_rate) = +0.33 for Ouroboros while
r(their_own_entity_count, their_TLE_rate) = -0.07.  That asymmetry has two
readings and the correlation cannot separate them:

  CAUSAL   our clutter enlarges whatever they iterate over -> their turns
           get slower -> they time out.
  REVERSE  they are slow/timing out -> they play worse -> we survive and
           build more.  This ALSO predicts our count up and theirs down.

This probe adds the one thing the game-level cut cannot have: TIME ORDER.
Per round it records our placements, their placements, their cumulative
entity count, ours, and their builder-bot exec time and TLE count.  The
analysis then asks whether a burst of OUR building at round R is followed by
a rise in THEIR exec time at R+1..R+k, after removing the within-game trend
(first differences), which is what makes it a lag test rather than a
"both things grow over a long game" test.

Read-only.  Usage:
  .venv/bin/python tools/cpu_lag_probe.py --opp Ouroboros [--jobs 5]
"""
from __future__ import annotations

import argparse
import csv
import sys
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, "tools")
from replay_census import fields, read_pos, parse_entity, WIRE_LEN  # noqa: E402

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


def decode(job):
    path, our_team = job
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

    team_of, kind_of = {}, {}
    for num, wire, value in fields(map_buf):
        if num != 4:
            continue
        cid = cteam = None
        for cn, _cw, cv in fields(value):
            if cn == 1:
                cid = cv
            elif cn == 2:
                cteam = cv
            elif cn == 3:
                read_pos(cv)
        if cid is not None:
            team_of[cid] = cteam or 0
            kind_of[cid] = "core"
    if len(team_of) != 2:
        return None

    alive_us = alive_them = 0
    out = []
    for rnd, turn_buf in enumerate(turn_bufs):
        place_us = place_them = 0
        rem_us = rem_them = 0
        ex_sum = ex_turns = tled = 0
        for _n, _w, ub in fields(turn_buf):
            for unum, _uw, ubuf in fields(ub):
                if unum == 1:                                     # placeEntity
                    for en, _ew, ebuf in fields(ubuf):
                        if en != 1:
                            continue
                        e = parse_entity(ebuf, rnd)
                        if e is None or e.id in kind_of:
                            continue                              # re-emit
                        team_of[e.id] = e.team
                        kind_of[e.id] = e.kind
                        if e.kind == "builder_bot":
                            continue                              # units, not clutter
                        if e.team == our_team:
                            place_us += 1
                        else:
                            place_them += 1
                elif unum == 3:                                   # removeEntity
                    rid = None
                    for rn, _rw, rv in fields(ubuf):
                        if rn == 1:
                            rid = rv
                    if rid is None or kind_of.get(rid) in (None, "builder_bot"):
                        continue
                    if team_of.get(rid) == our_team:
                        rem_us += 1
                    else:
                        rem_them += 1
                elif unum == 9:                                   # botOutput
                    eid = exec_us = None
                    tl = False
                    for bn, _bw, bv in fields(ubuf):
                        if bn == 1:
                            eid = bv
                        elif bn == 3:
                            exec_us = bv
                        elif bn == 4:
                            tl = bool(bv)
                    if eid is None or kind_of.get(eid) != "builder_bot":
                        continue
                    if team_of.get(eid) == our_team:
                        continue                                  # THEIR turns only
                    ex_turns += 1
                    if exec_us:
                        ex_sum += exec_us
                    if tl:
                        tled += 1
        alive_us += place_us - rem_us
        alive_them += place_them - rem_them
        out.append((path.name, rnd, place_us, alive_us, alive_them,
                    ex_turns, ex_sum, tled))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--opp", action="append", required=True)
    ap.add_argument("--archive", default="replay_archive")
    ap.add_argument("--jobs", type=int, default=5)
    ap.add_argument("-o", "--out", default="scratchpad/cpu_lag.tsv")
    args = ap.parse_args()

    want = set(args.opp)
    jobs = []
    for r in csv.DictReader(open("corpus/join.tsv"), delimiter="\t"):
        if r["opp"] not in want:
            continue
        p = Path(args.archive) / r["file"]
        if p.exists():
            jobs.append((p, int(r["our_team"])))
    print(f"{len(jobs)} replays vs {sorted(want)}", file=sys.stderr)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(args.out, "w") as fh:
        fh.write("file\trnd\tplace_us\talive_us\talive_them\t"
                 "their_turns\ttheir_exec_sum\ttheir_tled\n")
        with Pool(args.jobs) as pool:
            for rows in pool.imap_unordered(decode, jobs, chunksize=4):
                if rows is None:
                    continue
                n += 1
                for r in rows:
                    fh.write("\t".join(str(x) for x in r) + "\n")
    print(f"decoded {n} -> {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
