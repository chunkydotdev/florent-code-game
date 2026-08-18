#!/usr/bin/env python3
"""s51 map segmentation -- gunner-cripple vs barrier-rush, per-map overperformance.

Method (per Magnus's instructions, s51): within-tape delta-vs-pooled, NOT
cross-tape absolute share comparison (tapes have different controls).

  delta_map = share_map - share_pooled(tape)
  half_width = 1.96 * sqrt(pbar*(1-pbar)/n_map) * sqrt(DEFF)

  pbar = tape's pooled share (used in the variance term for every map --
         standard one-sample-vs-pool test).
  DEFF: local tapes (BELTBREAK2, SIEGECREW) are corefill/arena-style local
        shards (overnight.sh, MacBook-Pro) -> pair-weighted DEFF ~0.98
        measured s39 -> naive (DEFF=1) is correct and marginally conservative.
        Ladder tape is the PLATFORM surface -> per-map cut: the MATCH cluster
        dies (5-game matches spread across 5 different maps, verified
        elsewhere in this repo), the OPPONENT cluster survives at residual
        DEFF ~= 1.07 -> applied here.

  verdict: GOOD if delta > +half_width, BAD if delta < -half_width, else
           NEUTRAL.
"""
from __future__ import annotations
import csv
import math
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

MAPS = ["antler", "archipelago", "auroraveil", "drakkarfjord", "drumlin",
        "fjordgate", "frostgate", "glacierkeep", "icefloe", "midgard",
        "nordkap", "ragnarok", "royale", "valkyrie", "yulerune"]

GATED = {"antler", "archipelago", "fjordgate"}


def load_tsv_with_comment(path):
    with open(path) as f:
        first = f.readline()
        assert first.startswith("#"), f"{path}: expected comment line 1"
        header = f.readline().rstrip("\n").split("\t")
        rows = []
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            rows.append(dict(zip(header, line.split("\t"))))
    return rows


def half_width(pbar, n, deff=1.0):
    if n == 0:
        return float("inf")
    return 1.96 * math.sqrt(pbar * (1 - pbar) / n * deff)


def per_map_table(rows, win_key_fn, mapkey="map"):
    """rows: list of dict. win_key_fn(row)->bool (counts as a 'win' for the
    mode). Returns (pooled_share, pooled_n, {map: (n, wins, share)})."""
    by_map = defaultdict(lambda: [0, 0])  # n, wins
    for r in rows:
        m = r[mapkey]
        by_map[m][0] += 1
        if win_key_fn(r):
            by_map[m][1] += 1
    total_n = sum(v[0] for v in by_map.values())
    total_w = sum(v[1] for v in by_map.values())
    pooled = total_w / total_n if total_n else 0.0
    out = {}
    for m, (n, w) in by_map.items():
        out[m] = (n, w, w / n if n else 0.0)
    return pooled, total_n, out


def verdict(delta, hw):
    if delta > hw:
        return "GOOD"
    if delta < -hw:
        return "BAD"
    return "NEUTRAL"


def emit_tape_table(name, pooled, total_n, per_map, deff, fh):
    fh.write(f"# {name}: pooled share {pooled:.4f} ({pooled*100:.2f}%) n={total_n} DEFF={deff}\n")
    fh.write("map\tn\twins\tshare\tdelta_pp\thalf_width_pp\tverdict\n")
    for m in MAPS:
        if m not in per_map:
            fh.write(f"{m}\tNA\tNA\tNA\tNA\tNA\tNO_DATA\n")
            continue
        n, w, share = per_map[m]
        hw = half_width(pooled, n, deff)
        delta = share - pooled
        v = verdict(delta, hw)
        fh.write(f"{m}\t{n}\t{w}\t{share*100:.2f}\t{delta*100:+.2f}\t{hw*100:.2f}\t{v}\n")


def main():
    bb_rows = load_tsv_with_comment(ROOT / "scratchpad/overnight/BELTBREAK2.tsv")
    sc_rows = load_tsv_with_comment(ROOT / "scratchpad/overnight/SIEGECREW.tsv")

    # instrument guard
    sc_t = sum(1 for r in sc_rows if r["winner"] == "T")
    assert len(sc_rows) == 1257, f"SIEGECREW n={len(sc_rows)} expected 1257"
    assert abs(sc_t / len(sc_rows) - 0.49482895783611774) < 1e-9, "SIEGECREW pooled mismatch"
    bb_t = sum(1 for r in bb_rows if r["winner"] == "T")
    assert len(bb_rows) == 5400, f"BELTBREAK2 n={len(bb_rows)} expected 5400"
    assert round(bb_t / len(bb_rows) * 10000) == 5309, "BELTBREAK2 pooled mismatch"
    print(f"INSTRUMENT GUARD OK: SIEGECREW {sc_t}/{len(sc_rows)} = {sc_t/len(sc_rows)*100:.2f}%  "
          f"BELTBREAK2 {bb_t}/{len(bb_rows)} = {bb_t/len(bb_rows)*100:.4f}%")

    bb_pooled, bb_n, bb_map = per_map_table(bb_rows, lambda r: r["winner"] == "T")
    sc_pooled, sc_n, sc_map = per_map_table(sc_rows, lambda r: r["winner"] == "T")

    # ladder: ourver 159 (gunner-cripple/beltbreak chassis) and 155 (kladturbo lineage, secondary)
    ladder_rows = []
    with open(ROOT / "corpus/ladder_games.tsv") as f:
        rdr = csv.DictReader(f, delimiter="\t")
        for r in rdr:
            ladder_rows.append(r)
    v159 = [r for r in ladder_rows if r["ourver"] == "159"]
    v155 = [r for r in ladder_rows if r["ourver"] == "155"]
    v159_pooled, v159_n, v159_map = per_map_table(v159, lambda r: r["won"] == "1")
    v155_pooled, v155_n, v155_map = per_map_table(v155, lambda r: r["won"] == "1")

    LADDER_DEFF = 1.07

    with open(OUT / "tape1_beltbreak2_permap.tsv", "w") as fh:
        emit_tape_table("BELTBREAK2 (v488beltbreak2 T vs v468kladturbo C) -- GUNNER-CRIPPLE local, n=5400 full",
                         bb_pooled, bb_n, bb_map, 1.0, fh)

    with open(OUT / "tape2_siegecrew_permap.tsv", "w") as fh:
        emit_tape_table("SIEGECREW (v513siegecrew T vs v488beltbreak2 C) -- BARRIER-RUSH local, n=1257 partial/trend-floor-stopped",
                         sc_pooled, sc_n, sc_map, 1.0, fh)

    with open(OUT / "tape3_ladder_v159_permap.tsv", "w") as fh:
        emit_tape_table("LADDER ourver=159 (gunner-cripple chassis) vs whole field, n=" + str(v159_n) + f" DEFF={LADDER_DEFF}",
                         v159_pooled, v159_n, v159_map, LADDER_DEFF, fh)

    with open(OUT / "tape3b_ladder_v155_permap.tsv", "w") as fh:
        emit_tape_table("LADDER ourver=155 (kladturbo lineage, SECONDARY cripple-mode reference) vs whole field, n=" + str(v155_n) + f" DEFF={LADDER_DEFF}",
                         v155_pooled, v155_n, v155_map, LADDER_DEFF, fh)

    # quadrant table
    def get_verdict(pooled, per_map, m, deff=1.0):
        if m not in per_map:
            return None, None, None
        n, w, share = per_map[m]
        hw = half_width(pooled, n, deff)
        delta = share - pooled
        return verdict(delta, hw), delta, hw

    quad_rows = []
    for m in MAPS:
        gv, gd, ghw = get_verdict(bb_pooled, bb_map, m, 1.0)
        rv, rd, rhw = get_verdict(sc_pooled, sc_map, m, 1.0)
        lv, ld, lhw = get_verdict(v159_pooled, v159_map, m, LADDER_DEFF)
        gated = m in GATED
        # local/ladder disagreement flag for gunner mode
        disagree = None
        if gv is not None and lv is not None:
            combined_hw = ghw + lhw
            # disagreement: the two deltas' CIs do not overlap (|diff| exceeds
            # the combined half-width), regardless of which side of zero
            # either sits on individually.
            disagree = abs(gd - ld) > combined_hw
        quad_rows.append(dict(map=m, gated=gated, gunner_local=gv, gunner_local_delta=gd,
                               gunner_ladder=lv, gunner_ladder_delta=ld,
                               gunner_disagree=disagree,
                               rush_local=rv if not gated else "CONFOUNDED",
                               rush_local_delta=rd,
                               ore_dist=None))

    ore = {}
    with open(OUT / "ore_geom.tsv") as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            ore[row["map"]] = float(row["dist_mean"])
    for row in quad_rows:
        row["ore_dist"] = ore.get(row["map"])

    with open(OUT / "quadrant_table.tsv", "w") as fh:
        fh.write("map\tgated\tore_dist\tgunner_verdict(local)\tgunner_delta_local_pp\tgunner_verdict(ladder)\tgunner_delta_ladder_pp\tlocal_ladder_disagree\trush_verdict(local)\trush_delta_local_pp\n")
        for row in quad_rows:
            fh.write(f"{row['map']}\t{row['gated']}\t{row['ore_dist']}\t{row['gunner_local']}\t{row['gunner_local_delta']*100:+.2f}\t"
                      f"{row['gunner_ladder']}\t{row['gunner_ladder_delta']*100:+.2f}\t{row['gunner_disagree']}\t"
                      f"{row['rush_local']}\t{(row['rush_local_delta']*100 if row['rush_local_delta'] is not None else float('nan')):+.2f}\n")

    print("wrote per-map tables + quadrant_table.tsv to", OUT)


if __name__ == "__main__":
    main()
