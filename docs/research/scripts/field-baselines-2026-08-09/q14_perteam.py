#!/usr/bin/env python3
"""Within-team companions to Q1 and Q4.

Q4's published "the field builds 2 turrets per game in r200-300" is NOT a
whole-field mean: `late-game-doctrine-2026-08-09.md` §2 is a table of SIX named
opponents' GUNNER builds against us (1.94-4.18).  The faithful re-derivation is
therefore per team, gunners, r200-300, against-us vs third-party.

Q1's published figure conditions on kills landed ON US.  Splitting our own games
by direction is what makes "the field kills late" comparable to a third-party
game, where every kill is a field kill in both directions.

    python q14_perteam.py <freezedir> <collardir> <out.md>
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

SIX = ["Ouroboros", "Powerpuff Girls", "Leviathan", "Kings College Munich",
       "CtrlAltDefeat", "Lunds Stallions"]
TURRETS = ("build_gunner", "build_sentinel", "build_launcher")


def pct(xs, p):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def load_meta(fz):
    M = {}
    for r in csv.DictReader((fz / "meta_join.tsv").open(), delimiter="\t"):
        M[r["file"]] = {
            "pop": "VS_US" if r["us_side"] != "none" else "THIRD_PARTY",
            "us_idx": 0 if r["us_side"] == "a" else 1 if r["us_side"] == "b" else None,
            "name": {0: r["teamAName"], 1: r["teamBName"]},
        }
    return M


def main(argv):
    fz, cd, outp = Path(argv[0]), Path(argv[1]), Path(argv[2])
    M = load_meta(fz)
    out = []

    # ---- Q1 direction split in our own games -----------------------------
    deaths = defaultdict(dict)
    for r in csv.DictReader((cd / "collar_games.tsv").open(), delimiter="\t"):
        deaths[r["file"]][0 if r["side"] == "US" else 1] = int(r["core_death_own"])
    ours_they, ours_we, tp = [], [], []
    for f, d in deaths.items():
        m = M.get(f)
        if m is None or len(d) != 2:
            continue
        for victim, rnd in d.items():
            if rnd < 0:
                continue
            if m["pop"] == "THIRD_PARTY":
                tp.append(rnd)
            elif victim == m["us_idx"]:
                ours_they.append(rnd)
            else:
                ours_we.append(rnd)
    out.append("# Q1 — kill round by DIRECTION")
    out.append("")
    out.append("| kills | N | median | by r100 | by r150 | by r300 |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    for lab, v in (("field kills OUR core", ours_they),
                   ("WE kill a field core", ours_we),
                   ("field kills a field core (third-party)", tp)):
        n = len(v)
        out.append(f"| {lab} | {n} | r{pct(v,.5):.0f} | "
                   + " | ".join(f"{100.0*sum(1 for x in v if x<=t)/n:.0f}%"
                                for t in (100, 150, 300)) + " |")

    # ---- Q4 per team ------------------------------------------------------
    acc = defaultdict(lambda: defaultdict(int))
    seen = defaultdict(set)
    for r in csv.DictReader((fz / "build_agg.tsv").open(), delimiter="\t"):
        m = M.get(r["file"])
        if m is None:
            continue
        t = int(r["team"])
        if m["pop"] == "VS_US" and t == m["us_idx"]:
            key = ("OpenSverige", "VS_US")
        else:
            key = (m["name"][t], m["pop"])
        seen[key].add((r["file"], t))
        if r["band"] == "r200-300" and r["metric"] in TURRETS:
            acc[key][r["metric"]] += int(r["n"])
            acc[key]["all"] += int(r["n"])

    out.append("")
    out.append("# Q4 — gunners and all turrets built per game, r200-300, per team")
    out.append("")
    out.append("| team | vs-us games | vs-us gunners | vs-us all turrets | 3P games | 3P gunners | 3P all turrets | gunner delta |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    teams = sorted({k[0] for k in seen})
    rows = []
    for t in teams:
        a, b = ("VS_US"), ("THIRD_PARTY")
        na, nb = len(seen[(t, a)]), len(seen[(t, b)])
        if na < 5 or nb < 5:
            continue
        ga, gb = acc[(t, a)]["build_gunner"] / na, acc[(t, b)]["build_gunner"] / nb
        rows.append((t, na, ga, acc[(t, a)]["all"] / na, nb, gb,
                     acc[(t, b)]["all"] / nb, gb - ga))
    rows.sort(key=lambda r: -(r[1] + r[4]))
    for t, na, ga, aa, nb, gb, ab, d in rows:
        star = " **" if t in SIX else " "
        out.append(f"|{star}{t}{star.strip()} | {na} | {ga:.2f} | {aa:.2f} | "
                   f"{nb} | {gb:.2f} | {ab:.2f} | {d:+.2f} |")

    six = [r for r in rows if r[0] in SIX]
    if six:
        na = sum(r[1] for r in six); nb = sum(r[4] for r in six)
        ga = sum(r[2] * r[1] for r in six) / na
        gb = sum(r[5] * r[4] for r in six) / nb
        out.append("")
        out.append(f"**the published SIX, pooled**: vs-us {na} games "
                   f"{ga:.2f} gunners/game; third-party {nb} games {gb:.2f} "
                   f"gunners/game ({gb-ga:+.2f})")
    deltas = [r[7] for r in rows]
    if deltas:
        pos = sum(1 for d in deltas if d > 0)
        out.append(f"all {len(rows)} paired teams: {pos} build MORE gunners in "
                   f"third-party games; mean delta {sum(deltas)/len(deltas):+.2f}")

    outp.write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1:])
