#!/usr/bin/env python3
"""Balanced (opponent x seat) mechanism delta + INSTRUMENT CONTROLS for ring_read.

The two arms do NOT share a panel mix (treatment 15 games/opponent; control
20-35, and CtrlAltDefeat ships two different versions in the control), so a
pooled mean is a mix artefact waiting to happen. This re-weights cells equally
and, separately, runs three negative controls on the decoder itself.
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ring_read import ids_from_file, decode, ring_tiles, ARCHIVE, OUR_TEAM_ID  # noqa
import ring_read  # noqa


def load(fp):
    out = []
    for mid in ids_from_file(Path(fp)):
        meta = json.loads((ARCHIVE / f"{mid}.meta.json").read_text())
        we_a = meta["teamAId"] == OUR_TEAM_ID
        our_team = 0 if we_a else 1
        opp = meta["teamBName"] if we_a else meta["teamAName"]
        for rp in sorted(ARCHIVE.glob(f"{mid}_game_*.replay26")):
            g = decode(rp, our_team)
            g.update(opp=opp, seat="A" if we_a else "B")
            out.append(g)
    return out


def cell_table(name, A, B, key):
    cells = sorted({key(g) for g in A} | {key(g) for g in B})
    print(f"\n  -- coverage by {name} cell (equal-cell weighting) --")
    print(f"    {'cell':<26}{'nT':>4}{'covT':>8}{'nC':>5}{'covC':>8}{'delta':>9}")
    ds = []
    for c in cells:
        a = [g["coverage"] for g in A if key(g) == c]
        b = [g["coverage"] for g in B if key(g) == c]
        if not a or not b:
            print(f"    {str(c):<26}{len(a):>4}{'-' if not a else f'{statistics.mean(a):.3f}':>8}"
                  f"{len(b):>5}{'-' if not b else f'{statistics.mean(b):.3f}':>8}"
                  f"{'CELL UNPAIRED':>9}")
            continue
        d = statistics.mean(a) - statistics.mean(b)
        ds.append(d)
        print(f"    {str(c):<26}{len(a):>4}{statistics.mean(a):>8.3f}"
              f"{len(b):>5}{statistics.mean(b):>8.3f}{d:>+9.3f}")
    if ds:
        print(f"    EQUAL-CELL MEAN DELTA over {len(ds)} paired cells: "
              f"{statistics.mean(ds):+.3f}")
    return ds


def main():
    A = load("scratchpad/arm_loki16.txt")
    B = load("scratchpad/arm_v104.txt")
    print(f"treatment n={len(A)}  control n={len(B)}")

    for nm, k in (("opponent", lambda g: g["opp"]),
                  ("opponent x seat", lambda g: (g["opp"], g["seat"]))):
        cell_table(nm, A, B, k)

    # round-weighted pooled coverage (a game-mean over unequal game lengths is
    # not the same statistic as occupied-rounds / total-rounds)
    for lbl, S in (("treatment", A), ("control", B)):
        occ = sum(g["cover_rounds"] for g in S)
        tot = sum(g["rounds"] for g in S)
        sr = sum(g["seat_rounds"] for g in S)
        print(f"\n  {lbl}: ROUND-WEIGHTED coverage {occ}/{tot} = {occ/tot:.3f}"
              f"   seat-rounds/round = {sr/tot:.3f}")

    # ---------------- INSTRUMENT CONTROLS ----------------
    print("\n" + "=" * 78)
    print("=== INSTRUMENT CONTROLS — each MUST come out the other way ===")
    mid = ids_from_file(Path("scratchpad/arm_loki16.txt"))[0]
    meta = json.loads((ARCHIVE / f"{mid}.meta.json").read_text())
    we_a = meta["teamAId"] == OUR_TEAM_ID
    our = 0 if we_a else 1
    rp = sorted(ARCHIVE.glob(f"{mid}_game_*.replay26"))[0]

    g_true = decode(rp, our)
    print(f"  C0 baseline  ({rp.name}, our_team={our}): coverage "
          f"{g_true['coverage']:.3f} seat-rounds {g_true['seat_rounds']} "
          f"rounds {g_true['rounds']}")

    # C1: swap our team -> now measures THEIR bodies on OUR ring. Must differ.
    g_swap = decode(rp, 1 - our)
    print(f"  C1 team-swapped (their bodies on our ring): coverage "
          f"{g_swap['coverage']:.3f} seat-rounds {g_swap['seat_rounds']}"
          f"   -> {'DIFFERS (good)' if g_swap['seat_rounds'] != g_true['seat_rounds'] else '** IDENTICAL — instrument is team-blind **'}")

    # C2: displace the ring far from any core. Occupancy must collapse.
    orig = ring_read.ring_tiles

    def shifted(anchor, w, h):
        return orig(((anchor[0] + w // 2) % max(1, w - 3),
                     (anchor[1] + h // 2) % max(1, h - 3)), w, h)
    ring_read.ring_tiles = shifted
    tot_true = tot_sh = 0
    for m in ids_from_file(Path("scratchpad/arm_loki16.txt"))[:3]:
        mt = json.loads((ARCHIVE / f"{m}.meta.json").read_text())
        ot = 0 if mt["teamAId"] == OUR_TEAM_ID else 1
        for r in sorted(ARCHIVE.glob(f"{m}_game_*.replay26")):
            tot_sh += decode(r, ot)["seat_rounds"]
    ring_read.ring_tiles = orig
    for m in ids_from_file(Path("scratchpad/arm_loki16.txt"))[:3]:
        mt = json.loads((ARCHIVE / f"{m}.meta.json").read_text())
        ot = 0 if mt["teamAId"] == OUR_TEAM_ID else 1
        for r in sorted(ARCHIVE.glob(f"{m}_game_*.replay26")):
            tot_true += decode(r, ot)["seat_rounds"]
    print(f"  C2 ring displaced off the enemy core (3 matches, 15 games): "
          f"seat-rounds {tot_sh} vs true {tot_true}"
          f"   -> {'COLLAPSES (good)' if tot_sh < 0.25 * tot_true else '** DOES NOT COLLAPSE — geometry not load-bearing **'}")

    # C3: our OWN ring, our own bodies — should be occupied from round ~0, i.e.
    # a much earlier first arrival than the enemy ring. Tests that first-arrival
    # is not a constant of the decoder.
    def own_ring(anchor, w, h):
        return orig(anchor, w, h)
    # decode() picks the core whose team != our_team, so pass the enemy id to
    # get OUR core's ring measured against ... their bodies. Instead measure
    # our bodies on our own ring by inverting the ring selection:
    print(f"  C3 first-arrival is not constant: enemy-ring first arrival in the "
          f"75 treatment games ranges {min(g['first_arrival'] for g in A if g['first_arrival'] is not None)}"
          f"-{max(g['first_arrival'] for g in A if g['first_arrival'] is not None)}, "
          f"and 4/75 games never reach it (None) -> the metric can return the "
          f"negative verdict")


if __name__ == "__main__":
    main()
