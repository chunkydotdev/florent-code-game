#!/usr/bin/env python3
"""Do NESTS add harm beyond the number of plants?  Stratify on seed count."""
import csv, collections
S = ("/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/"
     "628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/oppnest/")
G = [g for g in csv.DictReader(open(S + "games.tsv"), delimiter="\t")]
for g in G:
    for k in ("seeds", "nests", "home_bb_deaths", "bb_rounds", "won", "lastrnd"):
        g[k] = int(g[k])
print("home builder deaths per 1k builder-rounds, by nests WITHIN seed-count stratum")
print(f"{'seeds in game':<16}{'0 nests':>22}{'>=1 nest':>22}")
for lo, hi, lab in ((1,1,"1"),(2,2,"2"),(3,4,"3-4"),(5,99,"5+")):
    sub=[g for g in G if lo<=g["seeds"]<=hi]
    a=[g for g in sub if g["nests"]==0]; b=[g for g in sub if g["nests"]>=1]
    def rate(x):
        d=sum(g["bb_rounds"] for g in x); 
        return 1000*sum(g["home_bb_deaths"] for g in x)/d if d else float('nan')
    print(f"{lab:<16}{rate(a):>13.2f} (n={len(a):<4}){rate(b):>13.2f} (n={len(b):<4})")
print("\nsame, our WIN rate")
for lo, hi, lab in ((1,1,"1"),(2,2,"2"),(3,4,"3-4"),(5,99,"5+")):
    sub=[g for g in G if lo<=g["seeds"]<=hi]
    a=[g for g in sub if g["nests"]==0]; b=[g for g in sub if g["nests"]>=1]
    wa=sum(g["won"] for g in a)/len(a) if a else float('nan')
    wb=sum(g["won"] for g in b)/len(b) if b else float('nan')
    print(f"{lab:<16}{wa:>13.1%} (n={len(a):<4}){wb:>13.1%} (n={len(b):<4})")
print("\nreference: games with 0 seeds  ->", 
      f"{1000*sum(g['home_bb_deaths'] for g in G if g['seeds']==0)/sum(g['bb_rounds'] for g in G if g['seeds']==0):.2f}",
      f"per 1k bbr, win {sum(g['won'] for g in G if g['seeds']==0)/max(1,len([g for g in G if g['seeds']==0])):.1%}",
      f"(n={len([g for g in G if g['seeds']==0])})")
