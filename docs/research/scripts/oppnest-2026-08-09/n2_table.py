#!/usr/bin/env python3
"""Per-opponent nest rate with MATCH-level and GAME-level cluster bootstrap CIs,
plus a cluster-permutation test on the between-opponent spread."""
import csv, collections, random, statistics, sys

S = ("/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/"
     "628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/oppnest/")
B = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/oppnest/snap/"

LM = {r["id"]: r for r in csv.DictReader(open(B + "league_matches.tsv"),
                                         delimiter="\t")}
seeds = list(csv.DictReader(open(S + "seeds.tsv"), delimiter="\t"))
games = list(csv.DictReader(open(S + "games.tsv"), delimiter="\t"))
for s in seeds:
    s["nest"] = int(s["nest"])
print(f"seeds {len(seeds)}  games {len(games)}", file=sys.stderr)

def meta(match, opp):
    r = LM.get(match)
    if not r:
        return None, None
    for side in ("A", "B"):
        if r[f"team{side}Name"] == opp:
            return r["createdAt"], r[f"team{side}Version"]
    return r["createdAt"], None

MT = {}
for s in seeds:
    if s["match"] not in MT:
        MT[s["match"]] = meta(s["match"], s["opp"])
for s in seeds:
    s["created"], s["oppver"] = MT[s["match"]]

# ---- aggregate at match and game level ------------------------------------
by_match = collections.defaultdict(lambda: [0, 0])   # match -> [nests, seeds]
match_opp, match_created = {}, {}
by_game = collections.defaultdict(lambda: [0, 0])
game_match = {}
for s in seeds:
    by_match[s["match"]][0] += s["nest"]; by_match[s["match"]][1] += 1
    by_game[s["file"]][0] += s["nest"];   by_game[s["file"]][1] += 1
    match_opp[s["match"]] = s["opp"]
    match_created[s["match"]] = s["created"]
    game_match[s["file"]] = s["match"]

opp_matches = collections.defaultdict(list)
for m, o in match_opp.items():
    opp_matches[o].append(m)
opp_games = collections.defaultdict(list)
for f in by_game:
    opp_games[match_opp[game_match[f]]].append(f)

rng = random.Random(20260809)

def boot_ci(units, tab, reps=4000):
    """cluster bootstrap of the pooled rate; units are cluster keys."""
    if not units:
        return (float("nan"), float("nan"))
    out = []
    n = len(units)
    for _ in range(reps):
        k = d = 0
        for _ in range(n):
            a, b = tab[units[rng.randrange(n)]]
            k += a; d += b
        out.append(k / d if d else 0.0)
    out.sort()
    return out[int(0.025 * reps)], out[int(0.975 * reps) - 1]

rows = []
for opp, ms in opp_matches.items():
    k = sum(by_match[m][0] for m in ms)
    n = sum(by_match[m][1] for m in ms)
    gs = opp_games[opp]
    lo_m, hi_m = boot_ci(ms, by_match)
    lo_g, hi_g = boot_ci(gs, by_game)
    rows.append((opp, len(ms), len(gs), n, k, k / n, lo_m, hi_m, lo_g, hi_g))
rows.sort(key=lambda r: -r[5])

tot_k = sum(r[4] for r in rows); tot_n = sum(r[3] for r in rows)
print(f"\nCORPUS-WIDE nest rate {tot_k}/{tot_n} = {tot_k/tot_n:.1%}\n")
print(f"{'opponent':<26}{'mtch':>5}{'game':>5}{'seed':>6}{'nest':>6}"
      f"{'rate':>8}   {'95% CI (match-clustered)':<26}{'95% CI (game)':<22}")
for opp, nm, ng, n, k, r, lm_, hm, lg, hg in rows:
    print(f"{opp:<26}{nm:>5}{ng:>5}{n:>6}{k:>6}{r:>8.1%}   "
          f"[{lm_:>5.1%},{hm:>6.1%}]{'':<12}[{lg:>5.1%},{hg:>6.1%}]")

# ---- cluster-permutation test on the spread -------------------------------
BIG = [r[0] for r in rows if r[3] >= 60]
print(f"\nopponents with >=60 seeds: {len(BIG)}")
allm = [m for m in by_match]
sizes = {o: len(opp_matches[o]) for o in BIG}

def spread(assign):
    """weighted between-opponent variance of the pooled rate, BIG opponents."""
    agg = collections.defaultdict(lambda: [0, 0])
    for m, o in assign.items():
        if o in sizes:
            agg[o][0] += by_match[m][0]; agg[o][1] += by_match[m][1]
    tk = sum(v[0] for v in agg.values()); tn = sum(v[1] for v in agg.values())
    gm = tk / tn
    return sum(v[1] * (v[0] / v[1] - gm) ** 2 for v in agg.values()) / tn, agg

obs, aggobs = spread(match_opp)
mx = max(v[0] / v[1] for v in aggobs.values())
mn = min(v[0] / v[1] for v in aggobs.values())
perm_sp, perm_ratio = [], []
for _ in range(4000):
    pool = allm[:]
    rng.shuffle(pool)
    a, i = {}, 0
    for o in BIG:
        for m in pool[i:i + sizes[o]]:
            a[m] = o
        i += sizes[o]
    sp, ag = spread(a)
    perm_sp.append(sp)
    rr = [v[0] / v[1] for v in ag.values() if v[1]]
    perm_ratio.append((max(rr), min(rr)))
p = (1 + sum(1 for v in perm_sp if v >= obs)) / (1 + len(perm_sp))
print(f"observed weighted between-opponent variance {obs:.5f}; "
      f"permutation mean {statistics.mean(perm_sp):.5f}, "
      f"p95 {sorted(perm_sp)[int(.95*len(perm_sp))]:.5f}, p = {p:.4f}")
print(f"observed max/min opponent rate {mx:.1%} / {mn:.1%} (ratio "
      f"{mx/mn:.1f}x); permutation median max {statistics.median(x[0] for x in perm_ratio):.1%}"
      f" min {statistics.median(x[1] for x in perm_ratio):.1%} "
      f"(null spread {statistics.median(x[0]-x[1] for x in perm_ratio):.1%}pp "
      f"vs observed {mx-mn:.1%}pp)")

# ---- intra-cluster correlation --------------------------------------------
def icc(tab):
    ks = [v[0] for v in tab.values()]; ns = [v[1] for v in tab.values()]
    tk, tn = sum(ks), sum(ns)
    p0 = tk / tn
    num = sum((k - n * p0) ** 2 - n * p0 * (1 - p0) for k, n in zip(ks, ns))
    den = p0 * (1 - p0) * sum(n * (n - 1) for n in ns)
    return num / den if den else float("nan")
print(f"\nICC of the nest label within GAME  = {icc(by_game):.3f}")
print(f"ICC of the nest label within MATCH = {icc(by_match):.3f}")
sz = [v[1] for v in by_match.values()]
print(f"mean seeds/match {statistics.mean(sz):.1f} -> design effect "
      f"~{1 + (statistics.mean(sz)-1)*icc(by_match):.2f}")
