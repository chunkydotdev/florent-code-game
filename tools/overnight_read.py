#!/usr/bin/env python3
"""OVERNIGHT READ-OUT — pools on the DECLARED denominator, never discards.

⛔ WHY THIS EXISTS, AND IT REPLACES A CONTROL THAT WOULD HAVE THROWN THE NIGHT AWAY
----------------------------------------------------------------------------------
The overnight design carried a rule: *"the read-out REFUSES to pool a shard
without a completion marker."* Sound in intent — silent truncation reads as
"covered everything" — and **catastrophic in practice at these targets.**

Measured on the live run, independently by two lanes: **4.07 s/game at 9 shards**
(side lane got 3.90). At TARGET 5,408 that is **6.12 h against a ~6 h window**.
⇒ **The MODAL outcome is every shard landing at 85–98% and EVERY ONE being
refused. A 95%-successful night converted into a total loss by its own control.**

⇒ **THIS TOOL POOLS PARTIAL SHARDS AND PRINTS THE SHORTFALL.** A shard at
4,900/5,408 is usable with a KNOWN denominator; what is not usable is a shard
whose denominator is unknown. The heartbeat already carries `n TARGET`, so
nothing had to be built to know it.

**WHAT IS STILL REFUSED**, because these are the cases where the denominator is a
lie rather than merely short:
  * `ABORTED_NOWINNER` — the fixture was broken, rows are not games.
  * row count disagreeing with the heartbeat's `n` by >1% — a restart that
    duplicated its prefix, so the sample is skewed to low seeds.
  * a shard whose seat split is off by more than max(2, 1% of n) — seat is worth
    **7.6pp on byte-identical arms**, so an unbalanced shard measures SEAT.
    ⛔ The first threshold was "within 1 game" and it REFUSED HEALTHY SHARDS at
    78/76 mid-run, because the loop plays seats alternately. **A guard that
    refuses good data is as wrong as one that passes bad**, and this repo has
    now produced both kinds in one session.

PART A converts each local win rate to an IMPLIED ELO GAP and compares it to the
opponent-controlled ladder gap. **Registered as a FALSIFIER, not an estimator**
(`docs/PLAN-overnight-2026-08-11.md` Amendment 1): era confounding can bend an
ordering, it cannot invert one.

Usage:  overnight_read.py [--dir scratchpad/overnight]
"""
from __future__ import annotations

import glob
import math
import sys
from collections import Counter
from pathlib import Path

# Opponent-controlled version effects (research, 2c261c8) -- NOT rating snapshots.
# v112 is deliberately absent: zero archived ladder games, so no ladder side.
LADDER = {"_v130loki13": 1686, "_v115dodge": 1600, "_v124loki8": 1609}
LADDER_CI = {"_v130loki13": (1656, 1717), "_v115dodge": (1520, 1681),
             "_v124loki8": (1578, 1641)}


def load(d):
    out = {}
    for f in sorted(glob.glob(f"{d}/*.tsv")):
        sh = Path(f).stem
        rows = [l.split("\t") for l in Path(f).read_text().splitlines()[1:] if l.strip()]
        hb = Path(f"{d}/{sh}.heartbeat")
        n_hb = tgt = None
        status = "NO_HEARTBEAT"
        if hb.exists():
            p = hb.read_text().strip().split("\t")
            if len(p) >= 5:
                n_hb, tgt, status = int(p[1]), int(p[2]), p[4]
        out[sh] = dict(rows=rows, n_hb=n_hb, target=tgt, status=status)
    return out


def summarise(sh, d):
    rows = d["rows"]
    n = len(rows)
    refusals = []
    if d["status"] == "ABORTED_NOWINNER":
        refusals.append("ABORTED_NOWINNER — fixture broken, rows are not games")
    if d["n_hb"] is not None and n and abs(n - d["n_hb"]) > max(1, 0.01 * n):
        refusals.append(f"row count {n} disagrees with heartbeat n={d['n_hb']} "
                        f"— restart likely duplicated a prefix")
    nowin = sum(1 for r in rows if len(r) > 6 and r[6] == "NOWINNER")
    good = [r for r in rows if len(r) > 8 and r[6] in ("T", "C")]
    if not good:
        return dict(sh=sh, n=0, refusals=refusals + ["no scorable rows"])
    W = sum(1 for r in good if r[6] == "T")
    seatA = [r for r in good if r[5] == "A"]
    seatB = [r for r in good if r[5] == "B"]
    # ⛔ TOLERANCE, NOT ZERO. The loop plays seats A,B alternately, so a shard
    # read MID-RUN is legitimately up to a couple of games apart. A refusal
    # threshold of 1 fired on healthy shards at 78/76 — a guard that refuses
    # good data is as wrong as one that passes bad. Proportional, floor 2.
    tol = max(2, int(0.01 * len(good)))
    if abs(len(seatA) - len(seatB)) > tol:
        refusals.append(f"seat imbalance {len(seatA)}/{len(seatB)} (tol {tol}) — "
                        f"seat is worth 7.6pp, an unbalanced shard measures SEAT")
    N = len(good)
    p = W / N
    hw = 1.96 * math.sqrt(0.25 / N)
    kills_t = [int(r[8]) for r in good if r[6] == "T" and r[7] == "core_destroyed" and r[8].isdigit()]
    kills_c = [int(r[8]) for r in good if r[6] == "C" and r[7] == "core_destroyed" and r[8].isdigit()]
    ties = sum(1 for r in good if r[7] == "tiebreak")
    return dict(sh=sh, n=N, target=d["target"], status=d["status"], W=W, p=p, hw=hw,
                seatA=(sum(1 for r in seatA if r[6] == "T"), len(seatA)),
                seatB=(sum(1 for r in seatB if r[6] == "T"), len(seatB)),
                kt=kills_t, kc=kills_c, ties=ties, nowin=nowin, refusals=refusals,
                maps=len({r[3] for r in good}))


def implied_elo(p):
    p = min(max(p, 1e-6), 1 - 1e-6)
    return -400 * math.log10(1 / p - 1)


def main():
    d = "scratchpad/overnight"
    if "--dir" in sys.argv:
        d = sys.argv[sys.argv.index("--dir") + 1]
    data = load(d)
    print("=" * 78)
    print("OVERNIGHT READ-OUT — partial shards POOLED with the shortfall printed")
    print("=" * 78)
    spec = {}
    sp = Path("scratchpad/overnight_spec.txt")
    if sp.exists():
        for line in sp.read_text().splitlines():
            if line.startswith("#") or not line.strip():
                continue
            f = line.split()
            if len(f) >= 3:
                spec[f[0]] = (f[1], f[2])

    for sh in sorted(data):
        s = summarise(sh, data[sh])
        tr, ct = spec.get(sh, ("?", "?"))
        pct = (100.0 * s["n"] / s["target"]) if s.get("target") else float("nan")
        tag = "COMPLETE" if s.get("status") == "COMPLETE" else f"PARTIAL {pct:.1f}%"
        print(f"\n{sh}   {Path(tr).name} vs {Path(ct).name}")
        if s["refusals"]:
            for r in s["refusals"]:
                print(f"   ⛔ REFUSED: {r}")
            if s["n"] == 0:
                continue
        print(f"   n={s['n']}/{s.get('target','?')}  {tag}   maps={s['maps']}  "
              f"NOWINNER={s['nowin']}  tiebreaks={s['ties']}")
        print(f"   WINS {s['W']}/{s['n']} = {s['p']:.2%}   informative band "
              f"{50-s['hw']*100:.2f}%–{50+s['hw']*100:.2f}%")
        a, an = s["seatA"]; b, bn = s["seatB"]
        print(f"   seat A {a}/{an}={a/max(an,1):.1%}   seat B {b}/{bn}={b/max(bn,1):.1%}")
        if s["kt"] and s["kc"]:
            mt = sorted(s["kt"])[len(s["kt"]) // 2]; mc = sorted(s["kc"])[len(s["kc"]) // 2]
            print(f"   median kill round  TREAT {mt}  CTRL {mc}   "
                  f"(kills {len(s['kt'])} vs {len(s['kc'])})")
        v = ("OUTSIDE-BELOW real negative" if s["p"] < 0.5 - s["hw"]
             else "OUTSIDE-ABOVE escalate" if s["p"] > 0.5 + s["hw"]
             else "NO-INFORMATION — back to the pool, NOT demoted")
        print(f"   VERDICT: {v}")

    # ---- PART A: falsifier, not estimator ----
    print("\n" + "=" * 78)
    print("PART A — DOES A LOCAL h2h WIN RATE PREDICT THE LADDER?  (FALSIFIER)")
    print("=" * 78)
    any_a = False
    for sh in sorted(data):
        if not sh.startswith("CAL"):
            continue
        s = summarise(sh, data[sh])
        tr, ct = spec.get(sh, ("?", "?"))
        t, c = Path(tr).name, Path(ct).name
        if s["n"] == 0 or t not in LADDER or c not in LADDER:
            print(f"  {sh}: NOT SCOREABLE (no opponent-controlled ladder estimate)")
            continue
        any_a = True
        loc = implied_elo(s["p"])
        lad = LADDER[t] - LADDER[c]
        print(f"\n  {t} vs {c}   n={s['n']}")
        print(f"    local {s['p']:.2%} ⇒ implied Elo gap {loc:+.1f}")
        print(f"    ladder (opponent-controlled) gap {lad:+.1f}  "
              f"[{LADDER_CI[t][0]}-{LADDER_CI[t][1]} vs {LADDER_CI[c][0]}-{LADDER_CI[c][1]}]")
        print(f"    residual {loc-lad:+.1f} Elo")
        print(f"    ORDERING: local says {t if loc>0 else c} better; "
              f"ladder says {t if lad>0 else c} better  "
              f"⇒ {'AGREE' if (loc>0)==(lad>0) else '⛔ INVERTED'}")
    if any_a:
        print("\n  ⛔ THE PRE-REGISTERED BAR (Amendment 1, before any game ran):")
        print("     ANY inversion, or large unsigned residuals ⇒ LOCAL SCREENS DO NOT")
        print("     PREDICT THE LADDER. Stop screening this week; ship on mechanism.")
        print("     Ordering holds ⇒ FAILED TO FALSIFY. Consistent with predicting.")
        print("     NOT PROOF — and the write-up must say so in those words.")
    print("\n  ⚠ v112 has ZERO archived ladder games, so its pairings are")
    print("    unscoreable at ANY local n. Four of the original six cells cannot")
    print("    be graded and are not reported as weak evidence.")


if __name__ == "__main__":
    main()
