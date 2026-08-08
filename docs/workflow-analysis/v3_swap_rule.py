#!/usr/bin/env python3
"""v3 — operating characteristics of the slot-swap rule.

READ-ONLY on elo_history.tsv. Writes nothing outside this folder.

The rule (ship-gate.md): rolling last-5 net Elo, ARMS at holder-match >= 8;
<= 0 frees the slot.

Two questions, both answerable without a counterfactual:

  A. OBSERVED — how often does a window that crosses the trigger recover on
     its own, with no swap? If spontaneous recovery is common the trigger is
     mostly firing on noise; if rare, the rule is load-bearing.
     (Research arm's reframing; the answerable version of "error rate".)

  B. SIMULATED — given the empirical per-match Elo increment distribution,
     what fraction of a TRULY NEUTRAL holder's tenures trigger by match 8,
     12, 20, 30? That is the false-positive rate, exactly computable by
     bootstrap from observed increments with the mean removed.

Usage: python3 v3_swap_rule.py [elo_history.tsv]
"""
from __future__ import annotations

import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ARM_AT = 8       # rule arms at holder-match >= 8
WINDOW = 5       # rolling last-5
TRIALS = 200_000


def load(path):
    """-> ordered [(matches, rating, active_bot)], last row wins per matches."""
    rows = []
    with open(path) as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) < 4:
                continue
            try:
                rating, matches = float(p[1]), int(p[2])
            except ValueError:
                continue
            rows.append((matches, rating, p[3]))
    # last row wins for a given match count (tape corrections supersede)
    by_m = {}
    for m, r, b in rows:
        by_m[m] = (r, b)
    return [(m, by_m[m][0], by_m[m][1]) for m in sorted(by_m)]


def increments(series):
    """Per-match Elo increments, attributed to the later row's holder."""
    out = []
    for (m0, r0, _), (m1, r1, b1) in zip(series, series[1:]):
        dm = m1 - m0
        if dm <= 0:
            continue
        step = (r1 - r0) / dm          # spread multi-match gaps evenly
        for _ in range(dm):
            out.append((step, b1))
    return out


def tenures(incs):
    """-> {bot: [increments in order]} for the holder's own matches."""
    t = defaultdict(list)
    for d, b in incs:
        t[b].append(d)
    return t


def trigger_points(seq):
    """Indices i (0-based, holder-match count i+1) where the rule fires."""
    hits = []
    for i in range(len(seq)):
        if i + 1 < ARM_AT:
            continue
        if sum(seq[max(0, i + 1 - WINDOW):i + 1]) <= 0:
            hits.append(i)
    return hits


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "elo_history.tsv"
    series = load(path)
    incs = increments(series)
    ten = tenures(incs)

    all_d = [d for d, _ in incs]
    print(f"tape: {len(series)} distinct match-stamps, "
          f"matches {series[0][0]}..{series[-1][0]}, "
          f"{len(all_d)} reconstructed per-match increments")
    print(f"per-match Elo increment: mean {statistics.fmean(all_d):+.2f}  "
          f"sd {statistics.stdev(all_d):.2f}  "
          f"min {min(all_d):+.1f}  max {max(all_d):+.1f}")

    long = {b: s for b, s in ten.items() if len(s) >= ARM_AT}
    print(f"\nholders with >= {ARM_AT} matches (rule can arm): {len(long)} of {len(ten)}")

    # ---- A. observed spontaneous recovery -------------------------------
    print(f"\n=== A. OBSERVED: do triggered windows recover without a swap? ===")
    n_trig_tenures = 0
    events = []
    for b, seq in sorted(long.items()):
        hits = trigger_points(seq)
        if not hits:
            continue
        n_trig_tenures += 1
        first = hits[0]
        after = seq[first + 1:]
        # recovery = rolling-5 returns > 0 later in the SAME tenure
        recovered = any(
            sum(seq[max(0, i + 1 - WINDOW):i + 1]) > 0
            for i in range(first + 1, len(seq)) if i + 1 >= ARM_AT
        )
        events.append({
            "bot": b, "n": len(seq), "first_trigger_at": first + 1,
            "n_triggers": len(hits), "recovered": recovered,
            "elo_after_trigger": sum(after), "matches_after": len(after),
        })

    print(f"  {n_trig_tenures} of {len(long)} armed tenures crossed the trigger "
          f"at least once")
    rec = [e for e in events if e["recovered"]]
    print(f"  SPONTANEOUS RECOVERY (rolling-5 returns >0, same holder, no swap): "
          f"{len(rec)}/{len(events)}"
          + (f" = {100*len(rec)/len(events):.0f}%" if events else ""))
    tail = [e["elo_after_trigger"] for e in events if e["matches_after"] > 0]
    if tail:
        print(f"  net Elo from first trigger to end of tenure: "
              f"mean {statistics.fmean(tail):+.1f}, "
              f"median {statistics.median(tail):+.1f}, "
              f"{sum(1 for t in tail if t > 0)}/{len(tail)} positive")
    print(f"\n  {'holder':<8}{'n':>4}{'1st trig':>9}{'#trig':>7}{'recov':>7}"
          f"{'elo after':>11}{'matches after':>15}")
    for e in sorted(events, key=lambda x: x["bot"]):
        print(f"  {e['bot']:<8}{e['n']:>4}{e['first_trigger_at']:>9}"
              f"{e['n_triggers']:>7}{'yes' if e['recovered'] else 'no':>7}"
              f"{e['elo_after_trigger']:>+11.1f}{e['matches_after']:>15}")

    # ---- B. simulated false-positive rate -------------------------------
    print(f"\n=== B. SIMULATED: false-positive rate on a TRULY NEUTRAL holder ===")
    mu = statistics.fmean(all_d)
    centred = [d - mu for d in all_d]     # true edge = 0 by construction
    print(f"  bootstrap from {len(centred)} observed increments, mean removed "
          f"(sd {statistics.stdev(centred):.2f}); {TRIALS:,} trials")
    rng = random.Random(20260808)
    print(f"\n  {'tenure length':>14}{'P(trigger fires)':>20}")
    for L in (8, 10, 12, 16, 20, 30, 50):
        fired = 0
        for _ in range(TRIALS):
            seq = [rng.choice(centred) for _ in range(L)]
            if trigger_points(seq):
                fired += 1
        print(f"  {L:>14}{100*fired/TRIALS:>19.1f}%")

    # true-edge sweep: how well does it discriminate?
    print(f"\n  discrimination at a 20-match tenure "
          f"(P the rule frees the slot, by TRUE per-match edge):")
    print(f"  {'true edge/match':>16}{'~Elo over 20':>14}{'P(fires)':>11}")
    for edge in (-3.0, -2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0, 3.0):
        fired = 0
        for _ in range(TRIALS // 4):
            seq = [rng.choice(centred) + edge for _ in range(20)]
            if trigger_points(seq):
                fired += 1
        print(f"  {edge:>+16.1f}{edge*20:>+14.0f}"
              f"{100*fired/(TRIALS//4):>10.1f}%")


if __name__ == "__main__":
    main()
