#!/usr/bin/env python3
"""Does OPPONENT VERSION explain nest-rate variation beyond match-to-match noise?
Permutation test: within each opponent, shuffle the version labels ACROSS THAT
OPPONENT'S MATCHES (preserving how many matches each version got), recompute the
weighted between-version variance, compare with the observed.  Match clustering
is preserved exactly because matches are the permuted unit."""
import csv, collections, random, statistics

S = ("/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/"
     "628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/oppnest/")
B = S + "snap/"
LM = {r["id"]: r for r in csv.DictReader(open(B + "league_matches.tsv"),
                                         delimiter="\t")}
seeds = list(csv.DictReader(open(S + "seeds.tsv"), delimiter="\t"))
mv, mo = {}, {}
bym = collections.defaultdict(lambda: [0, 0])
for s in seeds:
    bym[s["match"]][0] += int(s["nest"]); bym[s["match"]][1] += 1
    mo[s["match"]] = s["opp"]
    r = LM.get(s["match"])
    v = None
    if r:
        for side in ("A", "B"):
            if r[f"team{side}Name"] == s["opp"]:
                v = r[f"team{side}Version"]
    mv[s["match"]] = v

rng = random.Random(7)
print(f"{'opponent':<24}{'vers':>5}{'mtch':>6}{'obs var':>10}{'null mean':>11}{'p':>8}")
tot_obs = tot_null = 0.0
allp = []
for o in sorted({mo[m] for m in bym}):
    ms = [m for m in bym if mo[m] == o and mv[m]]
    if len(ms) < 6:
        continue
    labs = [mv[m] for m in ms]
    if len(set(labs)) < 2:
        continue

    def var(assign):
        d = collections.defaultdict(lambda: [0, 0])
        for m, v in assign:
            d[v][0] += bym[m][0]; d[v][1] += bym[m][1]
        tk = sum(x[0] for x in d.values()); tn = sum(x[1] for x in d.values())
        g = tk / tn
        return sum(x[1] * (x[0] / x[1] - g) ** 2 for x in d.values()) / tn

    obs = var(list(zip(ms, labs)))
    null = []
    for _ in range(3000):
        p = labs[:]
        rng.shuffle(p)
        null.append(var(list(zip(ms, p))))
    pv = (1 + sum(1 for v in null if v >= obs)) / (1 + len(null))
    allp.append(pv)
    tot_obs += obs; tot_null += statistics.mean(null)
    print(f"{o:<24}{len(set(labs)):>5}{len(ms):>6}{obs:>10.4f}"
          f"{statistics.mean(null):>11.4f}{pv:>8.3f}")
print(f"\nsummed observed between-version variance {tot_obs:.4f} vs "
      f"permutation expectation {tot_null:.4f}")
print(f"opponents tested {len(allp)}; min p {min(allp):.3f}; "
      f"how many p<0.05: {sum(1 for p in allp if p < 0.05)}")
