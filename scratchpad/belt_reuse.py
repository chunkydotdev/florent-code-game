#!/usr/bin/env python3
"""BELT REUSE — do we ever wire a new harvester into an EXISTING band, or do we
always lay a fresh parallel one?

THE CODE PREDICTION (v140 = bots/_v223sealrepair):
  `eco.py:504 _wire_on_build` has two branches.
    * linker BUSY  -> queue to `wire_pending`; `_wire_tick:534` later calls
      `_has_acceptor` and DROPS the job if the harvester is already connected.
    * linker FREE  -> `self.link_queue = self._link_path(ct, bp)` immediately,
      with NO acceptor check at all.
  `_link_path:391` BFS's to the CORE — its goals are core-adjacent tiles only.
  An existing friendly conveyor is merely PASSABLE, never a goal and never
  preferred. ⇒ a harvester built beside a working band still gets a whole new
  route planned to the core.
  Why that is pure waste, in the tree's own words (`_l4_harvester_starved`):
  "a harvester emits one stack per 4 rounds however many acceptors surround it,
  so the extra link is 3 Ti and +1% team cost scale for zero throughput."

TWO MEASURES, because they answer different halves:
  A. CONNECTED-AT-BUILD — of our harvesters, how many already had one of our
     conveyor/splitter/core cardinally adjacent at the moment they were placed?
     Those are the ones the FREE branch re-routes for nothing.
  B. SIDE-BY-SIDE PAIRS — our conveyor pairs that are cardinally adjacent but
     NOT chained (neither one's output tile is the other's position). That is
     literally "a band running next to a band", i.e. what was observed on
     screen. Chained neighbours are excluded, so a normal straight belt scores 0.

⛔ WHAT THIS IS NOT.  It does not prove a given parallel band was avoidable —
two harvesters on opposite sides of the core legitimately need two routes.
Measure B counts ADJACENCY, which is the visual; measure A counts the code path
that produces the avoidable subset.

Reuses `tools/replay_census.parse_entity` / `fields` / `read_pos` unchanged.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "tools"))

import replay_census as RC  # noqa: E402
import nav_lock_census as NLC  # noqa: E402

CARD = ((0, -1), (0, 1), (1, 0), (-1, 0))
ACCEPTORS = {"conveyor", "splitter", "core"}
# ⛔ WIRE DIRECTION IS THE PROTOBUF ORDINAL **+1** (0 reserved/unspecified), NOT
# the Python `Direction` ordinal. Established, not assumed: every conveyor in the
# corpus reads 1/3/5/7, which are DIAGONALS under the plain-ordinal reading — and
# CLAUDE.md is explicit that a conveyor may only face a CARDINAL. Discriminated
# by a positive control: "conveyor's output tile holds a friendly acceptor" reads
# 407/465 = 87.5% under +1 against 90/465 = 19.4% under the plain ordinal. A belt
# exists to feed the next thing, so 87.5% is the correct reading and 19.4% is
# noise. (The 12.5% residual is belt heads and pecked-out trunks — consistent
# with the L4 repair defect documented in doctrine.py:1631.)
DIR_DELTA = {1: (0, -1), 3: (1, 0), 5: (0, 1), 7: (-1, 0)}   # N, E, S, W


def walk(path, our_team):
    """-> (harvesters, conveyors) for OUR team.

    harvesters: [(pos, connected_at_build: bool)]
    conveyors:  {pos: direction}   final state
    """
    data = Path(path).read_bytes()
    turn_bufs = [v for n, w, v in RC.fields(data) if n == 3 and w == RC.WIRE_LEN]
    occ = {}          # (x,y) -> (team, kind, direction)
    harvesters = []
    for rnd, tb in enumerate(turn_bufs):
        for _n, _w, upd in RC.fields(tb):
            for unum, _uw, ubuf in RC.fields(upd):
                if unum == 1:                                   # placeEntity
                    for en, _ew, ebuf in RC.fields(ubuf):
                        if en != 1:
                            continue
                        ent = RC.parse_entity(ebuf, rnd)
                        if ent is None or ent.pos is None:
                            continue
                        x, y = ent.pos
                        if ent.kind == "harvester" and ent.team == our_team:
                            conn = any(
                                occ.get((x + dx, y + dy), (None, None, None))[0] == our_team
                                and occ.get((x + dx, y + dy))[1] in ACCEPTORS
                                for dx, dy in CARD)
                            harvesters.append(((x, y), conn))
                        occ[(x, y)] = (ent.team, ent.kind, ent.direction)
                elif unum == 3:                                 # removeEntity
                    pass  # positions are re-emitted on rebuild; final-state only
    conv = {p: d for p, (t, k, d) in occ.items() if t == our_team and k == "conveyor"}
    return harvesters, conv


def side_by_side(conv, same_dir=True):
    """Our conveyor pairs that are adjacent, NOT chained, and (default) FLOWING
    THE SAME WAY — the signature of one band running alongside another.

    ⛔ `same_dir=False` was the first version and it is NOT a parallel-band
    detector: it returned 29,841 pairs against 29,513 conveyors (~1.01 each),
    because a MERGE (two feeders into one trunk) and a CORNER are both adjacent
    and unchained. That measures local network density, not duplication.
    Requiring equal facing excludes merges and corners, which is what makes it
    the thing that was observed on screen.
    """
    pairs = 0
    for (x, y), d in conv.items():
        od = DIR_DELTA.get(d if d is not None else 8, (0, 0))
        out = (x + od[0], y + od[1])
        for dx, dy in CARD:
            n = (x + dx, y + dy)
            if n not in conv or n <= (x, y):
                continue
            nd_raw = conv[n]
            nd = DIR_DELTA.get(nd_raw if nd_raw is not None else 8, (0, 0))
            nout = (n[0] + nd[0], n[1] + nd[1])
            if out == n or nout == (x, y):
                continue                      # chained: one feeds the other
            if same_dir and nd_raw != d:
                continue                      # corner/merge, not a parallel run
            if (dx, dy) == od or (dx, dy) == (-od[0], -od[1]):
                continue                      # in-line, not alongside
            pairs += 1
    return pairs


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ourver", action="append", required=True)
    ap.add_argument("--limit", type=int)
    args = ap.parse_args()

    tot = defaultdict(int)
    print("%-6s %6s %8s %10s %10s   %9s %12s" % (
        "ver", "games", "harv", "connected", "pct", "conveyors", "side-by-side"))
    for v in args.ourver:
        a = defaultdict(int)
        for p, team, _c, _vv in NLC.population(ourver=v, meta=str(NLC.DEFAULT_META),
                                               archive=str(NLC.DEFAULT_ARCHIVE),
                                               limit=args.limit):
            try:
                harv, conv = walk(p, team)
            except Exception:
                continue
            a["games"] += 1
            a["harv"] += len(harv)
            a["conn"] += sum(1 for _, c in harv if c)
            a["conv"] += len(conv)
            sbs = side_by_side(conv)
            a["sbs"] += sbs
            a["games_sbs"] += 1 if sbs else 0
        for k, x in a.items():
            tot[k] += x
        h = a["harv"] or 1
        print("v%-5s %6d %8d %10d %9.1f%%   %9d %12d" % (
            v, a["games"], a["harv"], a["conn"], 100 * a["conn"] / h,
            a["conv"], a["sbs"]))
    h = tot["harv"] or 1
    g = tot["games"] or 1
    print("-" * 72)
    print("%-6s %6d %8d %10d %9.1f%%   %9d %12d" % (
        "TOTAL", tot["games"], tot["harv"], tot["conn"], 100 * tot["conn"] / h,
        tot["conv"], tot["sbs"]))
    print("\nA. harvesters ALREADY CONNECTED when built: %d of %d = %.1f%%"
          % (tot["conn"], tot["harv"], 100 * tot["conn"] / h))
    print("B. side-by-side (adjacent, unchained) conveyor pairs: %d over %d games "
          "= %.2f/game; %d games (%.1f%%) have at least one"
          % (tot["sbs"], tot["games"], tot["sbs"] / g,
             tot["games_sbs"], 100 * tot["games_sbs"] / g))
    print("   conveyors built: %d = %.1f/game" % (tot["conv"], tot["conv"] / g))


if __name__ == "__main__":
    main()
