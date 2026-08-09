#!/usr/bin/env python3
"""Rating stratification + the within-team form of Q2.

The obvious objection to the whole exercise is that third-party games are not
rating-matched to the games we play: `population.py` measures the third-party
field side at p10 1,090 / p90 1,930 against 1,514 / 1,728 for the sides we face.
So every headline is repeated here (a) inside rating bands built from
`ratingABefore`/`ratingBBefore`, and (b) per team, where team identity is held
fixed and no rating control is needed at all.

    python strata.py <freezedir> <collardir> <out.md>
"""
from __future__ import annotations

import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path

BANDS = [(0, 1400, "<1400"), (1400, 1550, "1400-1549"),
         (1550, 1700, "1550-1699"), (1700, 9999, ">=1700")]
MATCHED = (1500, 1750)          # the band our own opponents actually live in


def band_of(r):
    if r is None:
        return None
    for lo, hi, lab in BANDS:
        if lo <= r < hi:
            return lab
    return None


def load_meta(fz):
    M = {}
    for r in csv.DictReader((fz / "meta_join.tsv").open(), delimiter="\t"):
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
    out = []

    # ---------- Q5 collar occupancy by rating band ------------------------
    agg = defaultdict(lambda: {"r": 0, "occ": 0, "seats": 0})
    games = defaultdict(set)
    with (cd / "collar_rounds.tsv").open() as fh:
        rd = csv.reader(fh, delimiter="\t")
        head = next(rd)
        I = {c: i for i, c in enumerate(head)}
        for row in rd:
            m = M.get(row[I["file"]])
            if m is None:
                continue
            t = 0 if row[I["side"]] == "US" else 1
            if m["pop"] == "VS_US" and t == m["us_idx"]:
                key = ("OpenSverige", "ALL")
            else:
                b = band_of(m["rb"][t])
                if b is None:
                    continue
                key = (m["pop"], b)
            s = int(row[I["orth_seats0"]])
            a = agg[key]
            a["r"] += 1
            a["seats"] += s
            if s:
                a["occ"] += 1
            games[key].add((row[I["file"]], t))
            # rating-matched cell
            rb = m["rb"][t]
            if rb is not None and MATCHED[0] <= rb < MATCHED[1] and not (
                    m["pop"] == "VS_US" and t == m["us_idx"]):
                k2 = (m["pop"], "MATCHED 1500-1749")
                a2 = agg[k2]
                a2["r"] += 1
                a2["seats"] += s
                if s:
                    a2["occ"] += 1
                games[k2].add((row[I["file"]], t))

    out.append("# Q5 — collar occupancy, rating-stratified")
    out.append("")
    out.append("| rating band of the side | population | side-games | rounds | collar-occupied | mean seats |")
    out.append("| --- | --- | ---: | ---: | ---: | ---: |")
    for lab in [b[2] for b in BANDS] + ["MATCHED 1500-1749"]:
        for pop in ("VS_US", "THIRD_PARTY"):
            a = agg.get((pop, lab))
            if not a or not a["r"]:
                continue
            out.append(f"| {lab} | {pop} | {len(games[(pop,lab)])} | {a['r']:,} | "
                       f"{100.0*a['occ']/a['r']:.2f}% | {a['seats']/a['r']:.4f} |")
    a = agg[("OpenSverige", "ALL")]
    out.append(f"| — | OpenSverige | {len(games[('OpenSverige','ALL')])} | {a['r']:,} | "
               f"{100.0*a['occ']/a['r']:.2f}% | {a['seats']/a['r']:.4f} |")

    # ---------- Q2 within team ---------------------------------------------
    econ = defaultdict(lambda: defaultdict(int))
    for r in csv.DictReader((fz / "econ.tsv").open(), delimiter="\t"):
        m = M.get(r["file"])
        if m is None:
            continue
        t = int(r["team"])
        if m["pop"] == "VS_US" and t == m["us_idx"]:
            key = ("OpenSverige", "VS_US")
        else:
            key = (m["name"][t], m["pop"])
        for c in ("heals", "attacks", "ammo_converted"):
            econ[key][c] += int(r[c])
        econ[key]["_g"] = econ[key].get("_g", 0)
        econ[key].setdefault("_files", set())
    # count side-games properly
    sg = defaultdict(set)
    for r in csv.DictReader((fz / "econ.tsv").open(), delimiter="\t"):
        m = M.get(r["file"])
        if m is None:
            continue
        t = int(r["team"])
        key = (("OpenSverige", "VS_US") if (m["pop"] == "VS_US" and t == m["us_idx"])
               else (m["name"][t], m["pop"]))
        sg[key].add((r["file"], t))

    def ratio(key):
        n = len(sg[key])
        if not n:
            return None
        c = econ[key]
        rep = c["heals"] / n * 4
        dmg = c["ammo_converted"] / n * 1.8 + c["attacks"] / n * 2
        return n, dmg / rep if rep else None, c["heals"] / n, c["ammo_converted"] / n

    out.append("")
    out.append("# Q2 — damage:repair within team (>=5 side-games each cell)")
    out.append("")
    out.append("| team | vs-us games | vs-us ratio | 3P games | 3P ratio | delta |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    pairs = []
    for t in sorted({k[0] for k in sg}):
        a, b = ratio((t, "VS_US")), ratio((t, "THIRD_PARTY"))
        if not a or not b or a[0] < 5 or b[0] < 5 or a[1] is None or b[1] is None:
            continue
        pairs.append((t, a, b))
    pairs.sort(key=lambda r: -(r[1][0] + r[2][0]))
    for t, a, b in pairs:
        out.append(f"| {t} | {a[0]} | {a[1]:.2f} | {b[0]} | {b[1]:.2f} | {b[1]-a[1]:+.2f} |")
    if pairs:
        d = [b[1] - a[1] for _t, a, b in pairs]
        out.append("")
        out.append(f"{len(pairs)} paired teams; median delta {statistics.median(d):+.2f}; "
                   f"{sum(1 for x in d if x<0)}/{len(d)} are LOWER in third-party games")

    outp.write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1:])
