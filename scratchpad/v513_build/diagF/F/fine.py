import sys, os
V="/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/82720aae-f502-4b10-9dd5-ad5f55d16b94/scratchpad/v512_failures"
sys.path.insert(0,V)
import walk, feat
R={r["tag"]:r for r in feat.load_batch()}
tag=sys.argv[1]; lo=int(sys.argv[2]); hi=int(sys.argv[3])
mb,turns,winner,cond=walk.load(os.path.join(V,"replays",tag+".replay26"))
ourteam=0 if R[tag]["ord"]=="A" else 1; us="AB"[ourteam]
players={}
for rnd,k,p in walk.events(turns):
    if k=="players": players[rnd]=p
for r in sorted(players):
    if lo<=r<=hi:
        a=players[r].get(us,{})
        print("r%-4d ti=%-5s ammo=%-5s tic=%-4s" % (r,a.get("ti"),a.get("ammo"),a.get("tic")))
