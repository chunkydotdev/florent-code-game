import os,sys,glob
sys.path.insert(0,"/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/82720aae-f502-4b10-9dd5-ad5f55d16b94/scratchpad/v512_failures")
import walk
ORD={"glacierkeep_g5":"B","glacierkeep_g7":"B","glacierkeep_g0":"A",
     "nordkap_g1":"B","nordkap_g3":"B","atoll_g2":"A"}
for d in ("replays","replays2"):
    print("---",d)
    for f in sorted(glob.glob(os.path.join(d,"*.replay26"))):
        tag=os.path.basename(f)[:-len(".replay26")]
        mb,turns,w,c=walk.load(f)
        players={}
        for rnd,k,p in walk.events(turns):
            if k=="players": players[rnd]=p
        last=players[max(players)]
        us=ORD[tag]; them="B" if us=="A" else "A"
        print("  %-16s our_tic=%-6s their_tic=%-6s" % (tag,last.get(us,{}).get("tic",0),last.get(them,{}).get("tic",0)))
