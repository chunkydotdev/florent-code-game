#!/usr/bin/env python3
"""Label sensitivity: is 'nest rate' partly 'their seeds live long enough to
coexist'?  Recompute per opponent WITHOUT the coexistence requirement, and
report seed survival-to-30-rounds.  Also: does an opponent prior add anything
on top of a round-band prior?"""
import csv, collections, math, statistics, sys

B = "/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/oppnest/snap/"
S = ("/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/"
     "628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/oppnest/")
J = {r["file"]: r for r in csv.DictReader(open(B + "join.tsv"), delimiter="\t")}
ev = collections.defaultdict(list)
for r in csv.DictReader(open(B + "events.tsv"), delimiter="\t"):
    if r["file"] in J:
        ev[r["file"]].append((int(r["rnd"]), r["ev"], int(r["team"]), r["kind"],
                              int(r["x"]), int(r["y"]), int(r["d2_enemy"])))
TUR = ("gunner", "sentinel")
out = []
for f, rows in ev.items():
    j = J[f]; ours = int(j["our_team"]); them = 1 - ours
    rows.sort(key=lambda t: (t[0], t[1]))
    lastrnd = max(t[0] for t in rows)
    pend = collections.defaultdict(collections.deque); life = []
    for rnd, e, tm, kind, x, y, d2e in rows:
        if tm != them or kind not in TUR:
            continue
        k = (kind, x, y)
        if e == "BUILD":
            life.append([rnd, None, kind, x, y]); pend[k].append(len(life) - 1)
        elif pend[k]:
            life[pend[k].popleft()][1] = rnd
    for i, (rb, rd, kind, x, y) in enumerate(life):
        d2e = None
        for rnd, e, tm, kk, xx, yy, dd in rows:
            if e == "BUILD" and tm == them and kk == kind and xx == x and yy == y and rnd == rb:
                d2e = dd; break
        if d2e is None or d2e > 32 or lastrnd - rb < 30:
            continue
        pre = sum(1 for lb, ld, lk, lx, ly in life
                  if lb < rb and (ld is None or ld > rb)
                  and (lx - x) ** 2 + (ly - y) ** 2 <= 8)
        if pre:
            continue
        strict = loose = 0
        for lb, ld, lk, lx, ly in life:
            if not (rb < lb <= rb + 30) or (lx == x and ly == y):
                continue
            if (lx - x) ** 2 + (ly - y) ** 2 > 8:
                continue
            loose += 1
            if rd is None or rd > lb:
                strict += 1
        out.append(dict(opp=j["opp"], rnd=rb,
                        strict=1 if strict else 0, loose=1 if loose else 0,
                        alive30=1 if (rd is None or rd - rb >= 30) else 0,
                        lifetime=(rd - rb) if rd is not None else 9999))
print(f"seeds recomputed: {len(out)}", file=sys.stderr)

agg = collections.defaultdict(collections.Counter)
lif = collections.defaultdict(list)
for s in out:
    a = agg[s["opp"]]
    a["n"] += 1; a["strict"] += s["strict"]; a["loose"] += s["loose"]
    a["alive30"] += s["alive30"]
    lif[s["opp"]].append(min(s["lifetime"], 1000))
rows = [(o, a["n"], a["strict"] / a["n"], a["loose"] / a["n"],
         a["alive30"] / a["n"], statistics.median(lif[o]))
        for o, a in agg.items() if a["n"] >= 60]
rows.sort(key=lambda r: -r[2])
print(f"\n{'opponent':<24}{'n':>6}{'nest STRICT':>13}{'nest LOOSE':>12}"
      f"{'seed alive @30':>16}{'median seed life':>18}")
for o, n, st, lo, al, md in rows:
    print(f"{o:<24}{n:>6}{st:>13.1%}{lo:>12.1%}{al:>16.1%}"
          f"{(md if md < 1000 else float('inf')):>18.0f}")


def pearson(x, y):
    mx, my = statistics.mean(x), statistics.mean(y)
    sx = math.sqrt(sum((a - mx) ** 2 for a in x)); sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


print(f"\nr(strict, loose) across {len(rows)} opponents = "
      f"{pearson([r[2] for r in rows], [r[3] for r in rows]):.3f}")
print(f"r(strict, seed-alive-at-30)                  = "
      f"{pearson([r[2] for r in rows], [r[4] for r in rows]):.3f}")
print(f"r(loose,  seed-alive-at-30)                  = "
      f"{pearson([r[3] for r in rows], [r[4] for r in rows]):.3f}")

# ---- does opponent add over round band? (leave-one-match-out is overkill
#      here; use a simple 2-fold: odd/even seeds by match hash) --------------
seeds = list(csv.DictReader(open(S + "seeds.tsv"), delimiter="\t"))
for s in seeds:
    s["nest"] = int(s["nest"]); r = int(s["rnd"])
    s["band"] = ("r0-50" if r <= 50 else "r51-150" if r <= 150 else
                 "r151-300" if r <= 300 else "r301+")
ms = sorted({s["match"] for s in seeds})
fold = {m: i % 2 for i, m in enumerate(ms)}
for s in seeds:
    s["fold"] = fold[s["match"]]


def fit(rows, keyf):
    d = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        d[keyf(r)][0] += r["nest"]; d[keyf(r)][1] += 1
    g = sum(v[0] for v in d.values()) / sum(v[1] for v in d.values())
    return {k: (v[0] + 10 * g) / (v[1] + 10) for k, v in d.items()}, g


print("\n=== 2-fold (match-disjoint) out-of-sample Brier at the seed level ===")
for lab, keyf in (("global", lambda r: 0),
                  ("round band", lambda r: r["band"]),
                  ("opponent", lambda r: r["opp"]),
                  ("opponent x round band", lambda r: (r["opp"], r["band"]))):
    br = n = 0
    for f in (0, 1):
        tr = [s for s in seeds if s["fold"] != f]
        te = [s for s in seeds if s["fold"] == f]
        mdl, g = fit(tr, keyf)
        for s in te:
            p = mdl.get(keyf(s), g)
            br += (s["nest"] - p) ** 2; n += 1
    print(f"  {lab:<24} Brier {br/n:.4f}  n={n}")
