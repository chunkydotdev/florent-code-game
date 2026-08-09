#!/usr/bin/env python3
"""Is the opponent spread really ROUND COMPOSITION?  Nest rate falls hard with
game phase (published: r0-50 38.8% -> r301+ 13.8%), and opponents differ in when
they plant.  Standardise on round band, and re-run the split-half on the
residual."""
import csv, collections, math, statistics

S = ("/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/"
     "628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/oppnest/")
B = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/oppnest/snap/"
created = {r["match"]: r["created"]
           for r in csv.DictReader(open(B + "ladder_games.tsv"), delimiter="\t")}
seeds = list(csv.DictReader(open(S + "seeds.tsv"), delimiter="\t"))
for s in seeds:
    s["nest"] = int(s["nest"]); s["rnd"] = int(s["rnd"])
    r = s["rnd"]
    s["band"] = ("r0-50" if r <= 50 else "r51-150" if r <= 150 else
                 "r151-300" if r <= 300 else "r301+")

bt = collections.defaultdict(lambda: [0, 0])
for s in seeds:
    bt[s["band"]][0] += s["nest"]; bt[s["band"]][1] += 1
print("nest rate by round band (reproduces the published gradient):")
for b in ("r0-50", "r51-150", "r151-300", "r301+"):
    print(f"  {b:<10}{bt[b][0]/bt[b][1]:>7.1%}  n={bt[b][1]}")
brate = {b: v[0] / v[1] for b, v in bt.items()}

opp = collections.defaultdict(list)
for s in seeds:
    opp[s["opp"]].append(s)
BIG = [o for o in opp if len(opp[o]) >= 60]

print("\nopponent OBSERVED vs EXPECTED-from-round-composition:")
print(f"{'opponent':<24}{'obs':>7}{'exp':>7}{'O/E':>6}{'n':>6}   share of seeds by band")
res = {}
for o in sorted(BIG, key=lambda o: -sum(s["nest"] for s in opp[o]) / len(opp[o])):
    rows = opp[o]
    obs = sum(s["nest"] for s in rows) / len(rows)
    exp = statistics.mean(brate[s["band"]] for s in rows)
    c = collections.Counter(s["band"] for s in rows)
    sh = " ".join(f"{b}:{c[b]/len(rows):.0%}"
                  for b in ("r0-50", "r51-150", "r151-300", "r301+"))
    print(f"{o:<24}{obs:>7.1%}{exp:>7.1%}{obs/exp:>6.2f}{len(rows):>6}   {sh}")
    res[o] = obs / exp

print("\nWITHIN round band, per opponent (n>=25 cells only):")
print(f"{'opponent':<24}" + "".join(f"{b:>18}" for b in
                                    ("r0-50", "r51-150", "r151-300", "r301+")))
for o in sorted(BIG, key=lambda o: -res[o]):
    line = f"{o:<24}"
    for b in ("r0-50", "r51-150", "r151-300", "r301+"):
        rows = [s for s in opp[o] if s["band"] == b]
        line += (f"{sum(s['nest'] for s in rows)/len(rows):>11.0%}(n={len(rows):<3})"
                 if len(rows) >= 25 else f"{'-':>18}")
    print(line)
print("\nfield rate in that band:      " +
      "".join(f"{brate[b]:>11.0%}(n={bt[b][1]:<3})" for b in
              ("r0-50", "r51-150", "r151-300", "r301+")))

# ---- split-half on the band-standardised O/E ------------------------------
by_match = collections.defaultdict(lambda: [0.0, 0.0])   # [nests, expected]
mopp = {}
for s in seeds:
    by_match[s["match"]][0] += s["nest"]
    by_match[s["match"]][1] += brate[s["band"]]
    mopp[s["match"]] = s["opp"]
om = collections.defaultdict(list)
for m in by_match:
    om[mopp[m]].append(m)
for o in om:
    om[o].sort(key=lambda m: created.get(m, ""))


def pearson(x, y):
    mx, my = statistics.mean(x), statistics.mean(y)
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


print("\n=== split-half on the BAND-STANDARDISED ratio O/E ===")
print(f"{'opponent':<24}{'h1 O/E':>8}{'h1 n':>7}{'h2 O/E':>9}{'h2 n':>7}")
x, y = [], []
for o in sorted(BIG):
    ms = om[o]
    if len(ms) < 6:
        continue
    a, b = ms[0::2], ms[1::2]
    ka = sum(by_match[m][0] for m in a); ea = sum(by_match[m][1] for m in a)
    kb = sum(by_match[m][0] for m in b); eb = sum(by_match[m][1] for m in b)
    na = sum(1 for s in seeds if s["match"] in set(a))
    nb = sum(1 for s in seeds if s["match"] in set(b))
    print(f"{o:<24}{ka/ea:>8.2f}{na:>7}{kb/eb:>9.2f}{nb:>7}")
    x.append(ka / ea); y.append(kb / eb)
print(f"  Pearson r = {pearson(x, y):.3f}  (n={len(x)} opponents, "
      "interleaved match split)")
