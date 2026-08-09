#!/usr/bin/env python3
"""Second-pass arsenal analysis: the blocking-class table, the extreme-lock
case read, spawn rate against SOFT-free slots, and the ore-reach cross-tab."""
import csv
import statistics as st
import sys
from collections import defaultdict, Counter

OUT, FROZ = sys.argv[1], sys.argv[2]


def rd(p):
    with open(p) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


J = {r["file"]: r for r in rd(f"{FROZ}/join.tsv")}


def side(r):
    j = J.get(r["file"])
    return None if not j else ("US" if r["team"] == j["our_team"] else "THEM")


def pct(a, b):
    return f"{100*a/b:.2f}%" if b else "n/a"


def q(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(p * len(xs)))] if xs else None


def hdr(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


hdr("1A — WHICH RING-TILE OCCUPANTS ACTUALLY BLOCK A SPAWN (pooled, all bands)")
sp = defaultdict(int)
ex = defaultdict(int)
for r in rd(f"{OUT}/ars_stile.tsv"):
    sp[r["tilecls"]] += int(r["n_spawn"])
    ex[r["tilecls"]] += int(r["n_tilernd"])
tot_e = sum(ex.values())
print(f"    total ring-tile-rounds observed: {tot_e:,}   "
      f"total spawns: {sum(sp.values()):,}")
print(f"    {'ring tile occupant':<26} {'tile-rounds':>13} {'spawns onto it':>15}"
      f" {'per 1k':>8}")
for k in sorted(ex, key=lambda x: -ex[x]):
    print(f"    {k:<26} {ex[k]:>13,} {sp[k]:>15,} {1000*sp[k]/ex[k]:>8.3f}")
blockers = [k for k in ex if sp[k] == 0]
print(f"\n    ZERO-SPAWN classes: {sorted(blockers)}")
print(f"    pooled zero-spawn exposure: {sum(ex[k] for k in blockers):,} "
      f"tile-rounds, {sum(sp[k] for k in blockers)} spawns")

hdr("1B — THE EXTREME CASES: every team-side that reached >=8 hostile ring tiles")
ring = rd(f"{OUT}/ars_ring.tsv")
ext = [r for r in ring if int(r["hst12_max"]) >= 8]
ext.sort(key=lambda r: -int(r["hst12_max"]))
print(f"    {len(ext)} of {len(ring)} team-sides ({pct(len(ext),len(ring))})")
print(f"    {'side':<5} {'opp':<20} {'hst':>4} {'bod':>4} {'bld':>4} "
      f"{'1st r':>6} {'rnds>=6':>8} {'coredead':>9} {'rounds':>7}")
for r in ext:
    j = J[r["file"]]
    s = side(r)
    print(f"    {s:<5} {j['opp'][:20]:<20} {r['hst12_max']:>4} "
          f"{r['hstbody12_max']:>4} {r['hstbldg12_max']:>4} "
          f"{r['f_hst12_8']:>6} {r['n_hst_ge6']:>8} "
          f"{r['core_dead_rnd']:>9} {r['rounds']:>7}")
dead = sum(1 for r in ext if int(r["core_dead_rnd"]) >= 0)
d250 = sum(1 for r in ext if 0 <= int(r["core_dead_rnd"]) < 250)
print(f"    core died: {dead}/{len(ext)} {pct(dead,len(ext))}  "
      f"| inside r250: {d250}/{len(ext)} {pct(d250,len(ext))}")
base = sum(1 for r in ring if int(r["core_dead_rnd"]) >= 0)
b250 = sum(1 for r in ring if 0 <= int(r["core_dead_rnd"]) < 250)
print(f"    BASE RATE over all sides: {pct(base,len(ring))} died, "
      f"{pct(b250,len(ring))} inside r250")

hdr("1C — HOSTILE BODIES ONLY (the form that is not refuted)")
print(f"    {'max hostile bodies':<22} {'sides':>7} {'core died':>10} "
      f"{'share':>8} {'inside r250':>12}")
for k in range(0, 7):
    sub = [r for r in ring if int(r["hstbody12_max"]) == k]
    if not sub:
        continue
    d = sum(1 for r in sub if int(r["core_dead_rnd"]) >= 0)
    d2 = sum(1 for r in sub if 0 <= int(r["core_dead_rnd"]) < 250)
    print(f"    {k:<22} {len(sub):>7} {d:>10} {pct(d,len(sub)):>8} "
          f"{pct(d2,len(sub)):>12}")
print("\n    SUSTAIN: rounds spent with >=3 hostile ring tiles, per side")
n3 = [int(r["n_hst_ge3"]) for r in ring]
n6 = [int(r["n_hst_ge6"]) for r in ring]
print(f"    >=3 hostile: sides with any {sum(1 for x in n3 if x)} "
      f"{pct(sum(1 for x in n3 if x),len(ring))}; among those median "
      f"{st.median([x for x in n3 if x]):.0f} rounds, p90 "
      f"{q([x for x in n3 if x],.9)}, max {max(n3)}")
print(f"    >=6 hostile: sides with any {sum(1 for x in n6 if x)} "
      f"{pct(sum(1 for x in n6 if x),len(ring))}; among those median "
      f"{st.median([x for x in n6 if x]):.0f} rounds, p90 "
      f"{q([x for x in n6 if x],.9)}, max {max(n6)}")

hdr("5A — SPAWN RATE vs SOFT-FREE RING TILES (conveyors count as free)")
acc = defaultdict(lambda: [0, 0])
for r in rd(f"{OUT}/ars_spawn.tsv"):
    s = side(r)
    if not s or r["atcap"] == "1" or r["band"] not in ("r0-100", "r100-250"):
        continue
    a = acc[(s, int(r["freesoft"]))]
    a[0] += int(r["rounds"])
    a[1] += int(r["spawns"])
print("    rounds < 250, 50-unit-cap rounds excluded")
print(f"    {'soft-free':>9} | {'US rounds':>10} {'US rate':>9} | "
      f"{'THEM rounds':>12} {'THEM rate':>10}")
for f in range(0, 13):
    u, t = acc[("US", f)], acc[("THEM", f)]
    if u[0] + t[0] == 0:
        continue
    ru = f"{u[1]/u[0]:.4f}" if u[0] else "-"
    rt = f"{t[1]/t[0]:.4f}" if t[0] else "-"
    print(f"    {f:>9} | {u[0]:>10} {ru:>9} | {t[0]:>12} {rt:>10}")
print("\n    HARD-BLOCKED slots (12 - softfree): pooled spawn rate")
pool = defaultdict(lambda: [0, 0])
for r in rd(f"{OUT}/ars_spawn.tsv"):
    s = side(r)
    if not s or r["atcap"] == "1" or r["band"] not in ("r0-100", "r100-250"):
        continue
    a = pool[12 - int(r["freesoft"])]
    a[0] += int(r["rounds"])
    a[1] += int(r["spawns"])
print(f"    {'blocked':>8} {'core-rounds':>13} {'spawns':>9} {'spawns/round':>13}")
for b in range(0, 13):
    a = pool[b]
    if a[0] == 0:
        continue
    print(f"    {b:>8} {a[0]:>13} {a[1]:>9} {a[1]/a[0]:>13.4f}")

hdr("4A — ORE: reach vs concentration cross-tab")
mp = {r["file"]: r for r in rd(f"{OUT}/ars_map.tsv")}
per = defaultdict(list)
for r in rd(f"{OUT}/ars_ore.tsv"):
    per[(r["file"], r["team"])].append(r)
trav = {(r["file"], r["team"]): r for r in rd(f"{OUT}/ars_trav.tsv")}
rows = []
for (f, t), rs in per.items():
    j = J.get(f)
    if not j:
        continue
    s = "US" if t == j["our_team"] else "THEM"
    n = sorted((int(x["n_built"]) for x in rs), reverse=True)
    tv = trav.get((f, str(1 - int(t))))     # the OTHER side's travel
    rows.append((s, len(rs), n, int(tv["r_enemy_ore_adj"]) if tv else -1, j["opp"]))
for s in ("THEM",):
    R = [x for x in rows if x[0] == s]
    print(f"    opponent sides with >=1 harvester: {len(R)}")
    for lim in (25, 50, 100, 250):
        sub = [x for x in R if 0 <= x[3] < lim]
        if not sub:
            continue
        d = [x[1] for x in sub]
        print(f"    our builder stood next to enemy-side ore before r{lim}: "
              f"{len(sub)} sides ({pct(len(sub),len(R))}) — their distinct ore "
              f"tiles: median {st.median(d):.0f}, mean {st.mean(d):.2f}")
    print("\n    how many of THEIR harvesters sit on the ONE tile we could "
          "deny (top-1),\n    and what the top-1 tile is worth as a share")
    t1 = [x[2][0] / sum(x[2]) for x in R]
    print(f"    top-1 share: median {st.median(t1)*100:.1f}%  "
          f"p90 {q(t1,.9)*100:.1f}%  sides where top-1 == 100%: "
          f"{sum(1 for x in t1 if x==1.0)} {pct(sum(1 for x in t1 if x==1.0),len(R))}")
    print(f"    spare-site headroom: median ore tiles ON THEIR SIDE = "
          f"{st.median([int(mp[f]['ore_side1']) if J[f]['our_team']=='0' else int(mp[f]['ore_side0']) for f in mp]):.0f}")

hdr("3A — KIDNAP-INTO-FIRE, per game and per opponent")
kid = rd(f"{OUT}/ars_kid.tsv")
byopp = defaultdict(list)
for r in kid:
    s = side(r)
    if s != "US":
        continue
    j = J[r["file"]]
    byopp[j["opp"]].append(r)
print(f"    {'opponent':<22} {'n':>4} {'opp-bot-rnds':>13} {'reach%':>8} "
      f"{'their-line%':>12} {'ff rnds/game':>13}")
for opp, R in sorted(byopp.items(), key=lambda kv: -len(kv[1])):
    if len(R) < 15:
        continue
    tot = sum(int(x["opp_bot_rounds"]) for x in R)
    kr = sum(int(x["k_reach"]) for x in R)
    fl = sum(int(x["ff_their_line_reach"]) for x in R)
    ff = [int(x["rnds_ff"]) for x in R]
    print(f"    {opp[:22]:<22} {len(R):>4} {tot:>13} {pct(kr,tot):>8} "
          f"{pct(fl,tot):>12} {st.median(ff):>13.0f}")
