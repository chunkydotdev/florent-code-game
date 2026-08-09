#!/usr/bin/env python3
"""Second-pass cuts for the suppression-mechanism test.

  A. SEAT SPLIT -- the ledger for bots that START the round on a collar seat vs
     bots that start it anywhere else.  This is what separates "the collar bots
     are healing" from "every builder stopped building".
  B. FIXED-COHORT TRACE -- prediction 4.  Cohort fixed at r14 by first-damage
     band (<=r13 vs not-yet-damaged-at-r14), then traced across successive
     windows.  A re-sorted cell ("damaged before window") changes membership
     each window and cannot show recovery TIMING.
  C. CONTEMPORANEOUS -- per-round P(a build happens) and P(a core heal happens)
     as a function of CAD's own core HP deficit at round start, pooled over all
     games.  This is the within-round physics, not a landmark.
  D. HEAL-CAP / seat availability sanity + the ledger-partition invariant.

Usage: probe.py <freeze_dir>
"""
from __future__ import annotations

import collections
import csv
import statistics
import sys

from analyse import LEDGER, load, cells, agg, band_of, wsum


def main(d):
    games = load(d)
    P = print

    # ---------------------------------------------------------------- A -----
    P("## A. SEAT SPLIT — collar bots vs everyone else, window r14-40\n")
    a, b = 14, 40
    dm, un = cells(games, a, b)
    for pre, who in (("S_", "ON a collar seat at round start"),
                     ("O_", "OFF the collar at round start")):
        P(f"\n**{who}**\n")
        P("| cell | n games | builder-turns | " + " | ".join(LEDGER) + " |")
        P("| --- | ---: | ---: | " + " | ".join("---:" for _ in LEDGER) + " |")
        for lbl, fs in (("DAMAGED", dm), ("undamaged", un)):
            vals = {k: statistics.mean(
                [wsum(games[f]["rs"], a, b, pre + k) for f in fs])
                for k in LEDGER}
            tot = sum(vals.values())
            P(f"| {lbl} | {len(fs)} | {tot:.1f} | " +
              " | ".join(f"{vals[k]:.2f}" for k in LEDGER) + " |")
            P(f"| {lbl} %turns | | | " +
              " | ".join(f"{100*vals[k]/tot:.1f}%" if tot else "-"
                         for k in LEDGER) + " |")

    # ---------------------------------------------------------------- B -----
    P("\n\n## B. FIXED-COHORT TRACE — prediction 4 (recovery timing)\n")
    P("Cohort fixed at r14. `EARLY` = first CAD core damage <= r13. "
      "`LATE/NEVER` = CAD core still undamaged at r14.\n")
    early = {f for f, g in games.items()
             if g["first_dmg"] is not None and g["first_dmg"] <= 13}
    late = {f for f, g in games.items()
            if g["first_dmg"] is None or g["first_dmg"] >= 14}
    P("| window | cohort | n | builds | core heals | collar seats/rd | "
      "%rd collar≥1 | moves/rd | idle/rd | attacks | bots/rd | med Ti |")
    P("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"
      " ---: | ---: |")
    for lo, hi in ((14, 25), (26, 40), (41, 60), (61, 80), (81, 120),
                   (121, 200), (201, 300)):
        for lbl, coh in (("EARLY", early), ("LATE/NEVER", late)):
            fs = [f for f in coh if games[f]["n"] > hi]
            if not fs:
                continue
            A = agg(games, fs, lo, hi)
            rr = hi - lo + 1
            P(f"| r{lo}-{hi} | {lbl} | {A['n']} | {A['cad_builds']:.2f} | "
              f"{A['cad_healcore_ev']:.2f} | {A['collar_seats']/rr:.3f} | "
              f"{100*A['collar_pct']:.1f}% | {A['cad_moves']/rr:.2f} | "
              f"{A['L_idle']/rr:.2f} | {A['cad_batk']:.2f} | "
              f"{A['bots_start']/rr:.2f} | {A['ti_med']:.0f} |")

    P("\n### The same trace as ratios (EARLY / LATE)\n")
    P("| window | build ratio | core-heal ratio | collar ratio | "
      "Δbuilds (LATE−EARLY) | Δcore heals (EARLY−LATE) |")
    P("| --- | ---: | ---: | ---: | ---: | ---: |")
    for lo, hi in ((14, 25), (26, 40), (41, 60), (61, 80), (81, 120),
                   (121, 200), (201, 300)):
        fe = [f for f in early if games[f]["n"] > hi]
        fl = [f for f in late if games[f]["n"] > hi]
        if not fe or not fl:
            continue
        E, L = agg(games, fe, lo, hi), agg(games, fl, lo, hi)
        rr = hi - lo + 1
        def rat(k, sc=1.0):
            den = L[k] / sc
            return f"{(E[k]/sc)/den:.2f}" if den else "-"
        P(f"| r{lo}-{hi} | {rat('cad_builds')} | {rat('cad_healcore_ev')} | "
          f"{rat('collar_seats')} | {L['cad_builds']-E['cad_builds']:+.2f} | "
          f"{E['cad_healcore_ev']-L['cad_healcore_ev']:+.2f} |")

    # ---------------------------------------------------------------- C -----
    P("\n\n## C. CONTEMPORANEOUS — per-round, by CAD core HP at round start\n")
    buckets = [("500 (full)", 500, 500), ("450-499", 450, 499),
               ("400-449", 400, 449), ("300-399", 300, 399),
               ("200-299", 200, 299), ("100-199", 100, 199),
               ("1-99", 1, 99)]
    acc = collections.defaultdict(lambda: collections.Counter())
    for f, g in games.items():
        prev_hp = 500
        for r in g["rs"]:
            rnd = int(r["rnd"])
            if rnd < 6 or rnd > 300:
                continue
            hpv = prev_hp
            prev_hp = int(r["cad_core_hp"])
            if int(r["bots_start"]) == 0:
                continue
            for name, lo, hi in buckets:
                if lo <= hpv <= hi:
                    c = acc[name]
                    c["n"] += 1
                    c["build"] += 1 if int(r["cad_builds"]) > 0 else 0
                    c["heal"] += 1 if int(r["cad_healcore_ev"]) > 0 else 0
                    c["turns"] += int(r["bots_start"])
                    c["Lbuild"] += int(r["L_build"])
                    c["Lheal"] += int(r["L_heal_core"])
                    c["Lmove"] += int(r["L_move"])
                    c["Lidle"] += int(r["L_idle"])
                    c["seats"] += int(r["collar_seats"])
                    break
    P("| CAD core HP at round start | rounds | P(build) | P(core heal) | "
      "builder-turns | %heal_core | %build | %move | %idle | collar seats/rd |")
    P("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for name, _lo, _hi in buckets:
        c = acc[name]
        if not c["n"]:
            continue
        t = c["turns"]
        P(f"| {name} | {c['n']} | {c['build']/c['n']:.3f} | "
          f"{c['heal']/c['n']:.3f} | {t} | {100*c['Lheal']/t:.1f}% | "
          f"{100*c['Lbuild']/t:.1f}% | {100*c['Lmove']/t:.1f}% | "
          f"{100*c['Lidle']/t:.1f}% | {c['seats']/c['n']:.3f} |")

    # ---------------------------------------------------------------- D -----
    P("\n\n## D. INVARIANTS\n")
    tot = collections.Counter()
    bad = 0
    for f, g in games.items():
        for r in g["rs"]:
            s = sum(int(r["L_" + k]) for k in LEDGER)
            if s != int(r["bots_start"]):
                bad += 1
            for k in LEDGER:
                tot["L_" + k] += int(r["L_" + k])
                tot["S_" + k] += int(r["S_" + k])
                tot["O_" + k] += int(r["O_" + k])
            tot["heal_ev"] += int(r["cad_heal_ev"])
            tot["healcore_ev"] += int(r["cad_healcore_ev"])
            tot["bbuild"] += int(r["cad_bbuild"])
            tot["builds"] += int(r["cad_builds"])
            tot["bots"] += int(r["bots_start"])
            tot["seats"] += int(r["collar_seats"])
    P(f"- ledger partitions builder-turns: {bad} violating rounds of "
      f"{sum(g['n'] for g in games.values())}")
    P(f"- seat + off == total, per label: " +
      ", ".join(f"{k}:{tot['S_'+k]+tot['O_'+k]-tot['L_'+k]}" for k in LEDGER))
    P(f"- builderHeal events {tot['heal_ev']} of which core "
      f"{tot['healcore_ev']} ({100*tot['healcore_ev']/max(tot['heal_ev'],1):.1f}%)")
    P(f"- heal_core ledger turns {tot['L_heal_core']} vs core-heal events "
      f"{tot['healcore_ev']} (a bot may only act once per round)")
    P(f"- builderBuild events {tot['bbuild']}, build-labelled turns "
      f"{tot['L_build']}, all first-placeEntity builds {tot['builds']}")
    P(f"- builder-turns total {tot['bots']}; collar seat-rounds {tot['seats']}")
    for k in LEDGER + ("heal_ev", "healcore_ev", "bbuild", "builds"):
        key = "L_" + k if k in LEDGER else k
        if tot[key] == 0:
            P(f"  !! ALL-ZERO COLUMN: {key}")


if __name__ == "__main__":
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    main(sys.argv[1])
