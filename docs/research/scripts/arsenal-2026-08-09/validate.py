#!/usr/bin/env python3
"""Validation-before-use for the arsenal decode. Prints one block per check."""
import csv
import sys
from collections import defaultdict

OUT = sys.argv[1]
FROZ = sys.argv[2]


def rd(p):
    with open(p) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


val = rd(f"{OUT}/ars_val.tsv")
print(f"V0  files decoded                     : {len(val)}")
print(f"V1  ring12 == 12 tiles, all files     : "
      f"{sum(int(r['ring12_ok']) for r in val)}/{len(val)}")
print(f"V2  ring8  == 8 tiles, all files      : "
      f"{sum(int(r['ring8_ok']) for r in val)}/{len(val)}")
print(f"V3  builders standing ON a footprint  : "
      f"{sum(int(r['onfp']) for r in val)} (must be 0)")
th = sum(int(r["throws"]) for r in val)
tp = sum(int(r["throw_pick_ok"]) for r in val)
tr = sum(int(r["throw_range_ok"]) for r in val)
print(f"V4  throws seen                       : {th}")
print(f"V5  a live launcher within d2<=2 of the pre-throw tile : "
      f"{tp}/{th} = {100*tp/th:.3f}%")
print(f"V6  ...and the landing tile within d2<=26 of it        : "
      f"{tr}/{th} = {100*tr/th:.3f}%")

# deliveries x 10 == econ ti_collected_end  (corpus-howto trap 6 says econ's
# `deliveries` column is dead; ti_collected_end is the populated one)
econ = defaultdict(dict)
BANDS = ["r0-150", "r150-200", "r200-300", "r300+"]
for r in rd(f"{FROZ}/econ.tsv"):
    econ[r["file"]].setdefault(r["team"], {})[r["band"]] = int(r["ti_collected_end"])
ok = bad = miss = 0
diffs = []
for r in val:
    f = r["file"]
    if f not in econ:
        miss += 1
        continue
    for t in ("0", "1"):
        b = econ[f].get(t)
        if not b:
            miss += 1
            continue
        last = None
        for bn in BANDS:
            if bn in b:
                last = b[bn]
        if last is None:
            miss += 1
            continue
        mine = int(r[f"deliv_stacks_t{t}"]) * 10
        if mine == last:
            ok += 1
        else:
            bad += 1
            diffs.append((f, t, mine, last))
print(f"V7  own-core stacks x 10 == econ.tsv ti_collected_end  : "
      f"{ok}/{ok+bad} = {100*ok/(ok+bad):.4f}%  ({miss} unmatched sides)")
for d in diffs[:5]:
    print("      mismatch", d)

# cross-check harvester builds against build_agg
agg = defaultdict(int)
for r in rd(f"{FROZ}/build_agg.tsv"):
    if r["metric"] == "build_harvester":
        agg[(r["file"], r["team"])] += int(r["n"])
mine = defaultdict(int)
for r in rd(f"{OUT}/ars_ore.tsv"):
    mine[(r["file"], r["team"])] += int(r["n_built"])
keys = set(agg) & set(mine)
same = sum(1 for k in keys if agg[k] == mine[k])
print(f"V8  harvester builds == corpus build_agg 'build_harvester' : "
      f"{same}/{len(keys)} sides agree")

# cross-check builder-bot builds against build_agg
agg2 = defaultdict(int)
for r in rd(f"{FROZ}/build_agg.tsv"):
    if r["metric"] == "build_builder_bot":
        agg2[(r["file"], r["team"])] += int(r["n"])
sp = defaultdict(int)
for r in rd(f"{OUT}/ars_spawn.tsv"):
    sp[(r["file"], r["team"])] += int(r["spawns"])
keys = set(agg2) & set(sp)
same = sum(1 for k in keys if agg2[k] == sp[k])
print(f"V9  builder spawns == corpus build_agg 'build_builder_bot': "
      f"{same}/{len(keys)} sides agree")

# throws cross-check against corpus/throws.tsv
tc = defaultdict(int)
for r in rd(f"{FROZ}/throws.tsv"):
    tc[r["file"]] += 1
same = tot = 0
for r in val:
    if r["file"] in tc:
        tot += 1
        if tc[r["file"]] == int(r["throws"]):
            same += 1
print(f"V10 throw count == corpus/throws.tsv rows : {same}/{tot} files agree")
