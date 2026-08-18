import sys, os, collections, statistics
V="/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/82720aae-f502-4b10-9dd5-ad5f55d16b94/scratchpad/v512_failures"
sys.path.insert(0,V)
import walk, feat
rows=feat.load_batch()
print("tag           n    tic  min_ti med_ti  ti_at_end  ammo_conv  ammo_sh(=/10) med_ammo  pinned_rounds(ti stuck same val>=20r)")
tot=[]
for R in rows:
    tag=R["tag"]
    mb,turns,winner,cond=walk.load(os.path.join(V,"replays",tag+".replay26"))
    ourteam=0 if R["ord"]=="A" else 1; us="AB"[ourteam]
    players={}
    for rnd,k,p in walk.events(turns):
        if k=="players": players[rnd]=p
    ks=sorted(players)
    ti=[players[r].get(us,{}).get("ti",0) for r in ks]
    am=[players[r].get(us,{}).get("ammo",0) for r in ks]
    tic=players[ks[-1]].get(us,{}).get("tic",0)
    conv=sum(max(0,am[i]-am[i-1]) for i in range(1,len(am)))
    # longest-run pin
    best=0;cur=1
    for i in range(1,len(ti)):
        cur = cur+1 if ti[i]==ti[i-1] else 1
        best=max(best,cur)
    med=statistics.median(ti)
    print("%-13s %-4d %-5d %-6d %-6.0f %-10d %-10d %-13d %-8.0f %d" %
          (tag,len(ks),tic,min(ti),med,ti[-1],conv,conv//10,statistics.median(am),best))
    tot.append((tag,tic,med,conv))
print()
print("games with tic==0: %d/%d" % (sum(1 for t in tot if t[1]==0), len(tot)))
print("median bank across games:", statistics.median(t[2] for t in tot))
print("median ammo converted:", statistics.median(t[3] for t in tot))
