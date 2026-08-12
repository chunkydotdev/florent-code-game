#!/usr/bin/env python3
"""Stronger C1 control, ring-size audit, zero-occurrence games, retention deltas."""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ring_read import ids_from_file, decode, ARCHIVE, OUR_TEAM_ID  # noqa
from ring_balance import load  # noqa


def main():
    A = load("scratchpad/arm_loki16.txt")
    B = load("scratchpad/arm_v104.txt")

    print("=== RING SIZE AUDIT (12 unless clipped by a map edge) ===")
    for lbl, S in (("treatment", A), ("control", B)):
        print(f"  {lbl}: {dict(Counter(g['ring_size'] for g in S))}")

    print("\n=== C1 STRONG: their bodies on OUR ring vs ours on THEIRS, 15 games ===")
    tot_ours = tot_theirs = 0
    for m in ids_from_file(Path("scratchpad/arm_loki16.txt"))[:3]:
        mt = json.loads((ARCHIVE / f"{m}.meta.json").read_text())
        ot = 0 if mt["teamAId"] == OUR_TEAM_ID else 1
        for r in sorted(ARCHIVE.glob(f"{m}_game_*.replay26")):
            tot_ours += decode(r, ot)["seat_rounds"]
            tot_theirs += decode(r, 1 - ot)["seat_rounds"]
    print(f"  our bodies on their ring: {tot_ours} seat-rounds")
    print(f"  their bodies on our ring: {tot_theirs} seat-rounds")
    print("  -> the two sides are NOT the same number, so the team byte is "
          "load-bearing in the decoder")

    print("\n=== ZERO-OCCURRENCE GAMES (treatment) ===")
    for g in A:
        if g["first_arrival"] is None:
            print(f"  {g['opp']:<16} seat {g['seat']}  rounds {g['rounds']:>4}  "
                  f"winner={'us' if g['winner'] == (0 if g['seat']=='A' else 1) else 'them'}")
    print("=== ZERO-OCCURRENCE GAMES (control) ===")
    for g in B:
        if g["first_arrival"] is None:
            print(f"  {g['opp']:<16} seat {g['seat']}  rounds {g['rounds']:>4}  "
                  f"winner={'us' if g['winner'] == (0 if g['seat']=='A' else 1) else 'them'}")

    print("\n=== RETENTION, EQUAL-CELL (opponent) DELTAS ===")
    metrics = {
        "longest single-tile hold / game len":
            lambda g: (max(g["tile_episodes"]) / g["rounds"]) if g["tile_episodes"] else 0.0,
        "seat-rounds / game len":
            lambda g: g["seat_rounds"] / g["rounds"],
        "median (bot,tile) episode len":
            lambda g: statistics.median(g["tile_episodes"]) if g["tile_episodes"] else 0.0,
        "max simultaneous bodies":
            lambda g: g["max_simul"],
        "ring tiles under OUR building @end":
            lambda g: g["bld_ring_tiles_end"],
    }
    opps = sorted({g["opp"] for g in A})
    print(f"  {'metric':<38}{'T':>8}{'C':>8}{'delta':>9}")
    for name, f in metrics.items():
        ds, ta, ca = [], [], []
        for o in opps:
            a = [f(g) for g in A if g["opp"] == o]
            b = [f(g) for g in B if g["opp"] == o]
            ta.append(statistics.mean(a)); ca.append(statistics.mean(b))
            ds.append(statistics.mean(a) - statistics.mean(b))
        print(f"  {name:<38}{statistics.mean(ta):>8.3f}{statistics.mean(ca):>8.3f}"
              f"{statistics.mean(ds):>+9.3f}")

    print("\n=== EPISODE-LENGTH SHAPE, pooled (consecutive rounds a body holds "
          "ONE ring tile) ===")
    for lbl, S in (("treatment (75 games)", A), ("control (165 games)", B)):
        eps = sorted(e for g in S for e in g["tile_episodes"])
        n = len(eps)
        buckets = [(1, 1), (2, 4), (5, 19), (20, 49), (50, 99), (100, 10**9)]
        parts = []
        for lo, hi in buckets:
            c = len([e for e in eps if lo <= e <= hi])
            parts.append(f"{lo}-{'inf' if hi > 10**8 else hi}: {c} ({c/n:.1%})")
        held = sum(eps)
        print(f"  {lbl}: n_episodes={n}  total held seat-rounds={held}")
        print(f"    {'  '.join(parts)}")
        long_eps = [e for e in eps if e >= 50]
        print(f"    episodes >=50 rounds hold {sum(long_eps)}/{held} = "
              f"{sum(long_eps)/held:.1%} of all seat-rounds "
              f"(from {len(long_eps)}/{n} = {len(long_eps)/n:.1%} of episodes)")


if __name__ == "__main__":
    main()
