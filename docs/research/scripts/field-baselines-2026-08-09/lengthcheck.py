#!/usr/bin/env python3
"""LENGTH CONTROL for Q2 and Q4 — the confound that nearly ate the headline.

`turrets built in r200-300 per game` and `ammunition titanium per game` are both
EXPOSURE quantities: a game that ends at r150 contributes a structural zero to the
first and a small number to the second.  Overall the two populations are matched
(mean 479 vs 489 rounds, r1000 share 29.5% vs 28.3%), so the pooled headlines are
safe — but the six named opponents from `late-game-doctrine-2026-08-09.md` §2 are
NOT: their games against us run 596 rounds mean / 36.3% to r1000, their
third-party games 333 / 10.6%.

So every r200-300 figure is repeated here (a) restricted to side-games that
actually REACHED r200, and (b) per 100 rounds actually lived inside the band.

    python lengthcheck.py <freezedir> <collardir> <out.md>
"""
from __future__ import annotations

import csv
import os
import statistics
import sys
from collections import defaultdict
from pathlib import Path

SIX = {"Ouroboros", "Powerpuff Girls", "Leviathan", "Kings College Munich",
       "CtrlAltDefeat", "Lunds Stallions"}
TURRETS = ("build_gunner", "build_sentinel", "build_launcher")


KEEP_RELATED = os.environ.get("FB_KEEP_RELATED") == "1"

def load_meta(fz):
    M = {}
    for r in csv.DictReader((fz / "meta_join.tsv").open(), delimiter="\t"):
        # POPULATION FILTER (2026-08-09 correction).  `opensverige - plan B`
        # (team id b7cafd9f) is a second registration almost certainly of us, so a
        # match it plays is NOT the field playing itself, and OUR match against it
        # is not a real opponent game either.  `meta_attrib.py` marks both with
        # `related`; the clean field is `us_side == "none" AND related == "none"`
        # and the clean vs-us cell is `us_side != "none" AND related == "none"`.
        # Set FB_KEEP_RELATED=1 to reproduce the pre-correction population, which
        # is how the movement in the deliverable's POPULATION CORRECTION section
        # is isolated from the archive having grown at the same time.
        if r.get("related", "none") != "none" and not KEEP_RELATED:
            continue
        def f(v):
            try:
                return float(v)
            except (TypeError, ValueError):
                return None
        M[r["file"]] = {
            "pop": "VS_US" if r["us_side"] != "none" else "THIRD_PARTY",
            "us_idx": 0 if r["us_side"] == "a" else 1 if r["us_side"] == "b" else None,
            "name": {0: r["teamAName"], 1: r["teamBName"]},
            "rb": {0: f(r["ratingABefore"]), 1: f(r["ratingBBefore"])},
        }
    return M


def main(argv):
    fz, cd, outp = Path(argv[0]), Path(argv[1]), Path(argv[2])
    M = load_meta(fz)
    nr = {}
    for r in csv.DictReader((cd / "collar_games.tsv").open(), delimiter="\t"):
        nr[r["file"]] = int(r["nr"])

    out = ["# Length control"]
    out.append("")
    lens = defaultdict(list)
    for f, n in nr.items():
        m = M.get(f)
        if m:
            lens[m["pop"]].append(n)
    out.append("| population | games | mean rounds | median | reached r200 | reached r1000 |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    for pop, v in lens.items():
        out.append(f"| {pop} | {len(v)} | {statistics.mean(v):.0f} | "
                   f"{statistics.median(v):.0f} | "
                   f"{100*sum(1 for x in v if x>=200)/len(v):.1f}% | "
                   f"{100*sum(1 for x in v if x>=999)/len(v):.1f}% |")

    # ---- Q4 length-controlled -------------------------------------------
    tur = defaultdict(lambda: defaultdict(int))
    seen = set()
    for r in csv.DictReader((fz / "build_agg.tsv").open(), delimiter="\t"):
        seen.add((r["file"], int(r["team"])))
        if r["band"] != "r200-300" or r["metric"] not in TURRETS:
            continue
        tur[(r["file"], int(r["team"]))][r["metric"]] += int(r["n"])
        tur[(r["file"], int(r["team"]))]["all"] += int(r["n"])

    def cells(pred):
        g = alive = 0
        gun = allt = 0
        band_rounds = 0
        for f, t in seen:
            m = M.get(f)
            if m is None or f not in nr:
                continue
            if not pred(m, t):
                continue
            g += 1
            if nr[f] >= 200:
                alive += 1
                gun += tur[(f, t)]["build_gunner"]
                allt += tur[(f, t)]["all"]
                band_rounds += min(nr[f], 300) - 200
        return g, alive, gun, allt, band_rounds

    def is_us(m, t):
        return m["pop"] == "VS_US" and t == m["us_idx"]

    POPS = [
        ("OpenSverige", lambda m, t: is_us(m, t)),
        ("field, vs us", lambda m, t: m["pop"] == "VS_US" and not is_us(m, t)),
        ("field, third-party", lambda m, t: m["pop"] == "THIRD_PARTY"),
        ("SIX, vs us", lambda m, t: m["pop"] == "VS_US" and not is_us(m, t)
         and m["name"][t] in SIX),
        ("SIX, third-party", lambda m, t: m["pop"] == "THIRD_PARTY"
         and m["name"][t] in SIX),
        ("3P >=1550", lambda m, t: m["pop"] == "THIRD_PARTY"
         and (m["rb"][t] or 0) >= 1550),
    ]
    out.append("")
    out.append("# Q4 length-controlled — turrets in r200-300")
    out.append("")
    out.append("| population | side-games | reached r200 | gunners/game (alive at r200) | all turrets/game (alive) | gunners per 100 band-rounds |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    for lab, pred in POPS:
        g, alive, gun, allt, br = cells(pred)
        if not alive:
            continue
        out.append(f"| {lab} | {g} | {100*alive/g:.1f}% | {gun/alive:.2f} | "
                   f"{allt/alive:.2f} | {100*gun/br:.2f} |")

    # ---- Q2 length-controlled: per 100 rounds ---------------------------
    econ = defaultdict(lambda: defaultdict(int))
    for r in csv.DictReader((fz / "econ.tsv").open(), delimiter="\t"):
        for c in ("heals", "attacks", "ammo_converted"):
            econ[(r["file"], int(r["team"]))][c] += int(r[c])
    out.append("")
    out.append("# Q2 length-controlled — per 100 rounds")
    out.append("")
    out.append("| population | side-games | rounds | heals/100r | ammo Ti/100r | atks/100r | **ratio** |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for lab, pred in POPS:
        h = a = am = R = n = 0
        for (f, t), c in econ.items():
            m = M.get(f)
            if m is None or f not in nr or not pred(m, t):
                continue
            n += 1
            R += nr[f]
            h += c["heals"]
            a += c["attacks"]
            am += c["ammo_converted"]
        if not R:
            continue
        rep, dmg = h * 4, am * 1.8 + a * 2
        out.append(f"| {lab} | {n} | {R:,} | {100*h/R:.1f} | {100*am/R:.1f} | "
                   f"{100*a/R:.1f} | **{dmg/rep:.2f} : 1** |")

    outp.write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1:])
