#!/usr/bin/env python3
"""Q1: how do the games end? cond x who x turns, Ouroboros vs controls."""
import csv, sys, collections, statistics
ROOT = "/Users/junghard/Projects/Work/florent-code-game"

def load(t):
    meta = {r["file"]: r for r in csv.DictReader(open(f"{ROOT}/scratchpad/ouro/files_{t}.tsv"), delimiter="\t")}
    cen = {r["file"]: r for r in csv.DictReader(open(f"{ROOT}/scratchpad/ouro/census_{t}.tsv"), delimiter="\t")}
    out = []
    for f, m in meta.items():
        c = cen.get(f)
        if not c: continue
        us = m["us_side"]           # 'a' or 'b'  (from team NAMES, not winnerSide)
        winner = c["winner"]        # 'A'/'B'/'-' from the replay binary
        our_won_replay = (winner.lower() == us)
        r = dict(m); r.update(c)
        r["us"] = us; r["them"] = "b" if us == "a" else "a"
        r["won_replay"] = our_won_replay
        r["rounds"] = int(c["rounds"])
        out.append(r)
    return out

def pct(n, d): return "%.1f%%" % (100.0*n/d) if d else "n/a"

for t in sys.argv[1:]:
    G = load(t)
    n = len(G)
    # CONTROL: does the meta's our_won agree with the replay winner?
    agree = sum(1 for g in G if (g["our_won"] == "1") == g["won_replay"])
    print("="*70)
    print(f"{t}: n={n} games, our_won(replay)={sum(g['won_replay'] for g in G)} "
          f"share={sum(g['won_replay'] for g in G)/n:.3f}")
    print(f"  meta our_won vs replay winner agreement: {agree}/{n}")
    tab = collections.Counter()
    for g in G:
        cond = g["win_condition"]
        who = "US" if g["won_replay"] else "THEM"
        tab[(cond, who)] += 1
    for k in sorted(tab): print("   %-22s %-5s %3d  (%s)" % (k[0], k[1], tab[k], pct(tab[k], n)))
    # turn profile for core_destroyed
    for who in ("US", "THEM"):
        rs = sorted(g["rounds"] for g in G if g["win_condition"] == "core_destroyed"
                    and (g["won_replay"] == (who == "US")))
        if not rs: continue
        q = lambda p: rs[min(len(rs)-1, int(p*len(rs)))]
        print(f"   core kill BY {who}: n={len(rs)} min={rs[0]} p25={q(.25)} med={q(.5)} p75={q(.75)} max={rs[-1]}"
              f"  <100r={sum(1 for x in rs if x<100)} <200r={sum(1 for x in rs if x<200)}")
