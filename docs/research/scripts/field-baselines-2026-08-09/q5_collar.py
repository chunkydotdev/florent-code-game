#!/usr/bin/env python3
"""Q5 — collar-heal staffing: does a team garrison its own core at the same rate
when WE are not the threat?

Reproduces `docs/research/opponent-collar-heal-staffing-2026-08-09.md` exactly
(rounds with >=1 of the 8 heal-capable ORTH8 seats occupied, at START of round),
then splits every team's rounds into

    VS_US        the team appears in a match where OpenSverige is the other side
    THIRD_PARTY  the team appears in a match with us absent

Both cells come from ONE decoder run over ONE geometry, so the split is the only
difference between them.  A team with both cells is a within-team comparison and
needs no cross-team rating control at all.

    python q5_collar.py <freezedir> <collardir> <out.md>
"""
from __future__ import annotations

import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path

OURS_NAME = "OpenSverige"


def load_meta(fz: Path):
    """file -> {side -> (team name, opponent name, population, rating_before)}."""
    per_file = {}
    for r in csv.DictReader((fz / "meta_join.tsv").open(), delimiter="\t"):
        pop = "VS_US" if r["us_side"] != "none" else "THIRD_PARTY"
        def f(v):
            try:
                return float(v)
            except (TypeError, ValueError):
                return None
        per_file[r["file"]] = {
            "US": (r["teamAName"], r["teamBName"], pop, f(r["ratingABefore"]),
                   r["teamAVersion"], r["us_side"] == "a"),
            "THEM": (r["teamBName"], r["teamAName"], pop, f(r["ratingBBefore"]),
                     r["teamBVersion"], r["us_side"] == "b"),
        }
    return per_file


def main(argv):
    fz, cd, outp = Path(argv[0]), Path(argv[1]), Path(argv[2])
    meta = load_meta(fz)

    # per (team, population): rounds, occupied rounds, seat-sum, games,
    #                         core heals, core dmg, core heal HP
    agg = defaultdict(lambda: dict.fromkeys(
        ("rounds", "occ", "seats", "heal_core", "coredmg", "coreheal", "cheb"), 0))
    games = defaultdict(set)
    seats_avail = defaultdict(list)

    with (cd / "collar_rounds.tsv").open() as fh:
        rd = csv.reader(fh, delimiter="\t")
        head = next(rd)
        I = {c: i for i, c in enumerate(head)}
        i_file, i_side = I["file"], I["side"]
        i_os0, i_ch0 = I["orth_seats0"], I["cheb_seats0"]
        i_hc, i_cd, i_chl = I["heal_core_ev"], I["coredmg"], I["coreheal"]
        for row in rd:
            m = meta.get(row[i_file])
            if m is None:
                continue
            name, _opp, pop, _rb, _ver, is_us = m[row[i_side]]
            if is_us:                       # OpenSverige's own side: not "the field"
                key = (OURS_NAME, pop)
            else:
                key = (name, pop)
            a = agg[key]
            s = int(row[i_os0])
            a["rounds"] += 1
            a["seats"] += s
            a["cheb"] += int(row[i_ch0])
            if s > 0:
                a["occ"] += 1
            a["heal_core"] += int(row[i_hc])
            a["coredmg"] += int(row[i_cd])
            a["coreheal"] += int(row[i_chl])
            games[key].add(row[i_file])

    # free/standable ORTH8 seats per (file, side) -- collar truncation check
    with (cd / "collar_games.tsv").open() as fh:
        rd = csv.reader(fh, delimiter="\t")
        head = next(rd)
        J = {c: i for i, c in enumerate(head)}
        for row in rd:
            m = meta.get(row[J["file"]])
            if m is None:
                continue
            name, _opp, pop, _rb, _ver, is_us = m[row[J["side"]]]
            key = (OURS_NAME if is_us else name, pop)
            seats_avail[key].append(int(row[J["orth_n"]]))

    def line(key):
        a = agg[key]
        n = a["rounds"]
        if not n:
            return None
        return {
            "games": len(games[key]), "rounds": n,
            "occ_pct": 100.0 * a["occ"] / n,
            "seats_mean": a["seats"] / n,
            "cheb_mean": a["cheb"] / n,
            "heals_per_game": a["heal_core"] / len(games[key]),
            "heals_per_100r": 100.0 * a["heal_core"] / n,
            "coredmg": a["coredmg"], "coreheal": a["coreheal"],
            "healed_share": (100.0 * a["coreheal"] / a["coredmg"]) if a["coredmg"] else None,
            "orth_n": statistics.mean(seats_avail[key]) if seats_avail[key] else None,
        }

    teams = sorted({k[0] for k in agg})
    out = []
    out.append("| team | pop | games | rounds | collar-occupied rounds | mean seats | core heals/game | core dmg healed back |")
    out.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    both = []
    for t in teams:
        for pop in ("VS_US", "THIRD_PARTY"):
            d = line((t, pop))
            if not d:
                continue
            hs = "—" if d["healed_share"] is None else f"{d['healed_share']:.1f}%"
            out.append(f"| {t} | {pop} | {d['games']} | {d['rounds']:,} | "
                       f"{d['occ_pct']:.1f}% | {d['seats_mean']:.3f} | "
                       f"{d['heals_per_game']:.1f} | {hs} |")
        a, b = line((t, "VS_US")), line((t, "THIRD_PARTY"))
        if a and b and a["games"] >= 5 and b["games"] >= 5:
            both.append((t, a, b))

    out.append("")
    out.append("## WITHIN-TEAM PAIRS (>=5 games in each cell)")
    out.append("")
    out.append("| team | vs-us games | vs-us occ% | 3P games | 3P occ% | delta (pp) | vs-us seats | 3P seats |")
    out.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    both.sort(key=lambda r: -(r[1]["games"] + r[2]["games"]))
    for t, a, b in both:
        out.append(f"| {t} | {a['games']} | {a['occ_pct']:.1f}% | {b['games']} | "
                   f"{b['occ_pct']:.1f}% | {b['occ_pct'] - a['occ_pct']:+.1f} | "
                   f"{a['seats_mean']:.3f} | {b['seats_mean']:.3f} |")

    if both:
        deltas = [b["occ_pct"] - a["occ_pct"] for _t, a, b in both]
        pos = sum(1 for d in deltas if d > 0)
        out.append("")
        out.append(f"paired teams: {len(both)}; median delta "
                   f"{statistics.median(deltas):+.1f}pp; mean "
                   f"{statistics.mean(deltas):+.1f}pp; "
                   f"{pos}/{len(deltas)} garrison MORE without us")
        # round-weighted pooled field figure
        for pop in ("VS_US", "THIRD_PARTY"):
            R = sum(agg[(t, pop)]["rounds"] for t, _a, _b in both)
            O = sum(agg[(t, pop)]["occ"] for t, _a, _b in both)
            S = sum(agg[(t, pop)]["seats"] for t, _a, _b in both)
            out.append(f"pooled over paired teams, {pop}: {O/R:.4%} occupied, "
                       f"{S/R:.4f} mean seats, {R:,} rounds")

    # whole-population pooled, field only (us excluded)
    out.append("")
    out.append("## POOLED, FIELD ONLY (OpenSverige's own side excluded)")
    for pop in ("VS_US", "THIRD_PARTY"):
        R = sum(a["rounds"] for k, a in agg.items() if k[1] == pop and k[0] != OURS_NAME)
        O = sum(a["occ"] for k, a in agg.items() if k[1] == pop and k[0] != OURS_NAME)
        S = sum(a["seats"] for k, a in agg.items() if k[1] == pop and k[0] != OURS_NAME)
        G = sum(len(g) for k, g in games.items() if k[1] == pop and k[0] != OURS_NAME)
        nt = len({k[0] for k in agg if k[1] == pop and k[0] != OURS_NAME})
        out.append(f"- **{pop}**: {nt} teams, {G:,} team-games, {R:,} rounds, "
                   f"**{O/R:.2%} collar-occupied**, {S/R:.4f} mean seats")
    d = line((OURS_NAME, "VS_US"))
    out.append(f"- **OpenSverige (reference)**: {d['games']} games, {d['rounds']:,} rounds, "
               f"**{d['occ_pct']:.2f}% collar-occupied**, {d['seats_mean']:.4f} mean seats")

    outp.write_text("\n".join(out) + "\n")
    print("\n".join(out[-40:]))


if __name__ == "__main__":
    main(sys.argv[1:])
