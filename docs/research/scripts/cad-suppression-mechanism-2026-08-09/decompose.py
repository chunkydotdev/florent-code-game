#!/usr/bin/env python3
"""The decomposition that decides the verdict.

  E. SHIFT-SHARE.  Builds = SUM over groups of (builder-turns in group) x
     (build rate per turn in group), with groups = {on a collar seat at round
     start, off the collar}.  Splitting the damaged-vs-undamaged build gap into
     a COMPOSITION term (bodies relocated onto the collar, where they heal
     instead of building -- the healer-displacement mechanism) and a RATE term
     (bots that are nowhere near the collar building less per turn -- which
     healing cannot explain).

  F. IDLE, split by cooldown.  A builder-turn labelled `idle` is either
     cooldown-blocked or a policy that chose nothing.  Cooldowns are
     reconstructed from setActionCooldown / setMoveCooldown and validated: 0 of
     34,363 acting turns and 0 of 374,440 moving turns had a nonzero cooldown.

  G. GEOGRAPHY.  Where CAD's builders stand, by min squared distance to their
     own core footprint.  Distinguishes "they came home to heal" from "they came
     home and stood there".

  H. POVERTY, directly.  The per-round build rate restricted to rounds where CAD
     held enough titanium that money cannot be the binding constraint.

Usage: decompose.py <freeze_dir>
"""
from __future__ import annotations

import collections
import csv
import statistics
import sys

from analyse import LEDGER, load, cells, wsum

ACT = ("build", "attack", "heal_core", "heal_bldg", "heal_bot", "heal_other")


def tot(games, files, a, b, key):
    return sum(wsum(games[f]["rs"], a, b, key) for f in files)


def main(d):
    games = load(d)
    P = print
    a, b = 14, 40
    dm, un = cells(games, a, b)

    # ---------------------------------------------------------------- E -----
    P("## E. SHIFT-SHARE — how much of the build gap is healer displacement?\n")
    P(f"window r{a}-{b}; DAMAGED n={len(dm)}, undamaged n={len(un)}\n")
    G = {}
    for lbl, fs in (("DAMAGED", dm), ("undamaged", un)):
        n = len(fs)
        row = {}
        for pre, g in (("S_", "collar"), ("O_", "off")):
            turns = sum(tot(games, fs, a, b, pre + k) for k in LEDGER) / n
            builds = tot(games, fs, a, b, pre + "build") / n
            heals = tot(games, fs, a, b, pre + "heal_core") / n
            row[g] = {"turns": turns, "builds": builds, "heals": heals,
                      "rate": builds / turns if turns else 0.0}
        G[lbl] = row
    P("| cell | group | builder-turns/game | builds/game | build rate/turn | "
      "core heals/game |")
    P("| --- | --- | ---: | ---: | ---: | ---: |")
    for lbl in ("DAMAGED", "undamaged"):
        for g in ("collar", "off"):
            r = G[lbl][g]
            P(f"| {lbl} | {g} | {r['turns']:.1f} | {r['builds']:.2f} | "
              f"{100*r['rate']:.2f}% | {r['heals']:.2f} |")

    U, D = G["undamaged"], G["DAMAGED"]
    base = sum(U[g]["builds"] for g in ("collar", "off"))
    obs = sum(D[g]["builds"] for g in ("collar", "off"))
    comp = sum(D[g]["turns"] * U[g]["rate"] for g in ("collar", "off"))
    gap = base - obs
    P(f"\n- undamaged builds/game (ledger `build` turns): **{base:.2f}**")
    P(f"- DAMAGED builds/game: **{obs:.2f}**  -> gap **{gap:.2f}**")
    P(f"- counterfactual, DAMAGED body distribution at UNDAMAGED per-turn "
      f"rates: **{comp:.2f}**")
    P(f"- **COMPOSITION** (bodies moved onto the collar): "
      f"{base-comp:+.2f} = **{100*(base-comp)/gap:.0f}%** of the gap")
    P(f"- **RATE** (same bodies, lower build propensity): {comp-obs:+.2f} = "
      f"**{100*(comp-obs)/gap:.0f}%** of the gap")
    P(f"- of the RATE term, off-collar alone: "
      f"{D['off']['turns']*(U['off']['rate']-D['off']['rate']):+.2f}")

    # ---------------------------------------------------------------- F -----
    P("\n\n## F. IDLE, split by cooldown\n")
    P("| window | cell | n | idle turns/game | idle, both cooldowns 0 | "
      "idle, action cd>0 | idle, move cd>0 | %turns free to act |")
    P("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for lo, hi in ((14, 25), (14, 40), (41, 80), (81, 120)):
        dd, uu = cells(games, lo, hi)
        for lbl, fs in (("DAMAGED", dd), ("undamaged", uu)):
            n = len(fs)
            if not n:
                continue
            idle = tot(games, fs, lo, hi, "L_idle") / n
            fr = tot(games, fs, lo, hi, "idle_free") / n
            ac = tot(games, fs, lo, hi, "idle_acd") / n
            mc = tot(games, fs, lo, hi, "idle_mcd") / n
            turns = sum(tot(games, fs, lo, hi, "L_" + k) for k in LEDGER) / n
            fa = tot(games, fs, lo, hi, "free_act") / n
            P(f"| r{lo}-{hi} | {lbl} | {n} | {idle:.1f} | {fr:.1f} | {ac:.1f} |"
              f" {mc:.1f} | {100*fa/turns:.1f}% |")

    # ---------------------------------------------------------------- G -----
    P("\n\n## G. GEOGRAPHY — where CAD's builders stand (round-start snapshot)\n")
    P("| window | cell | n | collar (ORTH8) | corner d²≤2 | d² 3-20 | "
      "d² 21-64 | d² >64 | mean min d² |")
    P("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for lo, hi in ((14, 40), (41, 80), (81, 120)):
        dd, uu = cells(games, lo, hi)
        for lbl, fs in (("DAMAGED", dd), ("undamaged", uu)):
            n = len(fs)
            if not n:
                continue
            rr = (hi - lo + 1) * n
            col = tot(games, fs, lo, hi, "collar_bots") / rr
            ch = tot(games, fs, lo, hi, "n_cheb") / rr
            nr = tot(games, fs, lo, hi, "n_near20") / rr
            md = tot(games, fs, lo, hi, "n_mid64") / rr
            fr = tot(games, fs, lo, hi, "n_far") / rr
            bots = tot(games, fs, lo, hi, "bots_start")
            md2 = tot(games, fs, lo, hi, "mind2_sum") / max(bots, 1)
            P(f"| r{lo}-{hi} | {lbl} | {n} | {col:.2f} | {ch:.2f} | {nr:.2f} | "
              f"{md:.2f} | {fr:.2f} | {md2:.1f} |")

    # ---------------------------------------------------------------- H -----
    P("\n\n## H. POVERTY, directly — build rate conditioned on money in hand\n")
    P("Per-round, r14-40 only, pooled over games; `dmgd` = CAD core already "
      "damaged at round start.\n")
    P("| CAD titanium at round | state | rounds | P(build) | builder-turns | "
      "%build | %heal_core | %move | %idle |")
    P("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    buckets = [("0-9", 0, 9), ("10-29", 10, 29), ("30-49", 30, 49),
               ("50-99", 50, 99), ("100+", 100, 10 ** 9)]
    acc = collections.defaultdict(collections.Counter)
    for f, g in games.items():
        fd = g["first_dmg"]
        for r in g["rs"]:
            rnd = int(r["rnd"])
            if not (14 <= rnd <= 40) or int(r["bots_start"]) == 0:
                continue
            state = "dmgd" if (fd is not None and fd < rnd) else "clean"
            tiv = int(r["cad_ti"])
            for name, lo, hi in buckets:
                if lo <= tiv <= hi:
                    c = acc[(name, state)]
                    c["n"] += 1
                    c["build"] += 1 if int(r["cad_builds"]) > 0 else 0
                    c["turns"] += int(r["bots_start"])
                    for k in ("build", "heal_core", "move", "idle"):
                        c[k] += int(r["L_" + k])
                    break
    for name, _lo, _hi in buckets:
        for state in ("dmgd", "clean"):
            c = acc[(name, state)]
            if not c["n"]:
                continue
            t = c["turns"]
            P(f"| {name} | {state} | {c['n']} | {c['build']/c['n']:.3f} | {t} | "
              f"{100*c['build']/t:.2f}% | {100*c['heal_core']/t:.2f}% | "
              f"{100*c['move']/t:.1f}% | {100*c['idle']/t:.1f}% |")

    # OFF-COLLAR ONLY, money-controlled: the sharpest single cell
    P("\n### The sharp cell: OFF-COLLAR builder-turns only, r14-40, "
      "money held above 30 Ti\n")
    P("| state | rounds | off-collar turns | builds | build rate/turn | "
      "%move | %idle | %attack |")
    P("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    acc2 = collections.defaultdict(collections.Counter)
    for f, g in games.items():
        fd = g["first_dmg"]
        for r in g["rs"]:
            rnd = int(r["rnd"])
            if not (14 <= rnd <= 40) or int(r["cad_ti"]) < 30:
                continue
            state = "dmgd" if (fd is not None and fd < rnd) else "clean"
            c = acc2[state]
            c["n"] += 1
            for k in LEDGER:
                c[k] += int(r["O_" + k])
    for state in ("dmgd", "clean"):
        c = acc2[state]
        t = sum(c[k] for k in LEDGER)
        if not t:
            continue
        P(f"| {state} | {c['n']} | {t} | {c['build']} | "
          f"{100*c['build']/t:.2f}% | {100*c['move']/t:.1f}% | "
          f"{100*c['idle']/t:.1f}% | {100*c['attack']/t:.1f}% |")


    # ---------------------------------------------------------------- I -----
    P("\n\n## I. WHERE the missing builds were — build site distance to own core\n")
    P("| window | cell | n | builds home d²≤20 | mid d² 21-64 | forward d²>64 |")
    P("| --- | --- | ---: | ---: | ---: | ---: |")
    for lo, hi in ((14, 40), (41, 80)):
        dd, uu = cells(games, lo, hi)
        for lbl, fs in (("DAMAGED", dd), ("undamaged", uu)):
            n = len(fs)
            if not n:
                continue
            P(f"| r{lo}-{hi} | {lbl} | {n} | "
              f"{tot(games, fs, lo, hi, 'bld_home20')/n:.2f} | "
              f"{tot(games, fs, lo, hi, 'bld_mid64')/n:.2f} | "
              f"{tot(games, fs, lo, hi, 'bld_fwd')/n:.2f} |")

    # ---------------------------------------------------------------- J -----
    P("\n\n## J. WITHIN the damaged band — does healing more mean building less?\n")
    lo, hi = 14, 40
    dd, _uu = cells(games, lo, hi)
    xs = [(wsum(games[f]["rs"], lo, hi, "cad_healcore_ev"),
           wsum(games[f]["rs"], lo, hi, "cad_builds"),
           wsum(games[f]["rs"], lo, hi, "L_idle")) for f in dd]
    def spear(u, v):
        def rank(z):
            order = sorted(range(len(z)), key=lambda i: z[i])
            r = [0.0] * len(z)
            i = 0
            while i < len(order):
                j = i
                while j + 1 < len(order) and z[order[j + 1]] == z[order[i]]:
                    j += 1
                avg = (i + j) / 2.0 + 1
                for k2 in range(i, j + 1):
                    r[order[k2]] = avg
                i = j + 1
            return r
        ru, rv = rank(u), rank(v)
        n = len(u)
        mu, mv = sum(ru) / n, sum(rv) / n
        num = sum((ru[i] - mu) * (rv[i] - mv) for i in range(n))
        den = (sum((x - mu) ** 2 for x in ru) *
               sum((x - mv) ** 2 for x in rv)) ** 0.5
        return num / den if den else 0.0
    h = [x[0] for x in xs]; bl = [x[1] for x in xs]; idl = [x[2] for x in xs]
    P(f"- n = {len(xs)} damaged-before-r14 games, window r{lo}-{hi}")
    P(f"- Spearman(core heals, builds)      = **{spear(h, bl):+.3f}**")
    P(f"- Spearman(core heals, idle turns)  = **{spear(h, idl):+.3f}**")
    P(f"- Spearman(idle turns, builds)      = **{spear(idl, bl):+.3f}**")
    med = statistics.median(h)
    for lbl2, sel in (("heals <= median", [i for i in range(len(xs)) if h[i] <= med]),
                      ("heals >  median", [i for i in range(len(xs)) if h[i] > med])):
        P(f"- {lbl2}: n={len(sel)}, mean core heals "
          f"{statistics.mean([h[i] for i in sel]):.1f}, mean builds "
          f"{statistics.mean([bl[i] for i in sel]):.2f}, mean idle "
          f"{statistics.mean([idl[i] for i in sel]):.1f}")


    # ---------------------------------------------------------------- K -----
    P("\n\n## K. WITHIN-MATCH pairing — map, opponent and both versions held fixed\n")
    P("Games inside one match share the map, CAD's version and the opponent, so a "
      "match that contains BOTH a damaged and an undamaged game is a paired "
      "control for every between-game confound at once.\n")
    lo, hi = 14, 40
    dd, uu = cells(games, lo, hi)
    bym = collections.defaultdict(lambda: {"d": [], "u": []})
    for f in dd:
        bym[games[f]["pop"]["match"]]["d"].append(f)
    for f in uu:
        bym[games[f]["pop"]["match"]]["u"].append(f)
    pairs = [(m, v) for m, v in bym.items() if v["d"] and v["u"]]
    P(f"- matches containing both cells: **{len(pairs)}** "
      f"({sum(len(v['d']) for _m, v in pairs)} damaged, "
      f"{sum(len(v['u']) for _m, v in pairs)} undamaged games)")
    metr = (("cad_builds", "builds"), ("cad_healcore_ev", "core heals"),
            ("collar_seats", "collar seat-rounds"), ("L_idle", "idle turns"),
            ("cad_moves", "moves"), ("L_build", "build turns"))
    P("\n| metric | mean DAMAGED | mean undamaged | mean within-match diff | "
      "matches D<U | D>U |")
    P("| --- | ---: | ---: | ---: | ---: | ---: |")
    for key, lbl3 in metr:
        diffs, dv, uv = [], [], []
        for _m, v in pairs:
            md = statistics.mean([wsum(games[f]["rs"], lo, hi, key) for f in v["d"]])
            mu = statistics.mean([wsum(games[f]["rs"], lo, hi, key) for f in v["u"]])
            diffs.append(md - mu); dv.append(md); uv.append(mu)
        lt = sum(1 for x in diffs if x < 0)
        gt = sum(1 for x in diffs if x > 0)
        P(f"| {lbl3} | {statistics.mean(dv):.2f} | {statistics.mean(uv):.2f} | "
          f"{statistics.mean(diffs):+.2f} | {lt} | {gt} |")


if __name__ == "__main__":
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    main(sys.argv[1])
