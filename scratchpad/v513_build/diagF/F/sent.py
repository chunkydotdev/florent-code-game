import sys, os, collections
V="/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/82720aae-f502-4b10-9dd5-ad5f55d16b94/scratchpad/v512_failures"
sys.path.insert(0,V)
import walk, feat
R={r["tag"]:r for r in feat.load_batch()}
def d2(a,b): return (a[0]-b[0])**2+(a[1]-b[1])**2
for tag in sys.argv[1:]:
    mb,turns,winner,cond=walk.load(os.path.join(V,"replays",tag+".replay26"))
    W,H,tiles,cores=walk.parse_map(mb)
    ourteam=0 if R[tag]["ord"]=="A" else 1
    oc=[c for c in cores if c["team"]==ourteam][0]; ec=[c for c in cores if c["team"]!=ourteam][0]
    ents={};born={};died={};fires=[]
    for rnd,k,p in walk.events(turns):
        if k=="place":
            if p.id not in ents: ents[p.id]={"team":p.team,"kind":p.kind,"birth":tuple(p.pos)}; born[p.id]=rnd
        elif k=="remove": died[p["id"]]=rnd
        elif k=="fire": fires.append((rnd,tuple(p["from"]),tuple(p["to"])))
    print("==",tag,"rounds",len(turns))
    for i,e in sorted(ents.items(),key=lambda kv:born[kv[0]]):
        if e["team"]!=ourteam or e["kind"] not in("sentinel","gunner"): continue
        sh=[f for f in fires if f[1]==e["birth"]]
        print("  OUR %-9s#%-4d r%-4d..%-6s at %-9s d2_enemycore=%-4d d2_ourcore=%-4d shots=%d" %
              (e["kind"],i,born[i],died.get(i,"alive"),str(e["birth"]),d2(e["birth"],ec["pos"]),d2(e["birth"],oc["pos"]),len(sh)))
