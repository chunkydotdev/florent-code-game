#!/usr/bin/env python3
"""Q1 RATING-GAP CONTROL — is the third-party median kill round (r211) resilience
on our side, or mismatch in the third-party pool?

THE COMPETING EXPLANATION.  We meet rating-matched opponents on the ladder.  The
third-party pool spans 71 teams with no such constraint, so it contains badly
mismatched pairs, and **a weak team dying fast to a strong one pulls the median
down with nobody rushing.**  That alone could produce r211.

THE TEST.  Median kill round as a function of the |ratingABefore - ratingBBefore|
gap.  If the median climbs toward r296 as the gap narrows, the headline is
mismatch and the causal reading is dead.  If it stays near r211 among evenly
matched pairs, the causal reading survived a real attempt to kill it.

Matching rule is DERIVED FROM OUR OWN GAMES rather than picked: the "matched"
cell is third-party games whose gap is at or below the 75th percentile of the gap
in our own clean ladder games, i.e. the pairing tightness we actually experience.
Both the raw and the matched figures are reported — the raw r211 stays the honest
answer to "what does the archive's field do".

`ratingABefore`/`ratingBBefore` ONLY.  `teamARating`/`teamBRating` are live joins.

    python q1_gap.py <freezedir> <collardir> <out.md>
"""
from __future__ import annotations

import csv
import os
import statistics
import sys
from collections import defaultdict
from pathlib import Path

KEEP_RELATED = os.environ.get("FB_KEEP_RELATED") == "1"
GAP_BANDS = [(0, 25, "0-24"), (25, 50, "25-49"), (50, 100, "50-99"),
             (100, 200, "100-199"), (200, 400, "200-399"), (400, 1e9, ">=400")]


def pct(xs, p):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * p
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def band(g):
    for lo, hi, lab in GAP_BANDS:
        if lo <= g < hi:
            return lab
    return None


def main(argv):
    fz, cd, outp = Path(argv[0]), Path(argv[1]), Path(argv[2])

    M = {}
    for r in csv.DictReader((fz / "meta_join.tsv").open(), delimiter="\t"):
        if r.get("related", "none") != "none" and not KEEP_RELATED:
            continue

        def f(v):
            try:
                return float(v)
            except (TypeError, ValueError):
                return None
        ra, rb = f(r["ratingABefore"]), f(r["ratingBBefore"])
        if ra is None or rb is None:
            continue
        M[r["file"]] = {
            "pop": "VS_US" if r["us_side"] != "none" else "THIRD_PARTY",
            "us_idx": 0 if r["us_side"] == "a" else 1 if r["us_side"] == "b" else None,
            "rb": {0: ra, 1: rb}, "gap": abs(ra - rb),
        }

    deaths = defaultdict(dict)
    for r in csv.DictReader((cd / "collar_games.tsv").open(), delimiter="\t"):
        deaths[r["file"]][0 if r["side"] == "US" else 1] = int(r["core_death_own"])

    out = ["# Q1 — rating-gap control on the kill round"]
    out.append("")

    # --- the gap distributions the two populations actually have ----------
    gaps = defaultdict(list)
    for f, m in M.items():
        if f in deaths:
            gaps[m["pop"]].append(m["gap"])
    out.append("| |ratingBefore gap| | our ladder games | third-party |")
    out.append("| --- | ---: | ---: |")
    for lab, p in (("n games", None), ("median", .5), ("p75", .75),
                   ("p90", .9), ("p95", .95)):
        if p is None:
            out.append(f"| {lab} | {len(gaps['VS_US'])} | {len(gaps['THIRD_PARTY'])} |")
        else:
            out.append(f"| {lab} | {pct(gaps['VS_US'], p):.0f} | "
                       f"{pct(gaps['THIRD_PARTY'], p):.0f} |")
    thr = pct(gaps["VS_US"], .75)
    out.append("")
    out.append(f"**Matching rule:** third-party games with gap <= **{thr:.0f}** "
               f"(the 75th percentile of the gap in our own clean ladder games). "
               f"This is the pairing tightness the ladder actually gives us.")

    # --- kills by population x gap band -----------------------------------
    rows = defaultdict(list)          # (pop, band, direction) -> rounds
    for f, d in deaths.items():
        m = M.get(f)
        if m is None or len(d) != 2:
            continue
        b = band(m["gap"])
        for victim, rnd in d.items():
            if rnd < 0:
                continue
            killer = 1 - victim
            strong = m["rb"][killer] >= m["rb"][victim]
            if m["pop"] == "THIRD_PARTY":
                rows[("THIRD_PARTY", b, "any")].append(rnd)
                rows[("THIRD_PARTY", b, "killer stronger" if strong else "killer weaker")].append(rnd)
                rows[("THIRD_PARTY", "ALL", "any")].append(rnd)
                if m["gap"] <= thr:
                    rows[("THIRD_PARTY", "MATCHED", "any")].append(rnd)
                    if m["rb"][killer] >= 1550:
                        rows[("THIRD_PARTY", "MATCHED >=1550 killer", "any")].append(rnd)
            elif victim == m["us_idx"]:
                rows[("FIELD_KILLS_US", b, "any")].append(rnd)
                rows[("FIELD_KILLS_US", "ALL", "any")].append(rnd)
                if m["rb"][killer] >= 1550:
                    rows[("FIELD_KILLS_US", "ALL >=1550 killer", "any")].append(rnd)

    out.append("")
    out.append("## median kill round by rating gap — THE TEST")
    out.append("")
    out.append("| population | gap band | kills (N) | median | q1 | q3 | by r100 | by r150 |")
    out.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    order = ([("FIELD_KILLS_US", "ALL"), ("FIELD_KILLS_US", "ALL >=1550 killer")]
             + [("FIELD_KILLS_US", b[2]) for b in GAP_BANDS]
             + [("THIRD_PARTY", "ALL"), ("THIRD_PARTY", "MATCHED"),
                ("THIRD_PARTY", "MATCHED >=1550 killer")]
             + [("THIRD_PARTY", b[2]) for b in GAP_BANDS])
    for pop, b in order:
        v = rows.get((pop, b, "any"))
        if not v or len(v) < 15:
            continue
        n = len(v)
        out.append(f"| {pop} | {b} | {n} | r{pct(v,.5):.0f} | r{pct(v,.25):.0f} | "
                   f"r{pct(v,.75):.0f} | "
                   f"{100*sum(1 for x in v if x<=100)/n:.0f}% | "
                   f"{100*sum(1 for x in v if x<=150)/n:.0f}% |")

    out.append("")
    out.append("## third-party kills split by whether the KILLER was the stronger side")
    out.append("")
    out.append("| gap band | killer stronger: N / median | killer weaker: N / median |")
    out.append("| --- | --- | --- |")
    for _lo, _hi, b in GAP_BANDS:
        s = rows.get(("THIRD_PARTY", b, "killer stronger"), [])
        w = rows.get(("THIRD_PARTY", b, "killer weaker"), [])
        if len(s) + len(w) < 15:
            continue
        sf = f"{len(s)} / r{pct(s,.5):.0f}" if len(s) >= 10 else f"{len(s)} / —"
        wf = f"{len(w)} / r{pct(w,.5):.0f}" if len(w) >= 10 else f"{len(w)} / —"
        out.append(f"| {b} | {sf} | {wf} |")

    outp.write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1:])
