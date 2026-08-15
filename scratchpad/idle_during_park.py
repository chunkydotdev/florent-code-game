#!/usr/bin/env python3
"""IDLE-DURING-PARK — does a parked builder ACT while it is parked?

WHY THIS EXISTS.  `tools/nav_lock_census.py` with `--max-tiles 1 --max-dwell inf`
answers "is a bot stationary for >=50 rounds", and reports `never acted` — but
that field is LIFE-SCOPED: a bot that builds at round 3 then parks for 400
rounds counts as having acted.  The question "how many games have IDLE builders"
needs the WINDOW-SCOPED version: did the bot act DURING its park?

⛔ D24(e) AVOIDANCE — THIS FILE DUPLICATES NOTHING LOAD-BEARING.  It calls
`nav_lock_census.decode_tracks` and `.analyze_bot_lock` and `.population`
UNCHANGED, so the position decode and the lock predicate are the certified ones.
The only new code is `action_rounds()`, a flat scan for the three builder-action
update numbers, which touches no position state.  A parallel re-implementation of
the position decode is exactly what a selftest would have validated into
existence; there isn't one here.

ACTIONS.  `UPD_ACTIONS = (13, 15, 16)` = builderAttack / builderHeal /
builderBuild — the only builder actions the wire attributes to a bot id
(`nav_lock_census.py:114-120`).  `destroy` and `self_destruct` surface as an
unattributed removeEntity, so a bot that ONLY destroys reads as idle here.
Stated as a known OVER-count of idleness, direction declared.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "tools"))

import nav_lock_census as NLC  # noqa: E402

MIN_SPAN = 50
PARK = dict(min_span=MIN_SPAN, max_tiles=1, max_dwell=10 ** 6)


def action_rounds(path):
    """{bot_id: {round, ...}} for builderAttack/Heal/Build. Position-free."""
    data = Path(path).read_bytes()
    out = defaultdict(set)
    rnd = -1
    for num, wire, value in NLC.fields(data):
        if num != 3 or wire != NLC.WIRE_LEN:
            continue
        rnd += 1
        # ⛔ THREE levels, not two: turn_buf -> upd wrapper -> update-type buf.
        # Collapsing the middle level makes `unum` read the wrapper's field
        # number (always 1), so NOTHING ever matches UPD_ACTIONS and the tool
        # reports 100% idle. That is exactly what the first draft did; it was
        # caught by the constant column, not by reading the code.
        for _n, _w, upd in NLC.fields(value):
            for unum, _uw, ubuf in NLC.fields(upd):
                if unum in NLC.UPD_ACTIONS:
                    for an, _aw, av in NLC.fields(ubuf):
                        if an == 1:
                            out[av].add(rnd)
                            break
    return out


def census(ourver, meta, archive, limit=None):
    agg = defaultdict(int)
    for path, our_team, _c, _v in NLC.population(ourver=ourver, meta=meta,
                                                 archive=archive, limit=limit):
        try:
            d = NLC.decode_tracks(path, our_team)
            acts = action_rounds(path)
        except Exception:
            continue
        agg["games"] += 1
        gp = gi = False
        for eid, b in d["bots"].items():
            agg["bots"] += 1
            a = NLC.analyze_bot_lock(b["track"], **PARK)
            if not a["strict"]:
                continue
            agg["parked_bots"] += 1
            agg["parked_rounds"] += a["strict_rounds"]
            gp = True
            lo = b["spawn"] + a["onset"]
            hi = b["spawn"] + len(b["track"]) - 1
            if not any(lo <= r <= hi for r in acts.get(eid, ())):
                agg["idle_bots"] += 1
                agg["idle_rounds"] += a["strict_rounds"]
                gi = True
        agg["games_any_park"] += gp
        agg["games_any_idle"] += gi
    return agg


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ourver", action="append", required=True)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--meta", default=str(NLC.DEFAULT_META))
    ap.add_argument("--archive", default=str(NLC.DEFAULT_ARCHIVE))
    args = ap.parse_args()

    hdr = ("%-6s %6s %13s %13s   %7s %7s   %10s %10s"
           % ("ver", "games", "w/ park", "w/ IDLE", "parked", "IDLE",
              "park-rnds", "idle-rnds"))
    print(hdr)
    tot = defaultdict(int)
    for v in args.ourver:
        a = census(v, args.meta, args.archive, args.limit)
        for k, x in a.items():
            tot[k] += x
        g = a["games"] or 1
        print("v%-5s %6d %13s %13s   %7d %7d   %10d %10d" % (
            v, a["games"],
            "%d (%.1f%%)" % (a["games_any_park"], 100 * a["games_any_park"] / g),
            "%d (%.1f%%)" % (a["games_any_idle"], 100 * a["games_any_idle"] / g),
            a["parked_bots"], a["idle_bots"], a["parked_rounds"], a["idle_rounds"]))
    g = tot["games"] or 1
    print("-" * len(hdr))
    print("%-6s %6d %13s %13s   %7d %7d   %10d %10d" % (
        "TOTAL", tot["games"],
        "%d (%.1f%%)" % (tot["games_any_park"], 100 * tot["games_any_park"] / g),
        "%d (%.1f%%)" % (tot["games_any_idle"], 100 * tot["games_any_idle"] / g),
        tot["parked_bots"], tot["idle_bots"], tot["parked_rounds"], tot["idle_rounds"]))
    if tot["parked_bots"]:
        print("\nof parked bots, %d/%d = %.1f%% took NO action during the park"
              % (tot["idle_bots"], tot["parked_bots"],
                 100 * tot["idle_bots"] / tot["parked_bots"]))
        print("parked bots = %.1f%% of all our builders (%d of %d)"
              % (100 * tot["parked_bots"] / tot["bots"], tot["parked_bots"], tot["bots"]))


if __name__ == "__main__":
    main()
