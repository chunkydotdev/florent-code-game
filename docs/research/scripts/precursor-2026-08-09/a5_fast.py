import csv, collections, math
S="/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/628d1383-b855-455c-b911-2e000e1ba0b8/scratchpad/precursor/"
B="/Users/junghard/Projects/Work/florent-code-game/corpus/"
J={r["file"]:r for r in csv.DictReader(open(B+"join.tsv"),delimiter="\t")}
P=list(csv.DictReader(open(S+"plants2.tsv"),delimiter="\t"))
for p in P:
    for k in ("rnd","d2","loiter36","nb36_m1","nb36_max_w10","nb36_distinct_w10",
              "pre_t8","lag_x0","lastrnd","reuse_idx","seat","moves_w10","age"):
        p[k]=int(p[k])
SEED=[p for p in P if p["pre_t8"]==0 and p["lastrnd"]-p["rnd"]>=30]
FAST=lambda p: 0<=p["lag_x0"]<=10
print(f"seeds {len(SEED)}, FAST nests (2nd turret within 10 rnd) {sum(1 for p in SEED if FAST(p))} "
      f"= {sum(1 for p in SEED if FAST(p))/len(SEED):.1%}")
def tab(name,keyf,buckets):
    print(f"  {name}")
    for lab,f in buckets:
        sub=[p for p in SEED if f(keyf(p))]
        if len(sub)<30: continue
        k=sum(1 for p in sub if FAST(p))
        print(f"    {lab:<14} {k:>5}/{len(sub):<5} = {k/len(sub):6.1%}")
tab("planter loiter36",lambda p:p["loiter36"],
    [("0-1",lambda v:v<=1),("2-4",lambda v:2<=v<=4),("5-9",lambda v:5<=v<=9),
     ("10-19",lambda v:10<=v<=19),("20-49",lambda v:20<=v<=49),("50+",lambda v:v>=50)])
tab("enemy builders in zone at t-1",lambda p:p["nb36_m1"],
    [(str(i),lambda v,i=i:v==i) for i in range(5)]+[("5+",lambda v:v>=5)])
tab("distinct enemy builders seen in the 10 rounds before",lambda p:p["nb36_distinct_w10"],
    [("1",lambda v:v<=1),("2",lambda v:v==2),("3",lambda v:v==3),("4+",lambda v:v>=4)])
tab("round planted",lambda p:p["rnd"],
    [("r0-50",lambda v:v<=50),("r51-150",lambda v:51<=v<=150),
     ("r151-300",lambda v:151<=v<=300),("r301+",lambda v:v>=301)])
