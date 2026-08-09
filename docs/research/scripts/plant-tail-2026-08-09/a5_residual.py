#!/usr/bin/env python3
"""Residual checks: seat artifact, map-after-opponent, sentinel null + power,
nest formation timing, and where the surviving tail actually lives."""
import csv, collections, math

D = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/tail/"
BASE = "/Users/junghard/Projects/Work/florent-code-game/corpus/"

rows = []
for r in csv.DictReader(open(D + "plants2.tsv"), delimiter="\t"):
    for k in ("our_team", "won", "lastrnd", "rnd", "x", "y", "d2", "died", "life",
              "nb_same8", "nb_sameturret8", "nb_opp8"):
        r[k] = int(r[k])
    r["fu"] = r["lastrnd"] - r["rnd"]
    rows.append(r)
T = 200
pop = [r for r in rows if r["side"] == "THEM" and r["fu"] >= T]
for r in pop:
    r["alive"] = 1 if ((not r["died"]) or r["life"] > T) else 0
ALL = [r for r in rows if r["side"] == "THEM"]


def pr(g):
    if not g:
        return "-"
    return f"{sum(r['alive'] for r in g)/len(g):.1%} (n={len(g)})"


print("=== SEAT: is the seat effect a d2-geometry artifact? "
      "(d2 is to the NW corner of the 2x2 core, which is asymmetric by seat)")
for s in (0, 1):
    g = [r for r in pop if r["our_team"] == s]
    dd = collections.Counter(("near<=8" if r["d2"] <= 8 else "mid9-17" if r["d2"] <= 17
                              else "far18-32") for r in g)
    tot = sum(dd.values())
    print(f"  seat{s}: n={tot}  " + "  ".join(f"{k} {v/tot:.1%}" for k, v in
                                              sorted(dd.items())))
print("  seat effect WITHIN each distance bucket:")
for b, f in (("near<=8", lambda r: r["d2"] <= 8), ("mid9-17", lambda r: 9 <= r["d2"] <= 17),
             ("far18-32", lambda r: r["d2"] >= 18)):
    a = [r for r in pop if f(r) and r["our_team"] == 0]
    c = [r for r in pop if f(r) and r["our_team"] == 1]
    print(f"    {b:9s} seat0 {pr(a):18s}  seat1 {pr(c):18s}")

print("\n=== MAP after opponent: within-opponent map spread "
      "(opponents with >=150 at-risk plants)")
byo = collections.defaultdict(list)
for r in pop:
    byo[r["opp"]].append(r)
for o, v in sorted(byo.items(), key=lambda t: -len(t[1]))[:6]:
    bym = collections.defaultdict(list)
    for r in v:
        bym[r["map"]].append(r)
    cells = [(m, sum(x["alive"] for x in g)/len(g), len(g))
             for m, g in bym.items() if len(g) >= 25]
    cells.sort(key=lambda t: -t[1])
    if len(cells) >= 2:
        print(f"  {o:22s} overall {sum(x['alive'] for x in v)/len(v):5.1%} (n={len(v)}) "
              f" best map {cells[0][0]} {cells[0][1]:.1%}(n={cells[0][2]}) "
              f" worst {cells[-1][0]} {cells[-1][1]:.1%}(n={cells[-1][2]}) "
              f" spread {(cells[0][1]-cells[-1][1])*100:+.0f}pp over {len(cells)} maps>=25")

print("\n=== SENTINEL vs GUNNER: null + power")
gg = [r for r in pop if r["kind"] == "gunner"]
ss = [r for r in pop if r["kind"] == "sentinel"]
pg = sum(r["alive"] for r in gg)/len(gg); ps = sum(r["alive"] for r in ss)/len(ss)
se = math.sqrt(pg*(1-pg)/len(gg) + ps*(1-ps)/len(ss))
print(f"  gunner {pg:.1%} (n={len(gg)})  sentinel {ps:.1%} (n={len(ss)})  "
      f"diff {(ps-pg)*100:+.1f}pp  SE {se*100:.1f}pp  "
      f"95%CI [{(ps-pg-1.96*se)*100:+.1f}, {(ps-pg+1.96*se)*100:+.1f}]pp")
print(f"  minimum detectable difference at 80% power, alpha .05: "
      f"{2.8*se*100:.1f}pp -> this test can only rule out effects larger than that")
# within-opponent
print("  within-opponent (opponents with >=40 sentinels at risk):")
for o, v in byo.items():
    s2 = [r for r in v if r["kind"] == "sentinel"]; g2 = [r for r in v if r["kind"] == "gunner"]
    if len(s2) >= 40 and len(g2) >= 40:
        print(f"    {o:22s} sentinel {pr(s2):16s} gunner {pr(g2)}")

print("\n=== NEST FORMATION: how long between the seed plant and the second turret "
      "in the same d2<=8 neighbourhood?")
byfile = collections.defaultdict(list)
for r in ALL:
    byfile[r["file"]].append(r)
gaps = []
seed_alive_when_2nd = 0
tot2 = 0
for f, v in byfile.items():
    v = sorted(v, key=lambda r: r["rnd"])
    for i, r in enumerate(v):
        if r["nb_sameturret8"] != 0:
            continue
        # find the next plant within d2<=8 of this one
        for r2 in v[i+1:]:
            if (r2["x"]-r["x"])**2 + (r2["y"]-r["y"])**2 <= 8:
                gaps.append(r2["rnd"] - r["rnd"])
                tot2 += 1
                if r["died"] == 0 or r["life"] > (r2["rnd"] - r["rnd"]):
                    seed_alive_when_2nd += 1
                break
gaps.sort()


def q(v, p):
    return v[int(p*(len(v)-1))] if v else -1


print(f"  seed plants (0 turrets nearby) that later got a neighbour: n={tot2}")
print(f"  rounds from seed to 2nd turret: p10={q(gaps,.1)} median={q(gaps,.5)} "
      f"p90={q(gaps,.9)}")
print(f"  <=10 rounds: {sum(1 for g in gaps if g<=10)/len(gaps):.1%}   "
      f"<=25: {sum(1 for g in gaps if g<=25)/len(gaps):.1%}   "
      f"<=50: {sum(1 for g in gaps if g<=50)/len(gaps):.1%}")
print(f"  seed still alive when the 2nd arrived: {seed_alive_when_2nd/tot2:.1%}")

print("\n=== WHERE THE TAIL LIVES: share of long-lived plants by cell")
buck = lambda r: "near<=8" if r["d2"] <= 8 else "mid9-17" if r["d2"] <= 17 else "far18-32"
cl = lambda r: "0turr" if r["nb_sameturret8"] == 0 else "1turr" if r["nb_sameturret8"] == 1 else "2+turr"
surv = [r for r in pop if r["alive"]]
cnt = collections.Counter((cl(r), buck(r)) for r in surv)
tot = len(surv)
allc = collections.Counter((cl(r), buck(r)) for r in pop)
print(f"  n surviving 200+ = {tot} of {len(pop)} at-risk")
for k, v in cnt.most_common():
    print(f"    {k[0]:7s} {k[1]:9s} {v:4d} = {v/tot:5.1%} of the tail "
          f"(cell survival {v/allc[k]:5.1%}, cell is {allc[k]/len(pop):5.1%} of plants)")
print(f"  0-turret plants are {sum(v for k,v in allc.items() if k[0]=='0turr')/len(pop):.1%} "
      f"of plants and {sum(v for k,v in cnt.items() if k[0]=='0turr')/tot:.1%} of the tail")
