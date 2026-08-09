#!/usr/bin/env python3
"""What population do these numbers describe? Coverage, team mix, rating mix.

Third-party games are not a random sample of the league: they are the matches our
archiver happened to download.  This prints the material needed to say so with
numbers instead of a hedge — team distribution, rating distribution of the sides
in each population (from `ratingABefore`/`ratingBBefore`, never the live-join
`teamARating`/`teamBRating`), and the rating-matched subset.

    python population.py <freezedir> <out.md>
"""
from __future__ import annotations

import csv
import os
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

OURS = "379a5d80-9921-4c9e-949b-f9b1dcba16be"


KEEP_RELATED = os.environ.get("FB_KEEP_RELATED") == "1"

def main(argv):
    fz, outp = Path(argv[0]), Path(argv[1])
    allrows = list(csv.DictReader((fz / "meta_join.tsv").open(), delimiter="\t"))
    # POPULATION FILTER — see the header comment in q124.py.  `related != "none"`
    # marks a match involving `opensverige - plan B`, a second registration almost
    # certainly of us: in the third-party bucket it is us wearing another name, and
    # in the ours bucket it is us versus us.  Neither is a field observation.
    rows = [r for r in allrows if r.get("related", "none") == "none" or KEEP_RELATED]
    excl = [r for r in allrows if r.get("related", "none") != "none"]
    out = []
    out.append("# Population")
    out.append("")
    out.append(f"**EXCLUDED as `related`:** {len(excl)} files / "
               f"{len({r['match'] for r in excl})} matches — "
               f"{len([r for r in excl if r['us_side']=='none'])} that were in the "
               f"THIRD-PARTY bucket (plan B vs a real field team) and "
               f"{len([r for r in excl if r['us_side']!='none'])} in the OURS bucket "
               f"(us versus plan B). Retained population: {len(rows)} files.")
    out.append("")

    def f(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    files = Counter()
    matches = defaultdict(set)
    sides = defaultdict(list)          # pop -> [rating_before of each field side]
    ids = {}
    for r in rows:
        pop = "VS_US" if r["us_side"] != "none" else "THIRD_PARTY"
        files[pop] += 1
        for side, nm, tid, rb in (("a", r["teamAName"], r["teamAId"], f(r["ratingABefore"])),
                                  ("b", r["teamBName"], r["teamBId"], f(r["ratingBBefore"]))):
            ids[nm] = tid
            if tid == OURS:
                continue
            matches[(pop, nm)].add(r["match"])
            if rb is not None:
                sides[pop].append(rb)

    out.append(f"- replay FILES: VS_US **{files['VS_US']}**, THIRD_PARTY **{files['THIRD_PARTY']}**")
    out.append(f"- distinct MATCHES: VS_US {len({r['match'] for r in rows if r['us_side']!='none'})}, "
               f"THIRD_PARTY {len({r['match'] for r in rows if r['us_side']=='none'})}")
    out.append(f"- distinct field teams: VS_US {len({k[1] for k in matches if k[0]=='VS_US'})}, "
               f"THIRD_PARTY {len({k[1] for k in matches if k[0]=='THIRD_PARTY'})}")
    out.append("")
    out.append("| rating_before of the field side | VS_US | THIRD_PARTY |")
    out.append("| --- | ---: | ---: |")
    for lab, fn in (("n", len), ("mean", statistics.mean),
                    ("p10", lambda v: statistics.quantiles(v, n=10)[0]),
                    ("median", statistics.median),
                    ("p90", lambda v: statistics.quantiles(v, n=10)[8])):
        out.append(f"| {lab} | {fn(sides['VS_US']):,.0f} | {fn(sides['THIRD_PARTY']):,.0f} |")
    for thr in (1400, 1500, 1550, 1600, 1750):
        a = 100.0 * sum(1 for x in sides["VS_US"] if x >= thr) / len(sides["VS_US"])
        b = 100.0 * sum(1 for x in sides["THIRD_PARTY"] if x >= thr) / len(sides["THIRD_PARTY"])
        out.append(f"| share >= {thr} | {a:.1f}% | {b:.1f}% |")

    out.append("")
    out.append("## teams by third-party match coverage (top 30)")
    out.append("")
    out.append("| team | 3P matches | vs-us matches |")
    out.append("| --- | ---: | ---: |")
    tp = sorted({k[1] for k in matches if k[0] == "THIRD_PARTY"},
                key=lambda n: -len(matches[("THIRD_PARTY", n)]))
    for n in tp[:30]:
        out.append(f"| {n} | {len(matches[('THIRD_PARTY', n)])} | "
                   f"{len(matches[('VS_US', n)])} |")

    out.append("")
    out.append("## team ids of note")
    for n in ("opensverige - plan B",):
        out.append(f"- `{n}` -> `{ids.get(n)}` (OpenSverige is `{OURS}`)")

    outp.write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1:])
