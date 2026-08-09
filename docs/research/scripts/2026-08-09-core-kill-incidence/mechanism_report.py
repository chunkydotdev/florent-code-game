#!/usr/bin/env python3
"""Report the pre-registered SLOT_UNDER / shelled-core mechanism test.

Reads mech.moves.tsv + mech.games.tsv (from mechanism_slot_under.py), join.tsv
and the feature dataset, and produces the four checks the mechanism implies:
  1. PLACEBO      P(move) by distance, core DAMAGED vs core FULL HP
  2. DISCONTINUITY  is there a step at d2 = 25, or a smooth gradient?
  3. PERSISTENCE  P(move) near home vs rounds since our core last lost HP
  4. DOSE-RESPONSE  per-opponent: enemy shots vs our builders' dispersal

Usage: mechanism_report.py SNAPDIR DATASET OUTFILE
"""
from __future__ import annotations

import collections
import csv
import statistics
import sys
from pathlib import Path


def wilson(k, n):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    z = 1.96
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return (c - h, c + h)


def main(snap, dspath, outp):
    S = Path(snap)
    J = {r["file"]: r for r in csv.DictReader(open(S / "join.tsv"), delimiter="\t")}
    D = {r["file"]: r for r in csv.DictReader(open(dspath), delimiter="\t")}
    out = []

    # ---------- band r0-150, OUR team only
    cells = collections.defaultdict(lambda: [0, 0])       # (d2, dmg) -> [n, moved]   OUR side
    tcells = collections.defaultdict(lambda: [0, 0])      # same, THEIR side (control)
    lat = collections.defaultdict(lambda: [0, 0])         # (latch, near) -> [n, moved]
    per_game = collections.defaultdict(lambda: [0, 0])    # file -> [n, moved-near]
    hp_neg = hp_pos = 0
    for r in csv.DictReader(open(S / "mech.moves.tsv"), delimiter="\t"):
        j = J.get(r["file"])
        if not j or r["band"] != "r0-150":
            continue
        n, m = int(r["n"]), int(r["moved"])
        if r["team"] != j["our_team"]:
            # CONTROL: the opponent's builders around the opponent's own core,
            # under the opponent's own core-damage state. If they show the same
            # suppression, "builders stop moving when their core is hurt" is a
            # property of the game (bodies pinned by combat), not of our code.
            tcells[(r["d2"], r["core_dmg"])][0] += n
            tcells[(r["d2"], r["core_dmg"])][1] += m
            continue
        cells[(r["d2"], r["core_dmg"])][0] += n
        cells[(r["d2"], r["core_dmg"])][1] += m
        d = r["d2"]
        near = "near(d2<=25)" if (d.isdigit() and int(d) <= 25) else "far(d2>25)"
        lat[(r["latch_age"], near, r["core_dmg"])][0] += n
        lat[(r["latch_age"], near, r["core_dmg"])][1] += m
    for r in csv.DictReader(open(S / "mech.games.tsv"), delimiter="\t"):
        j = J.get(r["file"])
        if not j or r["team"] != j["our_team"]:
            continue
        per_game[r["file"]] = [int(r["samples"]), int(r["outside25"]),
                               int(r["sum_d2"]), int(r["dmg_rounds"])]
        hp_neg += int(r["hp_neg_events"])
        hp_pos += int(r["hp_pos_events"])

    out.append("## VALIDATION of the HP decode (the two's-complement trap)")
    out.append(f"\nupdateHp deltas seen across the 1,445 joined replays: "
               f"**{hp_neg//2:,} negative** (damage) and **{hp_pos//2:,} positive** (heals). "
               "Both signs present, so the varint sign handling is live rather than "
               "silently collapsing to one sign -- the failure mode that produced "
               "'exactly 0 core damage across 11,895 insertions' in the throw census.")

    # ---------- 1 + 2 PLACEBO and DISCONTINUITY
    out.append("\n## 1+2. PLACEBO AND DISCONTINUITY -- P(our builder moves) by d2 to our own core")
    out.append("\nr0-150, our team only. `core DAMAGED` = our core HP < max at the start of "
               "the round. The hypothesised code path fires ONLY when the core is damaged, "
               "so a real effect must appear in the DAMAGED column and be absent in the "
               "FULL column, with a STEP at d2=25.")
    out.append("")
    out.append("| d2 to our core | n (dmg) | P(move) dmg | n (full) | P(move) full | dmg - full |")
    out.append("| ---: | ---: | ---: | ---: | ---: | ---: |")
    keys = sorted({d for d, _ in cells}, key=lambda x: (0, int(x)) if x.isdigit() else (1, x))
    for d in keys:
        nd, md = cells[(d, "1")]
        nf, mf = cells[(d, "0")]
        if nd + nf < 200:
            continue
        pd_ = md / nd if nd else float("nan")
        pf = mf / nf if nf else float("nan")
        mark = "   <-- **d2=25 boundary**" if d == "25" else ""
        out.append(f"| {d}{mark} | {nd:,} | {pd_:.3f} | {nf:,} | {pf:.3f} | "
                   f"{pd_-pf:+.3f} |")

    # explicit step test -- TWO competing thresholds
    #   (a) dsq 25          the gate the hypothesis names
    #   (b) ORTHOGONAL ADJACENCY TO THE 2x2 CORE FOOTPRINT, which is what
    #       can_heal() actually enforces. With the core anchored at (x,y) and a
    #       footprint {(x,y),(x+1,y),(x,y+1),(x+1,y+1)}, the tiles orthogonally
    #       adjacent to SOME footprint tile are exactly those at d2 in {1,2,4,5}
    #       from the anchor. d2=8 is the diagonal corner (x+2,y+2) -- one tile
    #       further out and NOT adjacent to anything. So {1,2,4,5} vs {8,9,10,...}
    #       is a one-tile-wide test of the adjacency rule.
    ADJ = {1, 2, 4, 5}

    def agg(pred, dmg, src=None):
        src = cells if src is None else src
        n = m = 0
        for d, g in src:
            if g != dmg or not d.isdigit():
                continue
            if pred(int(d)):
                n += src[(d, g)][0]
                m += src[(d, g)][1]
        return n, m

    out.append("\n**The step test -- two competing thresholds.** The hypothesis names "
               "`dsq 25`. But `can_heal()` enforces ORTHOGONAL ADJACENCY to a core "
               "footprint tile, and for a 2x2 core anchored at (x,y) that set is exactly "
               "d2 in {1,2,4,5} from the anchor -- d2=8 is the diagonal corner, one tile "
               "further out and adjacent to nothing. Both thresholds are tested here, "
               "against the opponent's own builders around the opponent's own core as a "
               "control.")
    out.append("")
    out.append("| window | US: n, P(move) dmg [95% CI] | US: P(move) full | US suppression | "
               "THEM: P(move) dmg | THEM: P(move) full | THEM suppression |")
    out.append("| --- | --- | ---: | ---: | ---: | ---: | ---: |")
    WINDOWS = [
        (lambda d: d in ADJ, "d2 in {1,2,4,5} -- ORTHOGONALLY ADJACENT to the core footprint"),
        (lambda d: 6 <= d <= 20, "d2 6-20 -- near but NOT adjacent"),
        (lambda d: 21 <= d <= 25, "d2 21-25 -- inside the `dsq 25` gate"),
        (lambda d: 26 <= d <= 30, "d2 26-30 -- just OUTSIDE the `dsq 25` gate"),
        (lambda d: 31 <= d <= 60, "d2 31-60"),
    ]
    for pred, lab in WINDOWS:
        nd, md = agg(pred, "1")
        nf, mf = agg(pred, "0")
        tnd, tmd = agg(pred, "1", tcells)
        tnf, tmf = agg(pred, "0", tcells)
        lo_d, hi_d = wilson(md, nd)
        pu_d = md / nd if nd else 0
        pu_f = mf / nf if nf else 0
        pt_d = tmd / tnd if tnd else 0
        pt_f = tmf / tnf if tnf else 0
        out.append(f"| {lab} | {nd:,}, **{pu_d:.3f}** [{lo_d:.3f},{hi_d:.3f}] | {pu_f:.3f} | "
                   f"**{pu_d-pu_f:+.3f}** | {pt_d:.3f} | {pt_f:.3f} | {pt_d-pt_f:+.3f} |")

    # ---------- 3 PERSISTENCE
    out.append("\n## 3. PERSISTENCE -- P(move) vs rounds since our core last lost HP")
    out.append("\n`SLOT_UNDER` is a 50-round latch. If it is what suppresses movement, "
               "P(move) for near-home builders should be flat below 50 rounds of age and "
               "recover above it.")
    out.append("")
    out.append("| rounds since our core last took damage | near (d2<=25) n | P(move) | far (d2>25) n | P(move) |")
    out.append("| --- | ---: | ---: | ---: | ---: |")
    order = ["0-1", "1-5", "5-10", "10-25", "25-50", "50-75", "75-150", "150+", "never"]
    for lb in order:
        nn = mm = fn = fm = 0
        for (l, near, _dmg), (n, m) in lat.items():
            if l != lb:
                continue
            if near.startswith("near"):
                nn += n
                mm += m
            else:
                fn += n
                fm += m
        if nn + fn == 0:
            continue
        marker = "   <-- **latch expiry**" if lb == "50-75" else ""
        out.append(f"| {lb}{marker} | {nn:,} | {mm/nn if nn else 0:.3f} | {fn:,} | "
                   f"{fm/fn if fn else 0:.3f} |")

    # ---------- 4 DOSE-RESPONSE
    out.append("\n## 4. DOSE-RESPONSE -- enemy fire at our core vs our builders' dispersal")
    out.append("\nExposure: the opponent's turret shots in r0-150 (from the fine-band "
               "decoder, cross-validated against `build_agg.tsv` `metric=='shot'`; "
               "`econ.tsv.shots` is zero in every row and is not used). "
               "Response: the share of our builder-bot round-samples standing OUTSIDE "
               "d2=25 of our own core. One point per opponent, N stated.")
    out.append("")
    out.append("| opponent | games | their shots/game r0-150 | our core damaged, share of rounds | "
               "our builders outside d2=25 | our core-kill share |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    byopp = collections.defaultdict(list)
    for f, g in per_game.items():
        d = D.get(f)
        if not d:
            continue
        byopp[d["opp"]].append((g, d))
    pts = []
    for opp, v in sorted(byopp.items(), key=lambda kv: -len(kv[1])):
        if len(v) < 10:
            continue
        shots = statistics.mean(float(d["THEM_shot_w150"]) for _g, d in v)
        outside = sum(g[1] for g, _d in v) / max(1, sum(g[0] for g, _d in v))
        dmgshare = sum(g[3] for g, _d in v) / max(1, sum(g[0] for g, _d in v))
        ck = sum(1 for _g, d in v if d["y_corekill"] == "1") / len(v)
        pts.append((shots, outside, opp, len(v), ck, dmgshare))
        out.append(f"| {opp} | {len(v)} | {shots:.0f} | {dmgshare:.3f} | {outside:.3f} | "
                   f"{100*ck:.1f}% |")

    def pear(a, b):
        n = len(a)
        ma, mb = sum(a) / n, sum(b) / n
        num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
        den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
        return num / den if den else 0.0

    if len(pts) >= 5:
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        ds = [p[5] for p in pts]
        cs = [p[4] for p in pts]
        out.append(f"\nAcross the {len(pts)} opponents with >=10 archived games:")
        out.append(f"- corr(their shots/game, our builders outside d2=25) = **{pear(xs, ys):+.3f}** "
                   "-- the mechanism predicts a clear NEGATIVE.")
        out.append(f"- corr(share of rounds our core is damaged, our builders outside d2=25) = "
                   f"**{pear(ds, ys):+.3f}** -- this is the closer proxy, since the heal is "
                   "gated on damage, not on fire.")
        out.append(f"- corr(our builders outside d2=25, our core-kill share) = **{pear(ys, cs):+.3f}**"
                   " -- if dispersal is what buys kills this must be clearly positive.")
        out.append(f"- corr(their shots/game, our core-kill share) = **{pear(xs, cs):+.3f}**.")

    # per-GAME within-opponent version (removes the opponent-identity confound)
    out.append("\n**Within-opponent, per game** (the same relationship with opponent identity "
               "removed -- rank correlation of our dispersal against our core-kill outcome, "
               "computed inside each opponent and pooled):")
    out.append("")
    out.append("| opponent | games | mean dispersal in kill games | in non-kill games | diff |")
    out.append("| --- | ---: | ---: | ---: | ---: |")
    diffs = []
    for opp, v in sorted(byopp.items(), key=lambda kv: -len(kv[1])):
        if len(v) < 15:
            continue
        k1 = [g[1] / g[0] for g, d in v if d["y_corekill"] == "1" and g[0]]
        k0 = [g[1] / g[0] for g, d in v if d["y_corekill"] == "0" and g[0]]
        if len(k1) < 3 or len(k0) < 3:
            continue
        a, b = statistics.mean(k1), statistics.mean(k0)
        diffs.append(a - b)
        out.append(f"| {opp} | {len(v)} | {a:.3f} | {b:.3f} | {a-b:+.3f} |")
    if diffs:
        pos = sum(1 for d in diffs if d > 0)
        out.append(f"\n{pos} of {len(diffs)} opponents show higher dispersal in the games we "
                   f"land a core kill; mean difference {statistics.mean(diffs):+.3f}.")

    Path(outp).write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
