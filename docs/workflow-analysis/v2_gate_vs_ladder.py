#!/usr/bin/env python3
"""v2 — does the local gate predict ladder Elo?

READ-ONLY on results.tsv and elo_history.tsv. Writes nothing outside this folder.

Design (corrected on the research arm's critique, 2026-08-08): a raw
correlation of gate-number vs realized-window-Elo is uninterpretable, because
BOTH variables are noise-dominated and regression dilution makes a null
consistent with "gate is useless" AND "gate is perfect". So this script:

  1. Reports how many ships can actually be JOINED (gate rows key on bot dir,
     ladder rows key on version number; the mapping only exists where a tape
     row recorded "SHIP - vNN ... (bots/_xxx)").
  2. Estimates measurement variance in X (from each gate's own Wilson width)
     and in Y (from the window's match count and the observed per-match Elo sd).
  3. Reports the attenuation-corrected slope alongside the raw one, and states
     explicitly whether the design can distinguish the two hypotheses at the
     available n. If it cannot, that is the finding.

Usage: python3 v2_gate_vs_ladder.py [results.tsv] [elo_history.tsv]
"""
from __future__ import annotations

import math
import re
import statistics
import sys

SHIP_RE = re.compile(r"\bv(\d+)\b")
DIR_RE = re.compile(r"bots/(_[A-Za-z0-9]+)")


def load_ships(results_path):
    """-> {version:int -> bot_dir} from rows that announce a SHIP."""
    ships = {}
    with open(results_path) as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) < 7:
                continue
            desc = p[6]
            if "SHIP" not in desc.upper():
                continue
            mv, md = SHIP_RE.search(desc), DIR_RE.search(desc)
            if mv and md:
                ships.setdefault(int(mv.group(1)), md.group(1))
    return ships


def load_gates(results_path):
    """-> {bot_dir -> (winrate, ci_lo, ci_hi, n)} from rows with a numeric rate."""
    gates = {}
    with open(results_path) as fh:
        next(fh)
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) < 7:
                continue
            name = p[0]
            try:
                wr, lo, hi, n = float(p[1]), float(p[2]), float(p[3]), int(p[4])
            except ValueError:
                continue
            if n < 60 or hi <= lo:
                continue
            m = re.match(r"(_[A-Za-z0-9]+)", name)
            if m:
                gates.setdefault(m.group(1), (wr, lo, hi, n))
    return gates


def load_windows(elo_path):
    """-> {version:int -> (delta_elo, matches_held)}."""
    rows = []
    with open(elo_path) as fh:
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
    by_m = {}
    for m, r, b in rows:
        by_m[m] = (r, b)
    series = [(m, by_m[m][0], by_m[m][1]) for m in sorted(by_m)]

    span = {}
    for m, r, b in series:
        if b not in span:
            span[b] = [m, r, m, r]
        span[b][2], span[b][3] = m, r
    out = {}
    for b, (m0, r0, m1, r1) in span.items():
        mm = re.fullmatch(r"v(\d+)", b)
        if mm:
            out[int(mm.group(1))] = (r1 - r0, m1 - m0)
    return out, series


def per_match_sd(series):
    d = []
    for (m0, r0, _), (m1, r1, _) in zip(series, series[1:]):
        if m1 > m0:
            step = (r1 - r0) / (m1 - m0)
            d.extend([step] * (m1 - m0))
    return statistics.stdev(d)


def main():
    res = sys.argv[1] if len(sys.argv) > 1 else "results.tsv"
    elo = sys.argv[2] if len(sys.argv) > 2 else "elo_history.tsv"

    ships = load_ships(res)
    gates = load_gates(res)
    windows, series = load_windows(elo)
    sd_match = per_match_sd(series)

    print(f"ship rows found (version -> bot dir): {len(ships)}")
    print(f"gate rows with a usable interval:     {len(gates)}")
    print(f"ladder windows with a delta:          {len(windows)}")
    print(f"per-match ladder Elo sd:              {sd_match:.2f}\n")

    joined = []
    for ver in sorted(ships):
        d = ships[ver]
        if d not in gates or ver not in windows:
            continue
        wr, lo, hi, n = gates[d]
        dy, mh = windows[ver]
        if mh <= 0:
            continue
        joined.append({"ver": ver, "dir": d, "wr": wr, "ci": (hi - lo) / 2,
                       "n": n, "dy": dy, "mh": mh})

    print(f"=== JOINABLE SHIPS: {len(joined)} ===")
    print(f"  {'ver':>4}{'bot dir':>10}{'gate wr':>9}{'+/-':>7}{'n':>6}"
          f"{'ladder d':>10}{'matches':>9}{'elo/match':>11}")
    for j in joined:
        print(f"  {j['ver']:>4}{j['dir']:>10}{j['wr']:>9.3f}"
              f"{100*j['ci']:>6.1f}pp{j['n']:>6}{j['dy']:>+10.1f}"
              f"{j['mh']:>9}{j['dy']/j['mh']:>+11.2f}")

    if len(joined) < 3:
        print("\n  n < 3. No estimate is meaningful. STOP.")
        return

    X = [j["wr"] for j in joined]
    Y = [j["dy"] / j["mh"] for j in joined]          # Elo per ladder match
    n = len(X)
    mx, my = statistics.fmean(X), statistics.fmean(Y)
    sx = statistics.stdev(X) if n > 1 else 0.0
    sy = statistics.stdev(Y) if n > 1 else 0.0
    cov = sum((a - mx) * (b - my) for a, b in zip(X, Y)) / (n - 1)
    r = cov / (sx * sy) if sx and sy else float("nan")

    print(f"\n=== RAW ASSOCIATION ===")
    print(f"  n={n}   r = {r:+.3f}")
    if n > 2 and abs(r) < 1:
        t = r * math.sqrt((n - 2) / (1 - r * r))
        print(f"  t({n-2}) = {t:+.2f}   (|t| > ~2.4 needed for p<0.05 at this n)")
    print(f"  sign agreement (gate>50% & ladder>0, or both opposite): "
          f"{sum(1 for a, b in zip(X, Y) if (a > 0.5) == (b > 0))}/{n}")

    # ---- errors-in-variables -------------------------------------------
    var_x_err = statistics.fmean([(j["ci"] / 1.96) ** 2 for j in joined])
    var_y_err = statistics.fmean([(sd_match ** 2) / j["mh"] for j in joined])
    rel_x = max(0.0, (sx ** 2 - var_x_err)) / (sx ** 2) if sx else 0.0
    rel_y = max(0.0, (sy ** 2 - var_y_err)) / (sy ** 2) if sy else 0.0

    print(f"\n=== MEASUREMENT ERROR / RELIABILITY ===")
    print(f"  X (gate winrate):  observed var {sx**2:.5f}   "
          f"error var {var_x_err:.5f}   reliability {rel_x:.2f}")
    print(f"  Y (Elo per match): observed var {sy**2:.3f}   "
          f"error var {var_y_err:.3f}   reliability {rel_y:.2f}")
    denom = math.sqrt(rel_x * rel_y)
    if denom > 0:
        print(f"  attenuation factor sqrt(rel_x*rel_y) = {denom:.2f}  "
              f"-> disattenuated r = {r/denom:+.3f}")
    else:
        print(f"  attenuation factor = 0 -> a true correlation of ANY size is "
              f"consistent with the observed one. The design cannot answer.")

    print(f"\n=== CAN THIS DESIGN ANSWER ITS QUESTION? ===")
    if n < 10 or denom <= 0.3:
        print(f"  NO. n={n}, attenuation {denom:.2f}. A null here is consistent")
        print(f"  with 'the gate is useless' AND with 'the gate is perfect but")
        print(f"  both measurements are noise-dominated'. Do not read the r.")
    else:
        print(f"  Marginal. Report the disattenuated slope with its interval, "
              f"never the raw r alone.")


if __name__ == "__main__":
    main()
