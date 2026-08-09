#!/usr/bin/env python3
"""Is the FIRST incursion of a game anticipatable, and how much warning is there?

The round-grain control pools all rounds, which is dominated by mid/late game
where the enemy simply lives in our base.  The kindest possible framing for a
precursor is the FIRST plant of a game: before anything is planted, is there a
run-up?
"""
import csv, collections
S = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/precursor/"

Z = collections.defaultdict(dict)
games = {}
with open(S + "zone_rounds.tsv") as f:
    f.readline()
    for line in f:
        fn, seat, rnd, nb36, nb32, ms36, ms32, lastrnd = line.split("\t")
        Z[fn][int(rnd)] = (int(nb36), int(nb32), int(ms36), int(ms32))
        games[fn] = (int(seat), int(lastrnd))
P = list(csv.DictReader(open(S + "plants2.tsv"), delimiter="\t"))
first_plant = {}
for p in P:
    r = int(p["rnd"])
    if p["file"] not in first_plant or r < first_plant[p["file"]]:
        first_plant[p["file"]] = r

print(f"games with zone activity: {len(games)}; games with >=1 in-band plant: "
      f"{len(first_plant)}")


def q(v, lab):
    v = sorted(v)
    n = len(v)
    if not n:
        print(f"  {lab}: n=0")
        return
    g = lambda x: v[min(n - 1, int(x * n))]
    print(f"  {lab}: n={n} p10={g(.1)} p25={g(.25)} med={g(.5)} p75={g(.75)} "
          f"p90={g(.9)} mean={sum(v)/n:.1f}")


first_arr = {fn: min(r) for fn, r in Z.items()}
lag = [first_plant[fn] - first_arr[fn] for fn in first_plant if fn in first_arr]
q(lag, "rounds from the FIRST enemy builder entering d2<=36 to the FIRST plant")
q([first_arr[fn] for fn in first_plant if fn in first_arr],
  "round of the first enemy builder inside d2<=36")
q(list(first_plant.values()), "round of the first in-band plant")

# occupancy in the 20 rounds before the first plant vs a matched control round
# drawn from the same game's pre-first-plant window (uniform), same statistics.
import random
random.seed(7)
hit = collections.Counter()
ctl = collections.Counter()
n = 0
for fn, fp in first_plant.items():
    z = Z.get(fn)
    if not z or fp < 40:
        continue
    n += 1
    def stat(r0, acc):
        occ = sum(1 for k in range(r0 - 19, r0 + 1) if k in z)
        mx = max((z[k][0] for k in range(r0 - 19, r0 + 1) if k in z), default=0)
        ms = max((z[k][2] for k in range(r0 - 19, r0 + 1) if k in z), default=0)
        acc["occ"] += occ
        acc["mx"] += mx
        acc["ms"] += ms
        acc["occ_full"] += 1 if occ == 20 else 0
        acc["mx2"] += 1 if mx >= 2 else 0
    stat(fp - 1, hit)
    stat(random.randint(20, fp - 1), ctl)
print(f"\n  20-round window before the FIRST plant vs a random earlier window "
      f"in the same game (n={n} games):")
for k in ("occ", "mx", "ms", "occ_full", "mx2"):
    print(f"    {k:>9}: before-plant {hit[k]/n:7.2f}   random-earlier {ctl[k]/n:7.2f}")
print("    occ = rounds of the 20 with an enemy builder in zone; mx = max builders;")
print("    ms = max loiter streak; occ_full = window fully occupied; mx2 = ever >=2")

# how long is the enemy present in our zone before the first plant, cumulatively
pre = []
for fn, fp in first_plant.items():
    z = Z.get(fn, {})
    pre.append(sum(1 for k in z if k < fp))
q(pre, "\n  cumulative rounds an enemy builder was in our zone BEFORE the first plant")
