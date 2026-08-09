#!/usr/bin/env python3
"""Disentangle the discriminators.

(A) Mantel-Haenszel stratified BY GAME: removes opponent, map, seat, game
    length, our activity and win/loss entirely, because both plants being
    compared come from the same replay.  Only within-game varying predictors
    can be tested this way: distance, turret type, local clustering.
(B) Game-level analysis for the game-level predictors (opponent, our batk,
    won), unit = game, so the plants are not counted as independent.
(C) Multivariate logistic (L2) with opponent fixed effects.
(D) Collinearity audit.
"""
import csv, collections, math, random

D = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/tail/"
BASE = "/Users/junghard/Projects/Work/florent-code-game/corpus/"

rows = []
for r in csv.DictReader(open(D + "plants2.tsv"), delimiter="\t"):
    for k in ("our_team", "won", "turns", "lastrnd", "rnd", "d2", "died",
              "drnd", "life", "nb_same8", "nb_sameturret8", "nb_opp8",
              "nb_same16", "nb_opp16"):
        r[k] = int(r[k])
    r["fu"] = r["lastrnd"] - r["rnd"]
    rows.append(r)

batk = collections.Counter()
for r in csv.DictReader(open(BASE + "build_agg.tsv"), delimiter="\t"):
    if r["metric"] == "batk":
        batk[(r["file"], r["team"])] += int(r["n"])
for r in rows:
    r["our_batk"] = batk[(r["file"], str(r["our_team"]))]
    r["batk_rate"] = r["our_batk"] / max(1, r["lastrnd"])

T = 200
pop = [r for r in rows if r["side"] == "THEM" and r["fu"] >= T]
for r in pop:
    r["alive"] = 1 if ((not r["died"]) or r["life"] > T) else 0
print(f"T={T}  at-risk THEM plants n={len(pop)}  games={len(set(r['file'] for r in pop))}")


# ---------------- (A) Mantel-Haenszel stratified by game ----------------
def mh(pop, expo, name):
    """expo(r) -> 1 exposed / 0 unexposed / None excluded."""
    strata = collections.defaultdict(lambda: [[0, 0], [0, 0]])  # [exp][alive]
    for r in pop:
        e = expo(r)
        if e is None:
            continue
        strata[r["file"]][e][r["alive"]] += 1
    num = den = 0.0
    n1 = n0 = a1 = a0 = 0
    used = 0
    for f, t in strata.items():
        a, b = t[1][1], t[1][0]      # exposed alive/dead
        c, d = t[0][1], t[0][0]      # unexposed alive/dead
        n = a + b + c + d
        n1 += a + b; a1 += a; n0 += c + d; a0 += c
        if (a + b) == 0 or (c + d) == 0:
            continue                  # stratum carries no information
        used += 1
        num += a * d / n
        den += b * c / n
    orr = num / den if den else float("nan")
    # crude
    p1 = a1 / n1 if n1 else 0
    p0 = a0 / n0 if n0 else 0
    cor = (p1 / (1 - p1)) / (p0 / (1 - p0)) if 0 < p1 < 1 and 0 < p0 < 1 else float("nan")
    print(f"  {name:42s} exposed {p1:6.1%} (n={n1:5d})  unexposed {p0:6.1%} (n={n0:5d})"
          f"  crudeOR {cor:5.2f}  MH-OR(game-fixed) {orr:5.2f}  informative games {used}")
    return orr


print("\n(A) WITHIN-GAME (Mantel-Haenszel, game as stratum) -- opponent/map/seat/"
      "our-activity/win all differenced out")
mh(pop, lambda r: 1 if r["d2"] >= 18 else (0 if r["d2"] <= 8 else None),
   "far d2>=18 vs near d2<=8")
mh(pop, lambda r: 1 if r["d2"] > 10 else 0, "d2>10 vs d2<=10")
mh(pop, lambda r: 1 if r["kind"] == "sentinel" else 0, "sentinel vs gunner")
mh(pop, lambda r: 1 if r["nb_sameturret8"] >= 2 else (0 if r["nb_sameturret8"] == 0 else None),
   ">=2 friendly turrets within d2<=8 vs 0")
mh(pop, lambda r: 1 if r["nb_sameturret8"] >= 1 else 0, ">=1 friendly turret nearby vs 0")
mh(pop, lambda r: 1 if r["nb_same8"] >= 3 else (0 if r["nb_same8"] == 0 else None),
   ">=3 enemy buildings within d2<=8 vs 0")
mh(pop, lambda r: 1 if r["nb_opp8"] >= 3 else (0 if r["nb_opp8"] == 0 else None),
   ">=3 OUR buildings within d2<=8 vs 0")
mh(pop, lambda r: 1 if r["rnd"] >= 150 else 0, "planted r>=150 vs r<150 (within game)")

# ---------------- (B) game-level ----------------
print("\n(B) GAME-LEVEL (unit = game, mean of that game's at-risk plants)")
byg = collections.defaultdict(list)
for r in pop:
    byg[r["file"]].append(r)
games = []
for f, v in byg.items():
    games.append(dict(file=f, opp=v[0]["opp"], map=v[0]["map"], seat=v[0]["our_team"],
                      won=v[0]["won"], batk=v[0]["our_batk"], rate=v[0]["batk_rate"],
                      n=len(v), frac=sum(x["alive"] for x in v) / len(v),
                      last=v[0]["lastrnd"]))
print(f"  games={len(games)}  mean per-game survival fraction "
      f"{sum(g['frac'] for g in games)/len(games):.1%}")


def gshow(name, keyfn, minn=8, order=None):
    g = collections.defaultdict(list)
    for x in games:
        g[keyfn(x)].append(x)
    out = [(k, sum(y["frac"] for y in v) / len(v), len(v), sum(y["n"] for y in v))
           for k, v in g.items() if len(v) >= minn]
    out.sort(key=(lambda t: t[0]) if order == "key" else (lambda t: -t[1]))
    print(f"\n  -- {name}")
    for k, m, ng, npl in out:
        print(f"     {str(k):26s} mean per-game survival {m:6.1%}  games={ng:4d} plants={npl:5d}")
    return out


gshow("opponent", lambda x: x["opp"], minn=10)
gshow("our batk in game", lambda x: ("0" if x["batk"] == 0 else "1-49" if x["batk"] < 50
                                     else "50-199" if x["batk"] < 200 else
                                     "200-499" if x["batk"] < 500 else "500+"), order="key")
gshow("our batk PER ROUND", lambda x: ("<0.05" if x["rate"] < .05 else "0.05-0.2" if x["rate"] < .2
                                       else "0.2-0.5" if x["rate"] < .5 else "0.5+"), order="key")
gshow("won", lambda x: "WON" if x["won"] else "LOST")
gshow("seat", lambda x: f"seat{x['seat']}")

# ---------------- (D) collinearity audit ----------------
print("\n(D) COLLINEARITY AUDIT")
opp_map = collections.defaultdict(collections.Counter)
opp_batk = collections.defaultdict(list)
opp_won = collections.defaultdict(list)
opp_turr = collections.defaultdict(list)
opp_d2 = collections.defaultdict(list)
for g in games:
    opp_map[g["opp"]][g["map"]] += 1
    opp_batk[g["opp"]].append(g["rate"])
    opp_won[g["opp"]].append(g["won"])
for r in pop:
    opp_turr[r["opp"]].append(r["nb_sameturret8"])
    opp_d2[r["opp"]].append(r["d2"])
print("  opponent -> map spread (n maps / games), our batk rate, win rate, "
      "mean friendly-turrets-nearby, mean d2")
for o in sorted(opp_batk, key=lambda o: -len(opp_batk[o]))[:16]:
    ms = opp_map[o]
    print(f"    {o:24s} games={len(opp_batk[o]):4d} maps={len(ms):3d} "
          f"topmap={ms.most_common(1)[0][1]/len(opp_batk[o]):5.1%} "
          f"batkrate={sum(opp_batk[o])/len(opp_batk[o]):5.2f} "
          f"winrate={sum(opp_won[o])/len(opp_won[o]):5.1%} "
          f"turr8={sum(opp_turr[o])/max(1,len(opp_turr[o])):4.2f} "
          f"d2={sum(opp_d2[o])/max(1,len(opp_d2[o])):5.1f}")
