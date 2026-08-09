#!/usr/bin/env python3
"""The lockout test: does core damage suppress CtrlAltDefeat's building?

THE DESIGN, and why it is not the naive comparison
--------------------------------------------------
The naive test -- "CAD's build rate before first damage vs after it" -- cannot
work, because CAD's opening is a fixed script (185 forward-ferry throws, all in
r2-r5, zero after r5, across 15 maps).  A scripted team shows a build-rate
cliff at a fixed round in EVERY game, damaged or not, so a within-game
before/after contrast measures the script, not the damage.

So every headline number here is a LANDMARK comparison: CAD's build count over
the SAME ABSOLUTE ROUND WINDOW, between games where core damage had already
landed by the window's start and games where it had not.  The script is then
identical on both sides of the comparison and cancels.

Three further confounds, each with its own cut:
  REVERSE CAUSATION   builds in the window BEFORE any damage, by damage band.
                      If damaged-early games already built less pre-damage, the
                      arrow runs builds -> damage, not damage -> builds.
  OUTCOME SELECTION   everything is also reported split by whether CAD's core
                      eventually died.
  BEING DEAD          CAD builder bots alive through the window.  A team with no
                      builders is not locked out, it is losing.

STRICTNESS (pre-committed by the hypothesis's author mid-run, before results):
the originating game's signature is ZERO builds, not fewer.  So the cells report
the share of games with EXACTLY ZERO builds in the window, and a merely lower
mean is reported as "not this mechanism".

Usage: analyse.py <freeze_dir>
"""
from __future__ import annotations

import collections
import csv
import statistics
import sys

BANDS = [("<=r13", 0, 13), ("r14-25", 14, 25), ("r26+", 26, 10 ** 6)]


def load(d):
    pop = {r["file"]: r for r in csv.DictReader(open(f"{d}/cad_population.tsv"),
                                                delimiter="\t")}
    out = {r["file"]: r for r in csv.DictReader(open(f"{d}/cad_outcome.tsv"),
                                                delimiter="\t")}
    rounds = collections.defaultdict(list)
    for r in csv.DictReader(open(f"{d}/cad_rounds.tsv"), delimiter="\t"):
        rounds[r["file"]].append(r)
    # map names, where our own ladder games pin them
    jn = {r["file"]: r["map"] for r in csv.DictReader(open(f"{d}/join.tsv"),
                                                      delimiter="\t")}
    names = {}
    for f, o in out.items():
        if f in jn:
            names.setdefault(o["mapkey"], set()).add(jn[f])
    return pop, out, rounds, {k: "/".join(sorted(v)) for k, v in names.items()}


def i(r, k):
    return int(r[k])


def summarise(d):
    pop, out, rounds, mapnames = load(d)
    games = {}
    for f, rs in rounds.items():
        rs.sort(key=lambda r: int(r["rnd"]))
        first_dmg = next((i(r, "rnd") for r in rs if i(r, "cad_core_dmg") > 0), None)
        cad_core_died = i(rs[-1], "cad_core_hp") <= 0
        us_core_died = i(rs[-1], "us_core_hp") <= 0
        games[f] = {
            "rs": rs, "first_dmg": first_dmg, "n": len(rs),
            "cad_core_died": cad_core_died, "opp_core_died": us_core_died,
            "pop": pop[f], "out": out[f],
            "mapkey": out[f]["mapkey"],
            "mapname": mapnames.get(out[f]["mapkey"], out[f]["mapkey"]),
        }
    return games


def win(rs, a, b, key):
    return sum(i(r, key) for r in rs if a <= i(r, "rnd") <= b)


def band_of(fd):
    if fd is None:
        return "never"
    for name, lo, hi in BANDS:
        if lo <= fd <= hi:
            return name
    return "?"


def pct(n, d):
    return f"{100.0*n/d:.0f}%" if d else "-"


def cell(games, files, a, b, key):
    """Build stats over window [a,b] for a set of games."""
    vals = [win(games[f]["rs"], a, b, key) for f in files
            if games[f]["n"] > b]          # only games that reached the window
    if not vals:
        return None
    zero = sum(1 for v in vals if v == 0)
    return {"n": len(vals), "mean": statistics.mean(vals),
            "median": statistics.median(vals), "zero": zero,
            "zero_pct": pct(zero, len(vals)), "vals": vals}


def report(d, w):
    games = summarise(d)
    P = w

    P("# CAD lockout: population test\n")
    P(f"games decoded: {len(games)}\n")

    # ---------------- VALIDATION ----------------
    P("\n## VALIDATION\n")
    tot_b = tot_bb = 0
    spawn_est = 0
    for f, g in games.items():
        rs = g["rs"]
        tot_b += win(rs, 0, 10 ** 6, "cad_builds")
        tot_bb += win(rs, 0, 10 ** 6, "cad_bbuilds")
        spawn_est += (win(rs, 0, 10 ** 6, "cad_bot_deaths")
                      + i(rs[-1], "cad_bots"))
    P(f"placeEntity-builds {tot_b}, BuilderBuild events {tot_bb}, "
      f"difference {tot_b - tot_bb}\n")
    P(f"independent core-spawn estimate (bot deaths + bots alive at end) "
      f"{spawn_est}\n")

    g5 = [f for f in games if f.startswith("f92f1ca2") and "game_5" in f]
    if g5:
        g = games[g5[0]]
        rs = g["rs"]
        P(f"\nORIGINATING GAME f92f1ca2 game 5: first CAD core damage r"
          f"{g['first_dmg']}, core hp at end {i(rs[-1],'cad_core_hp')} "
          f"(rounds {g['n']}), CAD builds r12-end "
          f"{win(rs,12,10**6,'cad_builds')}, CAD BuilderBuild r12-end "
          f"{win(rs,12,10**6,'cad_bbuilds')}, CAD ammo frozen at "
          f"{i(rs[-1],'cad_ammo')}, r4 convert {win(rs,4,4,'cad_convert')}\n")

    # ---------------- first-damage profile ----------------
    P("\n## CAD's first-core-damage profile (how rare is early damage?)\n")
    for label, sel in (("all", lambda g: True),
                       ("vs us", lambda g: g["pop"]["vs_us"] == "1"),
                       ("vs third parties", lambda g: g["pop"]["vs_us"] == "0")):
        fs = [f for f, g in games.items() if sel(g)]
        b = collections.Counter(band_of(games[f]["first_dmg"]) for f in fs)
        fds = [games[f]["first_dmg"] for f in fs if games[f]["first_dmg"] is not None]
        P(f"{label:18s} n={len(fs):3d}  " +
          "  ".join(f"{k}={b.get(k,0)}" for k, _, _ in BANDS) +
          f"  never={b.get('never',0)}" +
          (f"  median first dmg r{int(statistics.median(fds))}" if fds else "") + "\n")

    # ---------------- THE LANDMARK ----------------
    P("\n## THE LANDMARK COMPARISON\n")
    P("Same absolute window, split by whether CAD's core had taken damage "
      "before the window opened.\n")
    for (wa, wb) in ((14, 25), (14, 40), (26, 45), (26, 60), (41, 80)):
        P(f"\n### window r{wa}-r{wb}\n")
        dmgd = [f for f, g in games.items()
                if g["first_dmg"] is not None and g["first_dmg"] < wa]
        clean = [f for f, g in games.items()
                 if g["first_dmg"] is None or g["first_dmg"] >= wa]
        for key in ("cad_builds", "cad_bbuilds"):
            P(f"  {key}\n")
            for label, fs in (("damaged before window", dmgd),
                              ("undamaged at window open", clean)):
                c = cell(games, fs, wa, wb, key)
                if c:
                    P(f"    {label:26s} n={c['n']:3d}  mean={c['mean']:6.1f}  "
                      f"median={c['median']:5.1f}  ZERO in "
                      f"{c['zero']}/{c['n']} ({c['zero_pct']})\n")

    # ---------------- banded landmark ----------------
    P("\n## LANDMARK, STRATIFIED BY FIRST-DAMAGE BAND\n")
    P("Band is when CAD's core FIRST took damage. Window r14-r40 is CAD's "
      "counter-build window and after.\n")
    for wa, wb in ((14, 40), (26, 60)):
        P(f"\n### window r{wa}-r{wb}\n")
        for name, lo, hi in BANDS + [("never", None, None)]:
            fs = [f for f, g in games.items() if band_of(g["first_dmg"]) == name]
            for key in ("cad_builds", "cad_bbuilds"):
                c = cell(games, fs, wa, wb, key)
                if c:
                    P(f"  {name:8s} {key:12s} n={c['n']:3d}  mean={c['mean']:6.1f}"
                      f"  median={c['median']:5.1f}  ZERO {c['zero']}/{c['n']}"
                      f" ({c['zero_pct']})\n")

    # ---------------- reverse causation ----------------
    P("\n## REVERSE CAUSATION: CAD's build rate BEFORE any damage\n")
    P("Window r6-r13 sits after the scripted ferry (r2-r5) and before the "
      "counter-build window. If early-damaged games were already building "
      "less here, the arrow runs the other way.\n")
    for name, lo, hi in BANDS + [("never", None, None)]:
        fs = [f for f, g in games.items() if band_of(g["first_dmg"]) == name]
        # restrict to games where NO damage had landed by r13 for a clean read
        for key in ("cad_builds", "cad_bbuilds"):
            c = cell(games, fs, 6, 13, key)
            if c:
                P(f"  {name:8s} {key:12s} n={c['n']:3d}  mean={c['mean']:6.1f}"
                  f"  median={c['median']:5.1f}  ZERO {c['zero']}/{c['n']}\n")

    # ---------------- builder deaths ----------------
    P("\n## BUILDER-DEATH CHECK: is CAD paralysed, or just dead?\n")
    for wa, wb in ((14, 40),):
        for name, lo, hi in BANDS + [("never", None, None)]:
            fs = [f for f, g in games.items()
                  if band_of(games[f]["first_dmg"]) == name and games[f]["n"] > wb]
            if not fs:
                continue
            bots_open = [i([r for r in games[f]["rs"] if i(r, "rnd") == wa][0],
                           "cad_bots") for f in fs]
            bots_min = [min(i(r, "cad_bots") for r in games[f]["rs"]
                            if wa <= i(r, "rnd") <= wb) for f in fs]
            builds = [win(games[f]["rs"], wa, wb, "cad_builds") for f in fs]
            zero_with_bots = sum(1 for b, bo in zip(builds, bots_min)
                                 if b == 0 and bo > 0)
            P(f"  {name:8s} n={len(fs):3d}  CAD builders alive at r{wa}: "
              f"median {statistics.median(bots_open):.1f}; min over window: "
              f"median {statistics.median(bots_min):.1f}; games with ZERO builds "
              f"AND >=1 builder alive throughout: {zero_with_bots}\n")

    # ---------------- outcome stratification ----------------
    P("\n## OUTCOME STRATIFICATION (within-winners is the only clean cut)\n")
    for died in (True, False):
        lab = "CAD core eventually DIED" if died else "CAD core SURVIVED"
        P(f"\n### {lab}\n")
        for name, lo, hi in BANDS + [("never", None, None)]:
            fs = [f for f, g in games.items()
                  if band_of(g["first_dmg"]) == name and g["cad_core_died"] == died]
            c = cell(games, fs, 14, 40, "cad_builds")
            cb = cell(games, fs, 14, 40, "cad_bbuilds")
            if c:
                P(f"  {name:8s} n={c['n']:3d}  builds r14-40 mean={c['mean']:6.1f} "
                  f"ZERO {c['zero']}/{c['n']}   BuilderBuild mean="
                  f"{cb['mean']:6.1f} ZERO {cb['zero']}/{cb['n']}\n")

    # ---------------- version ----------------
    P("\n## VERSION (the only working source: <match>.meta.json)\n")
    byver = collections.defaultdict(list)
    for f, g in games.items():
        byver[g["pop"]["cad_ver"]].append(f)
    for v in sorted(byver, key=lambda x: int(x)):
        fs = byver[v]
        b = collections.Counter(band_of(games[f]["first_dmg"]) for f in fs)
        c = cell(games, fs, 14, 40, "cad_builds")
        P(f"  v{v}: n={len(fs):3d}  bands " +
          " ".join(f"{k}={b.get(k,0)}" for k, _, _ in BANDS) +
          f" never={b.get('never',0)}" +
          (f"   builds r14-40 mean={c['mean']:.1f} ZERO {c['zero']}/{c['n']}"
           if c else "") + "\n")

    # ---------------- the trigger cell, game by game ----------------
    P("\n## THE TRIGGER CELL (first damage <= r13), GAME BY GAME\n")
    tf = sorted([f for f, g in games.items() if band_of(g["first_dmg"]) == "<=r13"],
                key=lambda f: games[f]["first_dmg"])
    P(f"n = {len(tf)}\n")
    for f in tf:
        g = games[f]
        rs = g["rs"]
        fd = g["first_dmg"]
        after = win(rs, fd, 10 ** 6, "cad_builds")
        after_bb = win(rs, fd, 10 ** 6, "cad_bbuilds")
        nxt = next((i(r, "rnd") for r in rs
                    if i(r, "rnd") >= fd and i(r, "cad_builds") > 0), None)
        nxtb = next((i(r, "rnd") for r in rs
                     if i(r, "rnd") >= fd and i(r, "cad_bbuilds") > 0), None)
        P(f"  {f[:8]} g{g['pop']['game']} v{g['pop']['cad_ver']:>3s} "
          f"vs {g['pop']['opp'][:20]:20s} {g['mapname'][:18]:18s} "
          f"first_dmg r{fd:>3d} rounds {g['n']:>4d} "
          f"builds_after {after:>4d} bb_after {after_bb:>4d} "
          f"next_build r{nxt} next_bb r{nxtb} "
          f"coredied {int(g['cad_core_died'])}\n")

    # ---------------- rounds to next build ----------------
    P("\n## ROUNDS FROM FIRST CORE DAMAGE TO CAD'S NEXT BUILD\n")
    for name, lo, hi in BANDS:
        gaps, gapsb, never_n, neverb = [], [], 0, 0
        fs = [f for f, g in games.items() if band_of(g["first_dmg"]) == name]
        for f in fs:
            g = games[f]
            fd = g["first_dmg"]
            nxt = next((i(r, "rnd") for r in g["rs"]
                        if i(r, "rnd") >= fd and i(r, "cad_builds") > 0), None)
            nxtb = next((i(r, "rnd") for r in g["rs"]
                         if i(r, "rnd") >= fd and i(r, "cad_bbuilds") > 0), None)
            if nxt is None:
                never_n += 1
            else:
                gaps.append(nxt - fd)
            if nxtb is None:
                neverb += 1
            else:
                gapsb.append(nxtb - fd)
        P(f"  {name:8s} n={len(fs):3d}  any build: median gap "
          f"{statistics.median(gaps) if gaps else '-'} rounds, never again in "
          f"{never_n}; BuilderBuild: median gap "
          f"{statistics.median(gapsb) if gapsb else '-'}, never again in {neverb}\n")

    # ---------------- opening invariants ----------------
    P("\n## OPENING INVARIANTS BY MAP: r6 launcher removal, r4 ammo dump\n")
    bymap = collections.defaultdict(list)
    for f, g in games.items():
        bymap[g["mapname"]].append(f)
    P(f"{'map':22s} {'n':>3s} {'lnc_nodmg_r6':>12s} {'lnc_nodmg_r5-7':>14s} "
      f"{'r4_conv>0':>9s} {'median_r4_conv':>14s} {'r0-5_conv_total':>15s}\n")
    for m in sorted(bymap):
        fs = bymap[m]
        r6 = r57 = c4 = 0
        amts, tots = [], []
        for f in fs:
            rs = games[f]["rs"]
            byr = {i(r, "rnd"): r for r in rs}
            if "nodmg" in byr.get(6, {"cad_lnc_gone": "-"})["cad_lnc_gone"]:
                r6 += 1
            if any("nodmg" in byr.get(x, {"cad_lnc_gone": "-"})["cad_lnc_gone"]
                   for x in (5, 6, 7)):
                r57 += 1
            a = win(rs, 4, 4, "cad_convert")
            if a > 0:
                c4 += 1
                amts.append(a)
            tots.append(win(rs, 0, 5, "cad_convert"))
        P(f"{m[:22]:22s} {len(fs):3d} {r6:12d} {r57:14d} {c4:9d} "
          f"{statistics.median(amts) if amts else '-':>14} "
          f"{statistics.median(tots):>15}\n")

    # per-round convert profile, pooled
    P("\nCAD ammo conversion by round, pooled over all games:\n")
    conv = collections.Counter()
    convn = collections.Counter()
    for f, g in games.items():
        for r in g["rs"][:12]:
            a = i(r, "cad_convert")
            if a > 0:
                conv[i(r, "rnd")] += a
                convn[i(r, "rnd")] += 1
    for rnd in sorted(convn):
        P(f"  r{rnd}: {convn[rnd]} games converted, total {conv[rnd]} Ti, "
          f"mean {conv[rnd]/convn[rnd]:.1f}\n")

    P("\nCAD launcher removals by round (nodmg = self-destruct or allied "
      "destroy), pooled, r0-r12:\n")
    lg = collections.Counter()
    ld = collections.Counter()
    for f, g in games.items():
        for r in g["rs"][:13]:
            s = r["cad_lnc_gone"]
            if s == "-":
                continue
            for tok in s.split(","):
                (lg if tok == "nodmg" else ld)[i(r, "rnd")] += 1
    for rnd in sorted(set(lg) | set(ld)):
        P(f"  r{rnd}: nodmg {lg[rnd]}, dmg {ld[rnd]}\n")


if __name__ == "__main__":
    report(sys.argv[1], sys.stdout.write)
