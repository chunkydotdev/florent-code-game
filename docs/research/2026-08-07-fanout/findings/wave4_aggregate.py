#!/usr/bin/env python3
"""Aggregate wave4_raw.json into the report tables."""
import json
import os
from collections import defaultdict

SCRATCH = ("/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/"
           "8c290b06-f7e1-40b4-b90c-7343eb7e2e8e/scratchpad")

data = json.load(open(os.path.join(SCRATCH, "findings", "wave4_raw.json")))
results = data["results"]

print("mapfile_match values:", {r["mapfile_match"] for r in results})
print()

# bucket by nemesis (kladde split into victim/besieger sub-buckets)
buckets = defaultdict(list)
for r in results:
    nem = r["nemesis"]
    if nem == "kladde-third-party":
        sub = "kladde-adj (kladde=victim)" if r.get("kladde_is_victim") else "kladde-adj (kladde=besieger)"
        buckets[sub].append(r)
    else:
        buckets[nem].append(r)

all_plants = []
for r in results:
    for row in r["rows"]:
        row2 = dict(row)
        row2["nemesis"] = r["nemesis"]
        row2["match"] = r["match"]
        row2["game"] = r["game"]
        row2["kladde_is_victim"] = r.get("kladde_is_victim")
        all_plants.append(row2)

print(f"TOTAL games analysed: {len(results)}")
print(f"TOTAL turret builds (all, both threatening and not): {len(all_plants)}")
core_damaging = [p for p in all_plants if p["core_damaging"]]
print(f"TOTAL core-damaging plants (dealt >0 dmg to victim core per damage_log): {len(core_damaging)}")
print()

def pct(n, d):
    return f"{100*n/d:.1f}%" if d else "n/a"

print("=" * 100)
print("PER-NEMESIS / PER-BUCKET TABLE")
print("=" * 100)
header = (f"{'bucket':<32} {'n_games':>7} {'n_plants':>8} {'n_coredmg':>9} "
          f"{'in_threat%':>10} {'coredmg_in_threat%':>19} {'not_aligned':>11} {'fp_dsq_range':>14}")
print(header)
summary_rows = []
for bucket, games in sorted(buckets.items()):
    plants = [row for r in games for row in r["rows"]]
    n_games = len(games)
    n_plants = len(plants)
    cdmg = [p for p in plants if p["core_damaging"]]
    in_threat = [p for p in plants if p["in_sentinel_threat"] or p["in_gunner_threat"]]
    cdmg_in_threat = [p for p in cdmg if p["in_sentinel_threat"] or p["in_gunner_threat"]]
    not_aligned = [p for p in plants if not p["aligned"]]
    fp_range = (min(p["fp_dsq"] for p in plants), max(p["fp_dsq"] for p in plants)) if plants else (None, None)
    print(f"{bucket:<32} {n_games:>7} {n_plants:>8} {len(cdmg):>9} "
          f"{pct(len(in_threat), n_plants):>10} {pct(len(cdmg_in_threat), len(cdmg)):>19} "
          f"{len(not_aligned):>11} {str(fp_range):>14}")
    summary_rows.append(dict(bucket=bucket, n_games=n_games, n_plants=n_plants,
                              n_coredmg=len(cdmg), in_threat_pct=pct(len(in_threat), n_plants),
                              coredmg_in_threat_pct=pct(len(cdmg_in_threat), len(cdmg)),
                              coredmg_in_threat_n=len(cdmg_in_threat), coredmg_total_n=len(cdmg),
                              not_aligned=len(not_aligned), fp_range=fp_range))

print()
print("=" * 100)
print("(a) OVERALL COVERAGE: core-damaging plants inside computed threat set")
print("=" * 100)
n_cdmg_in = sum(1 for p in core_damaging if p["in_sentinel_threat"] or p["in_gunner_threat"])
print(f"{n_cdmg_in} / {len(core_damaging)} = {pct(n_cdmg_in, len(core_damaging))}")
misses = [p for p in core_damaging if not (p["in_sentinel_threat"] or p["in_gunner_threat"])]
print(f"MISSES (core-damaging, model says not-threat): {len(misses)}")
for p in misses:
    print(f"   {p['nemesis']:<20} {p['match'][:8]} g{p['game']} {p['map']:<10} r{p['round']:<5} "
          f"id={p['id']} pos={p['pos']} fp_dsq={p['fp_dsq']} nw_dsq={p['nw_dsq']} "
          f"aligned={p['aligned']} dmg={p['core_dmg']}")

print()
print("=" * 100)
print("(b) fp_dsq DISTRIBUTION of ALL plants vs theoretical 5-32 band")
print("=" * 100)
fp_vals = [p["fp_dsq"] for p in all_plants]
in_band = [v for v in fp_vals if 5 <= v <= 32]
below = [v for v in fp_vals if v < 5]
above = [v for v in fp_vals if v > 32]
print(f"all plants: n={len(fp_vals)}  min={min(fp_vals)}  max={max(fp_vals)}")
print(f"  in [5,32]: {len(in_band)} ({pct(len(in_band), len(fp_vals))})")
print(f"  <5:        {len(below)} ({pct(len(below), len(fp_vals))})")
print(f"  >32:       {len(above)} ({pct(len(above), len(fp_vals))})")
print()
print("fp_dsq distribution of CORE-DAMAGING plants only:")
fp_vals_cd = [p["fp_dsq"] for p in core_damaging]
if fp_vals_cd:
    in_band_cd = [v for v in fp_vals_cd if 5 <= v <= 32]
    below_cd = [v for v in fp_vals_cd if v < 5]
    above_cd = [v for v in fp_vals_cd if v > 32]
    print(f"  n={len(fp_vals_cd)} min={min(fp_vals_cd)} max={max(fp_vals_cd)}")
    print(f"  in [5,32]: {len(in_band_cd)} ({pct(len(in_band_cd), len(fp_vals_cd))})")
    print(f"  <5:        {len(below_cd)} ({pct(len(below_cd), len(fp_vals_cd))})")
    print(f"  >32:       {len(above_cd)} ({pct(len(above_cd), len(fp_vals_cd))})")
# histogram buckets
from collections import Counter
buckets_fp = Counter()
for v in fp_vals:
    if v <= 2: k = "0-2"
    elif v <= 8: k = "3-8"
    elif v <= 16: k = "9-16"
    elif v <= 32: k = "17-32"
    elif v <= 50: k = "33-50"
    else: k = "51+"
    buckets_fp[k] += 1
print("histogram (all plants):", dict(sorted(buckets_fp.items(), key=lambda kv: kv[0])))

print()
print("=" * 100)
print("(c) NON-ALIGNED plants (economy-sniping / picket, excluded by thread-6 model by design)")
print("=" * 100)
non_aligned = [p for p in all_plants if not p["aligned"]]
print(f"{len(non_aligned)} / {len(all_plants)} = {pct(len(non_aligned), len(all_plants))}")
non_aligned_cd = [p for p in non_aligned if p["core_damaging"]]
print(f"of which core-damaging (should be ~0 since non-aligned CANNOT hit core): {len(non_aligned_cd)}")
for p in non_aligned_cd:
    print("   UNEXPECTED:", p)
# aligned but out of sentinel range (dsq>32) -- also structurally incapable
aligned_out_of_range = [p for p in all_plants if p["aligned"] and p["fp_dsq"] > 32]
print(f"aligned but fp_dsq>32 (out of sentinel range, also structurally incapable): {len(aligned_out_of_range)}")
print(f"TOTAL structurally-incapable-of-hitting-core (non-aligned OR out-of-range): "
      f"{len(non_aligned) + len(aligned_out_of_range)} / {len(all_plants)} = "
      f"{pct(len(non_aligned)+len(aligned_out_of_range), len(all_plants))}")

print()
print("=" * 100)
print("(d) HUNT_BAND_DSQ=41 question: fraction of core-damaging plants OUTSIDE the band")
print("=" * 100)
print("NOTE: bots/_v72e2/main.py:1543 actually measures")
print('   min(t.distance_squared(bp) for t in core_tiles(self.core)) > HUNT_BAND_DSQ')
print("   core_tiles() expands the NW-corner anchor to all 4 footprint tiles and takes")
print("   the MIN -- i.e. the shipped code already uses fp_dsq (nearest-footprint),")
print("   matching thread-6's convention, NOT a bare NW-corner distance.")
print()
nw_over = [p for p in core_damaging if p["nw_dsq"] > 41]
fp_over = [p for p in core_damaging if p["fp_dsq"] > 41]
print(f"core-damaging plants with nw_dsq > 41:  {len(nw_over)} / {len(core_damaging)} = {pct(len(nw_over), len(core_damaging))}")
print(f"core-damaging plants with fp_dsq > 41 (the ACTUAL coded metric): {len(fp_over)} / {len(core_damaging)} = {pct(len(fp_over), len(core_damaging))}")
print()
print("nw_dsq>41 tiles (core-damaging):")
for p in sorted(nw_over, key=lambda p: -p["nw_dsq"]):
    print(f"   {p['nemesis']:<20} {p['match'][:8]} g{p['game']} {p['map']:<10} r{p['round']:<5} "
          f"pos={p['pos']} fp_dsq={p['fp_dsq']} nw_dsq={p['nw_dsq']} dmg={p['core_dmg']} kind={p['kind']}")
print()
print("fp_dsq>41 tiles (core-damaging) -- the metric the shipped code actually checks:")
for p in sorted(fp_over, key=lambda p: -p["fp_dsq"]):
    print(f"   {p['nemesis']:<20} {p['match'][:8]} g{p['game']} {p['map']:<10} r{p['round']:<5} "
          f"pos={p['pos']} fp_dsq={p['fp_dsq']} nw_dsq={p['nw_dsq']} dmg={p['core_dmg']} kind={p['kind']}")

with open(os.path.join(SCRATCH, "findings", "wave4_summary_rows.json"), "w") as f:
    json.dump({
        "summary_rows": summary_rows,
        "coverage_n": n_cdmg_in, "coverage_d": len(core_damaging),
        "misses": misses,
        "nw_over_41": nw_over, "fp_over_41": fp_over,
        "non_aligned_n": len(non_aligned), "total_plants": len(all_plants),
        "aligned_out_of_range_n": len(aligned_out_of_range),
    }, f, indent=1, default=str)
