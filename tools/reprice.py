#!/usr/bin/env python3
"""Re-price a plank battery under BOTH estimators, from its per-game JSON.

Why this exists
---------------
Every row on the s23 scoreboard -- LOKI-3 +0.0, HOME -2.0, FLOOR -0.7,
SITE -6.7, ESCALATE -7.8 -- was recorded as a point estimate with no interval
attached, and the two estimators this repo uses disagree by up to 3x on the
same games:

  POOLED  SE = sqrt(p1(1-p1)/n + p0(1-p0)/n)      treats the arms as unrelated
  PAIRED  SE = sqrt(d)/n,  d = discordant pairs   uses the shared fixture

A paired battery run as `variant vs control on the SAME (map, opponent, seat,
seed)` is a matched design, and scoring it pooled throws away the matching.
The gap matters: on the SITE legs the pooled reading is p=0.26 and the paired
reading is p=0.09 -- "noise" versus "borderline" -- off identical games.

The discordant count is also a result in its OWN right, and on this board it
is the most informative column. A plank whose variant and control win and lose
the same games has not been measured badly; it has been measured, and it does
almost nothing. FLOOR's 0/144 is the clean example.

WHAT IT CANNOT DO. Neither estimator repairs a pool problem. A significant
result against `bots/opp_v*` is a significant result against OUR OWN PRIOR
VERSIONS. Check the pool before reading the p-value.

Input: a JSON list of per-game records carrying at least
  cell (arm name), ourwin (bool), and the fixture keys mp / opp / seat / tb.
Control arm is the cell containing "off" or named "c0" unless --control says so.

Usage:
  .venv/bin/python tools/reprice.py PATH.json [--control CELL] [--label NAME]
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import sys


def p_two_sided(z: float) -> float:
    if z != z:
        return float("nan")
    return math.erfc(abs(z) / math.sqrt(2))


def reprice(rows, control=None, keys=("mp", "opp", "seat", "tb")):
    cells = sorted({r["cell"] for r in rows})
    if control is None:
        guess = [c for c in cells if "off" in c or c == "c0"]
        if len(guess) != 1:
            raise SystemExit(f"cannot pick a control from {cells}; pass --control")
        control = guess[0]
    variants = [c for c in cells if c != control]

    # Group by fixture, keeping DUPLICATES as a list: the same
    # (map, opponent, seat, seed) can legitimately appear more than once, and
    # collapsing to a dict silently drops those games from the pairing.
    grouped = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows:
        grouped[tuple(r.get(k) for k in keys)][r["cell"]].append(bool(r["ourwin"]))

    out = []
    for v in variants:
        pairs = []
        for _key, bycell in grouped.items():
            a, b = bycell.get(v, []), bycell.get(control, [])
            for x, y in zip(a, b):
                pairs.append((x, y))
        n = len(pairs)
        if not n:
            out.append((v, control, 0, 0, *(float("nan"),) * 7))
            continue
        b_only = sum(1 for x, y in pairs if x and not y)
        c_only = sum(1 for x, y in pairs if y and not x)
        disc = b_only + c_only
        delta = (b_only - c_only) / n
        se_pair = math.sqrt(disc) / n if disc else float("nan")
        p1 = sum(1 for x, _ in pairs if x) / n
        p0 = sum(1 for _, y in pairs if y) / n
        se_pool = math.sqrt(p1 * (1 - p1) / n + p0 * (1 - p0) / n)
        z_pair = delta / se_pair if disc else float("nan")
        z_pool = delta / se_pool if se_pool else float("nan")
        n_v = sum(len(bc.get(v, [])) for bc in grouped.values())
        n_c = sum(len(bc.get(control, [])) for bc in grouped.values())
        out.append((v, control, n, disc, delta, se_pair, z_pair, se_pool, z_pool,
                    n_v - n, n_c - n))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--control")
    ap.add_argument("--label", default="")
    args = ap.parse_args()

    rows = json.load(open(args.path))
    if not isinstance(rows, list):
        raise SystemExit("expected a JSON list of per-game records")

    print(f"{args.label or args.path}  ({len(rows)} games)")
    for (v, c, n, disc, delta, sep, zp, seo, zo, drop_v, drop_c) in reprice(rows, args.control):
        print(f"  {v} vs {c}")
        print(f"    paired fixtures {n}   discordant {disc} "
              f"({100 * disc / n:.1f}%)   delta {100 * delta:+.2f}pp")
        print(f"    PAIRED  SE {100 * sep:5.2f}pp  z {zp:+5.2f}  p {p_two_sided(zp):.4f}")
        print(f"    POOLED  SE {100 * seo:5.2f}pp  z {zo:+5.2f}  p {p_two_sided(zo):.4f}")
        if drop_v or drop_c:
            print(f"    UNPAIRED games dropped: {drop_v} from {v}, {drop_c} from {c} "
                  f"-- any headline computed over ALL games includes these")
        if disc == 0:
            print("    NOTE: zero discordant pairs. Either the change never altered a "
                  "game outcome, or the flag was not live. Check control-equivalence "
                  "before reading this as a measured null.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
