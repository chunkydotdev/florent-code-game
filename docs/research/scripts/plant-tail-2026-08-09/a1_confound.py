#!/usr/bin/env python3
"""Step 1: the round-built confound. How much of the 41.4% 'never dies' is just
'built with no game left'?"""
import csv, collections, sys

P = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/tail/plants.tsv"
rows = list(csv.DictReader(open(P), delimiter="\t"))
for r in rows:
    for k in ("rnd", "d2", "died", "drnd", "life", "lastrnd", "turns",
              "nb_enemy8", "nb_enemyturret8", "nb_our8", "nb_enemy16", "nb_our16", "won"):
        r[k] = int(r[k])
    r["fu"] = r["lastrnd"] - r["rnd"]        # follow-up rounds available
print(f"plants: {len(rows)}")

# sanity: lastrnd vs turns
d = collections.Counter(r["lastrnd"] - r["turns"] for r in rows)
print("lastrnd-turns distribution (top):", d.most_common(5))

n = len(rows)
died = sum(r["died"] for r in rows)
print(f"\nUNCONTROLLED: died {died} ({died/n:.1%})  survived {n-died} ({(n-died)/n:.1%})")

# --- follow-up time available for the survivors vs the dead
def q(v, p):
    v = sorted(v); return v[int(p*(len(v)-1))]
surv = [r for r in rows if not r["died"]]
dead = [r for r in rows if r["died"]]
print(f"\nfollow-up (lastrnd-rnd) available:")
for nm, g in (("survivors", surv), ("died", dead)):
    fu = [r["fu"] for r in g]
    print(f"  {nm:10s} n={len(g):5d} p10={q(fu,.1):4d} med={q(fu,.5):4d} p90={q(fu,.9):4d}")
print(f"  survivors with <50 rounds of game left: "
      f"{sum(1 for r in surv if r['fu']<50)} ({sum(1 for r in surv if r['fu']<50)/len(surv):.1%})")
print(f"  survivors with <100 rounds left: {sum(1 for r in surv if r['fu']<100)} "
      f"({sum(1 for r in surv if r['fu']<100)/len(surv):.1%})")
print(f"  survivors with <200 rounds left: {sum(1 for r in surv if r['fu']<200)} "
      f"({sum(1 for r in surv if r['fu']<200)/len(surv):.1%})")

# --- censored survival: S(t) = fraction still alive t rounds after plant,
# among plants that had >= t rounds of game left (no censoring inside window)
def surv_at(g, t):
    elig = [r for r in g if r["fu"] >= t]
    if not elig:
        return None, 0
    alive = sum(1 for r in elig if (not r["died"]) or r["life"] > t)
    return alive/len(elig), len(elig)

print("\nCENSORED SURVIVAL (whole population):")
for t in (10, 25, 50, 100, 200, 400):
    s, k = surv_at(rows, t)
    print(f"  S({t:3d}) = {s:.1%}   n_at_risk={k}")

# --- restrict to early plants
for cut in (200, 500):
    g = [r for r in rows if r["rnd"] < cut]
    dd = sum(r["died"] for r in g)
    print(f"\nplants built before r{cut}: n={len(g)}  died={dd/len(g):.1%}  survived={(len(g)-dd)/len(g):.1%}")

# --- the honest control: plants with >=200 rounds of game left
g = [r for r in rows if r["fu"] >= 200]
dd = sum(1 for r in g if r["died"] and r["life"] <= 200)
print(f"\nCONTROLLED (>=200 rounds of game left, n={len(g)}): "
      f"dead within 200 rounds {dd/len(g):.1%}, alive at +200 {(len(g)-dd)/len(g):.1%}")

# how many of the 2653 'survivors' are explained by short follow-up:
# a survivor is 'trivial' if fu < median lifetime-scale threshold
for thr in (14, 50, 100):
    triv = sum(1 for r in surv if r["fu"] < thr)
    print(f"  survivors with fu < {thr}: {triv} = {triv/n:.1%} of all plants "
          f"({triv/len(surv):.1%} of survivors)")
