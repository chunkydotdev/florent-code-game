"""GATE 5a-bis (PREREG-loki19 Amendment 1b): our INSERT reach, CONTROL arm,
live unrated, this leg's own games, PER CELL, never pooled.

Population is defined by matchId, read from the leg's own arm files; opponent
name and our side come from replay_archive/<matchId>.meta.json (the platform's
own record), never from a hand-written table.
"""
import csv, json, sys, glob
from collections import defaultdict

ARMS = {
 "CTRL_W1": "scratchpad/arm_loki19_ctrl_w1.txt",
 "CTRL_W2": "scratchpad/arm_unrated_v104_20260811T052031Z.txt",
 "TREAT_W1": "scratchpad/arm_loki19_treat_w1.txt",
 "TREAT_W2": "scratchpad/arm_unrated_v108_20260811T053112Z.txt",
}

def match_ids(path):
    out=[]
    for line in open(path):
        i=line.find('"matchId": "')
        if i>=0: out.append(line[i+12:].split('"')[0])
    return out

meta={}   # matchId -> (opp, our_team_idx, ourver)
arm_of={} # matchId -> arm
for arm,path in ARMS.items():
    for mid in match_ids(path):
        arm_of[mid]=arm
        d=json.load(open(f"replay_archive/{mid}.meta.json"))
        if d["teamBName"]=="OpenSverige":
            meta[mid]=(d["teamAName"],1,d["teamBVersion"],d["createdAt"])
        elif d["teamAName"]=="OpenSverige":
            meta[mid]=(d["teamBName"],0,d["teamAVersion"],d["createdAt"])
        else:
            sys.exit(f"NEITHER SIDE IS OURS in {mid}")

# throws.tsv keyed by file "<matchId>_game_N.replay26"
stat=defaultdict(lambda: defaultdict(lambda:[0,0]))   # arm -> cell -> [reached, n]
opp_stat=defaultdict(lambda: defaultdict(lambda:[0,0]))
games=defaultdict(lambda: defaultdict(set))
reached_vals=set()
for r in csv.DictReader(open("corpus/throws.tsv"),delimiter="\t"):
    mid=r["file"].split("_game_")[0]
    if mid not in arm_of: continue
    if r["kind"]!="INSERT": continue
    opp,ours,ver,_=meta[mid]; arm=arm_of[mid]
    games[arm][opp].add(r["file"])
    reached_vals.add(r["reached"])
    tgt = stat if int(r["bteam"])==ours else opp_stat
    tgt[arm][opp][1]+=1
    tgt[arm][opp][0]+=int(r["reached"])

print("=== GATE 5a-bis — OUR INSERT REACH, PER CELL (prereg Amendment 1b) ===")
for arm in ("CTRL_W1","CTRL_W2","TREAT_W1","TREAT_W2"):
    print(f"\n-- {arm} --   ourver={sorted({meta[m][2] for m in arm_of if arm_of[m]==arm})}")
    tot=[0,0]
    for cell in sorted(stat[arm], key=lambda c:-stat[arm][c][1]):
        rch,n=stat[arm][cell]; orch,on=opp_stat[arm][cell]
        tot[0]+=rch; tot[1]+=n
        band = ">30 premise holds" if n and rch/n>0.30 else ("20-30 AMBIGUOUS" if n and rch/n>0.20 else "<=20 pre-quiet")
        print(f"  {cell:24} ours {rch:4}/{n:<4} = {rch/n*100 if n else 0:5.1f}%  [{band:17}]"
              f"   | THEIRS {orch:4}/{on:<4} = {orch/on*100 if on else 0:5.1f}%   games={len(games[arm][cell])}")
    print(f"  (pooled {tot[0]}/{tot[1]} = {tot[0]/tot[1]*100:.1f}% — BANNED BY AMENDMENT 1b, printed only as a decoder checksum)")

print("\n=== CONTROL ARM POOLED ACROSS WINDOWS, PER CELL (the gate as written) ===")
cells=defaultdict(lambda:[0,0]); cellsg=defaultdict(set); cello=defaultdict(lambda:[0,0])
for arm in ("CTRL_W1","CTRL_W2"):
    for cell,(rch,n) in stat[arm].items():
        cells[cell][0]+=rch; cells[cell][1]+=n; cellsg[cell]|=games[arm][cell]
        cello[cell][0]+=opp_stat[arm][cell][0]; cello[cell][1]+=opp_stat[arm][cell][1]
for cell in sorted(cells,key=lambda c:-cells[c][1]):
    rch,n=cells[cell]; orch,on=cello[cell]
    band = ">30" if rch/n>0.30 else ("20-30" if rch/n>0.20 else "<=20")
    print(f"  {cell:24} {rch:4}/{n:<4} = {rch/n*100:5.1f}%  band {band:5}  games={len(cellsg[cell])}"
          f"   | theirs {orch}/{on} = {orch/on*100 if on else 0:.1f}%")

print("\n=== INSTRUMENT CONTROLS (each must come out the other way) ===")
print(f"  C1 reached column is not constant: distinct values = {sorted(reached_vals)}  "
      f"{'OK' if len(reached_vals)>1 else 'FAIL — a constant column validates anything'}")
tot_ours=sum(v[1] for a in stat for v in stat[a].values())
tot_theirs=sum(v[1] for a in opp_stat for v in opp_stat[a].values())
print(f"  C2 opponent column is alive (not our zero): ours n={tot_ours}, theirs n={tot_theirs} "
      f"{'OK' if tot_theirs>0 else 'FAIL'}")
n_files=len({f for a in games for c in games[a] for f in games[a][c]})
print(f"  C3 games with >=1 INSERT: {n_files} of 100 expected leg games")
print(f"  C4 matches resolved: {len(arm_of)} (expect 20); sides resolved: {len(meta)}")
