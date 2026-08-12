#!/usr/bin/env python3
"""Estimator sensitivity + match-clustered bootstrap for the coverage delta,
and a split on the clipped-ring map."""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ring_read import ids_from_file, decode, ARCHIVE, OUR_TEAM_ID  # noqa


def load(fp):
    out = []
    for mid in ids_from_file(Path(fp)):
        meta = json.loads((ARCHIVE / f"{mid}.meta.json").read_text())
        we_a = meta["teamAId"] == OUR_TEAM_ID
        ot = 0 if we_a else 1
        opp = meta["teamBName"] if we_a else meta["teamAName"]
        for rp in sorted(ARCHIVE.glob(f"{mid}_game_*.replay26")):
            g = decode(rp, ot)
            g.update(opp=opp, seat="A" if we_a else "B", mid=mid)
            out.append(g)
    return out


def game_mean(S):
    return statistics.mean(g["coverage"] for g in S)


def round_weighted(S):
    return sum(g["cover_rounds"] for g in S) / sum(g["rounds"] for g in S)


def equal_cell(A, B, key):
    ds = []
    for c in sorted({key(g) for g in A} & {key(g) for g in B}):
        a = [g["coverage"] for g in A if key(g) == c]
        b = [g["coverage"] for g in B if key(g) == c]
        ds.append(statistics.mean(a) - statistics.mean(b))
    return statistics.mean(ds)


def main():
    A = load("scratchpad/arm_loki16.txt")
    B = load("scratchpad/arm_v104.txt")

    print("=== THE MECHANISM BAR DEPENDS ON THE ESTIMATOR (prereg names none) ===")
    print(f"  bar: treatment coverage - control coverage >= +0.080")
    ests = {
        "game-mean (each game 1 vote)": (game_mean(A), game_mean(B)),
        "round-weighted (occupied/total rounds)": (round_weighted(A), round_weighted(B)),
    }
    for k, (a, b) in ests.items():
        d = a - b
        print(f"  {k:<42}{a:.3f} - {b:.3f} = {d:+.3f}  "
              f"{'MEETS' if d >= 0.08 else 'MISSES'}")
    for nm, key in (("equal-cell by opponent", lambda g: g["opp"]),
                    ("equal-cell by opponent x seat", lambda g: (g["opp"], g["seat"]))):
        d = equal_cell(A, B, key)
        print(f"  {nm:<42}{'':>17}{d:+.3f}  {'MEETS' if d >= 0.08 else 'MISSES'}")

    print("\n=== MATCH-CLUSTERED BOOTSTRAP (games within a match are one draw) ===")
    ma = defaultdict(list); mb = defaultdict(list)
    for g in A: ma[g["mid"]].append(g)
    for g in B: mb[g["mid"]].append(g)
    ka, kb = list(ma), list(mb)
    rng = random.Random(20260810)
    ds = []
    for _ in range(4000):
        sa = [g for k in rng.choices(ka, k=len(ka)) for g in ma[k]]
        sb = [g for k in rng.choices(kb, k=len(kb)) for g in mb[k]]
        ds.append(game_mean(sa) - game_mean(sb))
    ds.sort()
    lo, hi = ds[int(.025 * len(ds))], ds[int(.975 * len(ds))]
    print(f"  game-mean delta {game_mean(A)-game_mean(B):+.3f}  "
          f"95% CI [{lo:+.3f}, {hi:+.3f}]  "
          f"(clusters: {len(ka)} treatment matches vs {len(kb)} control matches)")
    print(f"  P(delta >= +0.080) under the bootstrap = "
          f"{len([d for d in ds if d >= 0.08])/len(ds):.2f}")
    print(f"  P(delta > 0)                          = "
          f"{len([d for d in ds if d > 0])/len(ds):.2f}")

    print("\n=== CLIPPED-RING SPLIT (ring_size 5 = a corner-anchored enemy core) ===")
    for lbl, S in (("treatment", A), ("control", B)):
        for rs in sorted({g["ring_size"] for g in S}):
            gs = [g for g in S if g["ring_size"] == rs]
            print(f"  {lbl:<10} ring_size {rs:>2}: n={len(gs):>3} "
                  f"coverage {game_mean(gs):.3f}  "
                  f"occurrence {len([g for g in gs if g['first_arrival'] is not None])}/{len(gs)}")
    print("  (ring_size 5 games are the same map in both arms -- one of the five "
          "pinned maps anchors both cores in a corner, so its 'twelve-tile ring' "
          "is five tiles. Reported, not corrected for.)")


if __name__ == "__main__":
    main()
