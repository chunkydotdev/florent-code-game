#!/usr/bin/env python3
"""Q3 — "the field's measured 2.68 healers", re-derived on third-party games.

The published figure comes from `besieged-core-confound-2026-08-09.md`: on rounds
where a side's OWN core took damage, with >=3 distinct attackers on it, the mean
number of that side's live builder bots standing on one of the 8 ring tiles
orthogonally adjacent to its own 2x2 core.  There "FIELD" meant *every non-us
side*, which in that archive is overwhelmingly **the opponent's side of our own
games**.  This re-derives the same statistic with us absent.

Input is `bb.tsv` from the PRESERVED decoder
(`docs/research/scripts/side-lane-2026-08-09/bb_decode.py`), run unchanged.
Attacker count for a besieged side = the OTHER side's `atkers_on_enemy_core` in
the same (file, round) — the confound doc's own conditioning.

    python q3_besieged.py <freezedir> <bbdir> <out.md>
"""
from __future__ import annotations

import csv
import os
import statistics
import sys
from collections import defaultdict
from pathlib import Path


KEEP_RELATED = os.environ.get("FB_KEEP_RELATED") == "1"

def load_meta(fz: Path):
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
    fz, bd, outp = Path(argv[0]), Path(argv[1]), Path(argv[2])
    M = load_meta(fz)

    # (pop-label, attacker bin) -> stats
    agg = defaultdict(lambda: {"n": 0, "adj": 0, "adj0": 0, "live": 0,
                               "heal": 0, "dmg": 0, "heal_hp": 0,
                               "adjs": []})
    per_team = defaultdict(lambda: {"n": 0, "adj": 0})
    valid_max_adj = 0
    onfp_rounds = 0

    with (bd / "bb.tsv").open() as fh:
        rd = csv.reader(fh, delimiter="\t")
        head = next(rd)
        I = {c: i for i, c in enumerate(head)}
        cur_key = None
        buf = {}

        def flush(fname, rows):
            nonlocal valid_max_adj, onfp_rounds
            m = M.get(fname)
            if m is None:
                return
            byrnd = defaultdict(dict)
            for r in rows:
                byrnd[int(r[I["rnd"]])][int(r[I["team"]])] = r
            for rnd, sides in byrnd.items():
                if len(sides) != 2:
                    continue
                for t, r in sides.items():
                    dmg = int(r[I["coredmg_taken"]])
                    if dmg <= 0:
                        continue
                    atk = int(sides[1 - t][I["atkers_on_enemy_core"]])
                    if atk < 1:
                        continue
                    adj = int(r[I["adj"]])
                    adj0 = int(r[I["adj0"]])
                    valid_max_adj = max(valid_max_adj, adj)
                    onfp_rounds += 1 if int(r[I["onfp"]]) else 0
                    b = "1" if atk == 1 else "2" if atk == 2 else "3+"
                    labels = []
                    if m["pop"] == "VS_US":
                        labels.append(("US" if t == m["us_idx"] else "FIELD_vs_us", b))
                        if t != m["us_idx"]:
                            rb = m["rb"][t]
                            if rb is not None and rb >= 1750:
                                labels.append(("TOP1750_vs_us", b))
                    else:
                        labels.append(("FIELD_third_party", b))
                        rb = m["rb"][t]
                        if rb is not None and rb >= 1750:
                            labels.append(("TOP1750_third_party", b))
                        if rb is not None:
                            labels.append(("3P_>=1550" if rb >= 1550 else "3P_<1550", b))
                    for lab in labels:
                        a = agg[lab]
                        a["n"] += 1
                        a["adj"] += adj
                        a["adj0"] += adj0
                        a["live"] += int(r[I["live_bb"]])
                        a["heal"] += int(r[I["heal_core"]])
                        a["dmg"] += dmg
                        a["heal_hp"] += int(r[I["coreheal_taken"]])
                    if b == "3+" and m["pop"] != "VS_US":
                        pt = per_team[m["name"][t]]
                        pt["n"] += 1
                        pt["adj"] += adj
                    if b == "3+" and m["pop"] == "VS_US" and t != m["us_idx"]:
                        pt = per_team[m["name"][t] + " [vs us]"]
                        pt["n"] += 1
                        pt["adj"] += adj

        for row in rd:
            f = row[I["file"]]
            if f != cur_key:
                if cur_key is not None:
                    flush(cur_key, buf[cur_key])
                    del buf[cur_key]
                cur_key = f
                buf[f] = []
            buf[f].append(row)
        if cur_key is not None:
            flush(cur_key, buf[cur_key])

    out = []
    out.append("# Q3 — adjacent healers on a besieged core")
    out.append("")
    out.append(f"geometric invariant check: max adj observed over all besieged "
               f"rounds = **{valid_max_adj}** (must be <= 8); rounds with a builder "
               f"on an own-footprint tile = {onfp_rounds}")
    out.append("")
    out.append("| population | attackers | besieged rounds | **ADJ mean (end)** | ADJ mean (start) | live bots | heal ev on own core | cancellation |")
    out.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    order = ["US", "FIELD_vs_us", "TOP1750_vs_us", "FIELD_third_party",
             "TOP1750_third_party", "3P_>=1550", "3P_<1550"]
    for lab in order:
        for b in ("1", "2", "3+"):
            a = agg.get((lab, b))
            if not a or not a["n"]:
                continue
            n = a["n"]
            canc = 100.0 * a["heal_hp"] / a["dmg"] if a["dmg"] else 0.0
            out.append(f"| {lab} | {b} | {n:,} | **{a['adj']/n:.2f}** | "
                       f"{a['adj0']/n:.2f} | {a['live']/n:.2f} | "
                       f"{a['heal']/n:.2f} | {canc:.1f}% |")

    out.append("")
    out.append("## per-team ADJ at 3+ attackers (>=500 besieged rounds)")
    out.append("")
    out.append("| team | rounds | adj mean |")
    out.append("| --- | ---: | ---: |")
    for t, d in sorted(per_team.items(), key=lambda kv: -kv[1]["n"]):
        if d["n"] >= 500:
            out.append(f"| {t} | {d['n']:,} | {d['adj']/d['n']:.2f} |")

    outp.write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1:])
