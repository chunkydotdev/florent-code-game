#!/usr/bin/env python3
"""Does nest rate predict anything we care about?
   per-opponent: our win rate, our home builder deaths per 1k builder-rounds.
   plus a WITHIN-opponent game-level check (nests that game vs harm that game)."""
import csv, collections, math, statistics

S = ("/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/"
     "628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/oppnest/")

games = list(csv.DictReader(open(S + "games.tsv"), delimiter="\t"))
for g in games:
    for k in ("won", "plants", "seeds", "nests", "our_bb_built", "our_bb_died",
              "home_bb_deaths", "bb_rounds", "lastrnd", "seat"):
        g[k] = int(g[k])
print(f"games {len(games)}  (all attributed ladder games, seeds or not)")


def pearson(x, y):
    mx, my = statistics.mean(x), statistics.mean(y)
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


agg = collections.defaultdict(lambda: collections.Counter())
mset = collections.defaultdict(set)
for g in games:
    a = agg[g["opp"]]
    a["games"] += 1; a["won"] += g["won"]; a["seeds"] += g["seeds"]
    a["nests"] += g["nests"]; a["plants"] += g["plants"]
    a["hbd"] += g["home_bb_deaths"]; a["bbr"] += g["bb_rounds"]
    a["bbd"] += g["our_bb_died"]; a["rounds"] += g["lastrnd"]
    mset[g["opp"]].add(g["match"])

rows = []
for o, a in agg.items():
    if a["seeds"] < 60:
        continue
    rows.append((o, len(mset[o]), a["games"], a["seeds"],
                 a["nests"] / a["seeds"], a["won"] / a["games"],
                 1000 * a["hbd"] / a["bbr"], a["hbd"] / a["games"],
                 a["plants"] / a["games"], a["bbr"] / a["games"],
                 a["rounds"] / a["games"]))
rows.sort(key=lambda r: -r[4])
print(f"\n{'opponent':<24}{'m':>4}{'games':>6}{'seeds':>6}{'nest%':>7}"
      f"{'ourwin%':>9}{'homeBBdeath/1k bbr':>20}{'homeBBd/game':>13}"
      f"{'plants/game':>12}{'rounds/game':>12}")
for r in rows:
    print(f"{r[0]:<24}{r[1]:>4}{r[2]:>6}{r[3]:>6}{r[4]:>7.1%}{r[5]:>9.1%}"
          f"{r[6]:>20.2f}{r[7]:>13.1f}{r[8]:>12.1f}{r[10]:>12.0f}")

nest = [r[4] for r in rows]
print(f"\nacross {len(rows)} opponents (each is one point):")
for lab, i in (("our win rate", 5), ("home BB deaths per 1k builder-rounds", 6),
               ("home BB deaths per game", 7), ("enemy plants per game", 8),
               ("game length", 10)):
    print(f"  r(nest rate, {lab:<38}) = {pearson(nest, [r[i] for r in rows]):+.3f}")

# ---- WITHIN-opponent, game level -----------------------------------------
print("\n=== WITHIN-opponent, game level: nests that game vs harm that game ===")
print("(opponent-demeaned, games with >=1 seed)")
sub = [g for g in games if g["seeds"] >= 1]
mu = collections.defaultdict(lambda: [0.0, 0.0, 0.0, 0])
for g in sub:
    m = mu[g["opp"]]
    m[0] += g["nests"]; m[1] += 1000 * g["home_bb_deaths"] / max(g["bb_rounds"], 1)
    m[2] += g["won"]; m[3] += 1
dx, dy, dw = [], [], []
for g in sub:
    m = mu[g["opp"]]
    dx.append(g["nests"] - m[0] / m[3])
    dy.append(1000 * g["home_bb_deaths"] / max(g["bb_rounds"], 1) - m[1] / m[3])
    dw.append(g["won"] - m[2] / m[3])
print(f"  n={len(sub)} games; r(nests_in_game, home BB deaths/1k bbr) "
      f"= {pearson(dx, dy):+.3f}")
print(f"  n={len(sub)} games; r(nests_in_game, we won)                "
      f"= {pearson(dx, dw):+.3f}")

# raw dose-response
print("\n  home BB deaths per 1k builder-rounds by nests formed that game:")
d = collections.defaultdict(lambda: [0, 0, 0])
for g in sub:
    b = min(g["nests"], 4)
    d[b][0] += g["home_bb_deaths"]; d[b][1] += g["bb_rounds"]; d[b][2] += 1
for b in sorted(d):
    v = d[b]
    print(f"    {b}{'+' if b == 4 else ' '} nests: "
          f"{1000*v[0]/v[1]:>6.2f}   games={v[2]}")

# and by seeds (plants), to separate "they planted a lot" from "they nested"
print("\n  same, by SEEDS (lone plants included) that game:")
d = collections.defaultdict(lambda: [0, 0, 0])
for g in sub:
    b = min(g["seeds"], 6)
    d[b][0] += g["home_bb_deaths"]; d[b][1] += g["bb_rounds"]; d[b][2] += 1
for b in sorted(d):
    v = d[b]
    print(f"    {b}{'+' if b == 6 else ' '} seeds: "
          f"{1000*v[0]/v[1]:>6.2f}   games={v[2]}")
