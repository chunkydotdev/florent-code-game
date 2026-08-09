#!/usr/bin/env python3
"""The suppression-mechanism test: what are CAD's builders doing instead?

LANDMARK DESIGN, inherited unchanged from the lockout cut.  CAD's opening is a
byte-identical script, so a within-game before/after contrast measures the
script, not the damage.  Every cell here compares the SAME ABSOLUTE ROUND WINDOW
between games where CAD's core had already taken damage before the window opened
and games where it had not.  Games that did not reach the window's end are
excluded from that cell, so every game in a cell contributes the same number of
rounds.

Usage: analyse.py <freeze_dir>
"""
from __future__ import annotations

import collections
import csv
import statistics
import sys

LEDGER = ("heal_core", "heal_bldg", "heal_bot", "heal_other",
          "build", "attack", "thrown", "move", "died", "idle")

SUMS = (["cad_builds", "cad_bbuild", "cad_heal_ev", "cad_healcore_ev",
         "cad_batk", "cad_batk_core", "cad_moves", "cad_thrown_ev",
         "born", "died", "collar_seats", "collar_bots", "bots_start",
         "cad_bldg_lost", "cad_conv_lost", "cad_harv_lost", "cad_turret_lost",
         "b_conveyor", "b_harvester", "b_barrier", "b_builder_bot",
         "b_gunner", "b_sentinel", "b_launcher", "b_splitter",
         "cad_core_dmg", "out_n", "tled_n"]
        + ["L_" + k for k in LEDGER])

BANDS = [("<=r13", 0, 13), ("r14-25", 14, 25), ("r26+", 26, 10 ** 9)]


def load(d):
    pop = {r["file"]: r for r in csv.DictReader(open(f"{d}/cad_population.tsv"),
                                                delimiter="\t")}
    rounds = collections.defaultdict(list)
    for r in csv.DictReader(open(f"{d}/mech_rounds.tsv"), delimiter="\t"):
        rounds[r["file"]].append(r)
    games = {}
    for f, rs in rounds.items():
        rs.sort(key=lambda r: int(r["rnd"]))
        fd = next((int(r["rnd"]) for r in rs if int(r["cad_core_dmg"]) > 0), None)
        games[f] = {"rs": rs, "first_dmg": fd, "n": len(rs), "pop": pop[f],
                    "died": int(rs[-1]["cad_core_hp"]) <= 0}
    return games


def band_of(fd):
    if fd is None:
        return "never"
    for name, lo, hi in BANDS:
        if lo <= fd <= hi:
            return name
    return "?"


def wsum(rs, a, b, key):
    return sum(int(r[key]) for r in rs if a <= int(r["rnd"]) <= b)


def wmed(rs, a, b, key):
    v = [int(r[key]) for r in rs if a <= int(r["rnd"]) <= b]
    return statistics.median(v) if v else 0


def cells(games, a, b, subset=None):
    """Split games reaching round b into damaged-before-a and undamaged-at-a."""
    dmg, und = [], []
    for f, g in games.items():
        if subset is not None and f not in subset:
            continue
        if g["n"] <= b:
            continue
        fd = g["first_dmg"]
        (dmg if (fd is not None and fd < a) else und).append(f)
    return dmg, und


def agg(games, files, a, b):
    n = len(files)
    o = {"n": n, "rounds": b - a + 1}
    if not n:
        return o
    for k in SUMS:
        vals = [wsum(games[f]["rs"], a, b, k) for f in files]
        o[k] = statistics.mean(vals)
        o[k + "_med"] = statistics.median(vals)
    o["zero_build"] = sum(1 for f in files
                          if wsum(games[f]["rs"], a, b, "cad_builds") == 0)
    o["ti_med"] = statistics.median(
        [wmed(games[f]["rs"], a, b, "cad_ti") for f in files])
    o["collar_pct"] = statistics.mean(
        [sum(1 for r in games[f]["rs"]
             if a <= int(r["rnd"]) <= b and int(r["collar_seats"]) > 0)
         / (b - a + 1) for f in files])
    return o


def line(P, lbl, c):
    if not c.get("n"):
        P(f"| {lbl} | 0 | - | - | - | - | - | - | - | - |")
        return
    rr = c["rounds"]
    P(f"| {lbl} | {c['n']} | {c['cad_builds']:.2f} | "
      f"{c['zero_build']}/{c['n']} | {c['collar_seats']/rr:.3f} | "
      f"{100*c['collar_pct']:.1f}% | {c['cad_healcore_ev']:.2f} | "
      f"{c['cad_heal_ev']-c['cad_healcore_ev']:.2f} | "
      f"{c['cad_moves']:.1f} | {c['bots_start']/rr:.2f} |")


HDR = ("| cell | n | builds | ZERO | collar seats/rd | %rd collar≥1 | "
       "core heals | non-core heals | moves | bots/rd |\n"
       "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")


def main(d):
    games = load(d)
    out = []
    P = out.append

    P("# CAD suppression mechanism — what the builders do instead\n")
    P(f"games: {len(games)}  rounds: {sum(g['n'] for g in games.values())}\n")

    # ---------------- validation: reproduce the lockout landmark -------------
    P("\n## VALIDATION — reproduce the lockout cut's landmark\n")
    P(HDR)
    for a, b in ((14, 25), (14, 40), (26, 45), (41, 80), (81, 120)):
        dm, un = cells(games, a, b)
        line(P, f"r{a}-{b} DAMAGED", agg(games, dm, a, b))
        line(P, f"r{a}-{b} undamaged", agg(games, un, a, b))

    P("\n### Population / first-damage bands\n")
    bc = collections.Counter(band_of(g["first_dmg"]) for g in games.values())
    P("| band | n |\n| --- | ---: |")
    for k in ("<=r13", "r14-25", "r26+", "never"):
        P(f"| {k} | {bc[k]} |")

    # ---------------- the builder-turn ledger --------------------------------
    P("\n## THE LEDGER — every CAD builder-turn in r14-40, labelled\n")
    for a, b in ((14, 40), (41, 80), (81, 120)):
        dm, un = cells(games, a, b)
        P(f"\n### window r{a}-{b}\n")
        P("| cell | n games | builder-turns | " +
          " | ".join(LEDGER) + " |")
        P("| --- | ---: | ---: | " + " | ".join("---:" for _ in LEDGER) + " |")
        for lbl, fs in (("DAMAGED", dm), ("undamaged", un)):
            A = agg(games, fs, a, b)
            if not A.get("n"):
                continue
            tot = sum(A["L_" + k] for k in LEDGER)
            P(f"| {lbl} | {A['n']} | {tot:.1f} | " + " | ".join(
                f"{A['L_'+k]:.2f}" for k in LEDGER) + " |")
            P(f"| {lbl} %turns | | | " + " | ".join(
                f"{100*A['L_'+k]/tot:.1f}%" for k in LEDGER) + " |")

    # ---------------- prediction 3: arithmetic closure -----------------------
    P("\n## PREDICTION 3 — the arithmetic\n")
    P("| window | missing builds | Δ core heals | Δ non-core heals | Δ attacks |"
      " Δ moves | Δ idle turns | Δ builder-turns |")
    P("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for a, b in ((14, 25), (14, 40), (26, 45), (41, 80), (81, 120)):
        dm, un = cells(games, a, b)
        D, U = agg(games, dm, a, b), agg(games, un, a, b)
        if not D.get("n") or not U.get("n"):
            continue
        td = sum(D["L_" + k] for k in LEDGER)
        tu = sum(U["L_" + k] for k in LEDGER)
        dnc = sum(D["L_" + k] for k in ("heal_bldg", "heal_bot", "heal_other"))
        unc = sum(U["L_" + k] for k in ("heal_bldg", "heal_bot", "heal_other"))
        P(f"| r{a}-{b} | {U['cad_builds']-D['cad_builds']:+.2f} | "
          f"{D['L_heal_core']-U['L_heal_core']:+.2f} | "
          f"{dnc-unc:+.2f} | "
          f"{D['L_attack']-U['L_attack']:+.2f} | "
          f"{D['L_move']-U['L_move']:+.2f} | "
          f"{D['L_idle']-U['L_idle']:+.2f} | {td-tu:+.1f} |")

    # ---------------- alternatives ------------------------------------------
    P("\n## ALTERNATIVES\n")
    P("\n### REBUILDING — is the missing build a repair elsewhere?\n")
    P("| window | cell | n | CAD bldgs lost | conv lost | harv lost | "
      "turret lost | conveyors built | harvesters built | barriers built | "
      "builder bots built | heals on own buildings |")
    P("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"
      " ---: | ---: |")
    for a, b in ((14, 40), (41, 80)):
        dm, un = cells(games, a, b)
        for lbl, fs in (("DAMAGED", dm), ("undamaged", un)):
            A = agg(games, fs, a, b)
            if not A.get("n"):
                continue
            P(f"| r{a}-{b} | {lbl} | {A['n']} | {A['cad_bldg_lost']:.2f} | "
              f"{A['cad_conv_lost']:.2f} | {A['cad_harv_lost']:.2f} | "
              f"{A['cad_turret_lost']:.2f} | {A['b_conveyor']:.2f} | "
              f"{A['b_harvester']:.2f} | {A['b_barrier']:.2f} | "
              f"{A['b_builder_bot']:.2f} | {A['L_heal_bldg']:.2f} |")

    P("\n### POVERTY — titanium in hand during the window\n")
    P("| window | cell | n | median per-round Ti | mean builder-bot builds |")
    P("| --- | --- | ---: | ---: | ---: |")
    for a, b in ((14, 40), (41, 80)):
        dm, un = cells(games, a, b)
        for lbl, fs in (("DAMAGED", dm), ("undamaged", un)):
            A = agg(games, fs, a, b)
            if not A.get("n"):
                continue
            P(f"| r{a}-{b} | {lbl} | {A['n']} | {A['ti_med']:.0f} | "
              f"{A['b_builder_bot']:.2f} |")

    P("\n### BLOCKED / UNDER FIRE — churn, and CPU\n")
    P("| window | cell | n | births | deaths | bots/rd | "
      "builder-turns/rd | botOutput/rd | TLE/rd |")
    P("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for a, b in ((14, 40), (41, 80)):
        dm, un = cells(games, a, b)
        for lbl, fs in (("DAMAGED", dm), ("undamaged", un)):
            A = agg(games, fs, a, b)
            if not A.get("n"):
                continue
            rr = A["rounds"]
            tot = sum(A["L_" + k] for k in LEDGER)
            P(f"| r{a}-{b} | {lbl} | {A['n']} | {A['born']:.2f} | "
              f"{A['died']:.2f} | {A['bots_start']/rr:.2f} | {tot/rr:.2f} | "
              f"{A['out_n']/rr:.2f} | {A['tled_n']/rr:.3f} |")

    # ---------------- version ------------------------------------------------
    P("\n## VERSION DISTRIBUTION of the games used (window r14-40)\n")
    a, b = 14, 40
    dm, un = cells(games, a, b)
    vers = collections.defaultdict(lambda: [[], []])
    for i, fs in enumerate((dm, un)):
        for f in fs:
            vers[games[f]["pop"]["cad_ver"]][i].append(f)
    P("| CAD ver | n DAMAGED | builds | core heals | collar/rd | "
      "n undamaged | builds | core heals | collar/rd |")
    P("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for v in sorted(vers, key=lambda x: int(x)):
        D = agg(games, vers[v][0], a, b)
        U = agg(games, vers[v][1], a, b)
        rr = b - a + 1
        def fmt(A):
            if not A.get("n"):
                return "0 | - | - | -"
            return (f"{A['n']} | {A['cad_builds']:.2f} | "
                    f"{A['cad_healcore_ev']:.2f} | {A['collar_seats']/rr:.3f}")
        P(f"| v{v} | {fmt(D)} | {fmt(U)} |")

    P("\n## OPPONENT SPLIT (window r14-40)\n")
    P("| cell | pop | n | builds | core heals | collar/rd | moves | idle turns |")
    P("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for popname, pred in (("vs us", lambda g: g["pop"]["vs_us"] == "1"),
                          ("3rd party", lambda g: g["pop"]["vs_us"] == "0")):
        sub = {f for f, g in games.items() if pred(g)}
        dm, un = cells(games, a, b, sub)
        for lbl, fs in (("DAMAGED", dm), ("undamaged", un)):
            A = agg(games, fs, a, b)
            if not A.get("n"):
                continue
            rr = b - a + 1
            P(f"| {lbl} | {popname} | {A['n']} | {A['cad_builds']:.2f} | "
              f"{A['cad_healcore_ev']:.2f} | {A['collar_seats']/rr:.3f} | "
              f"{A['cad_moves']:.1f} | {A['L_idle']:.1f} |")

    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1])
