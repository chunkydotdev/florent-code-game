import sys, os, collections
V="/private/tmp/claude-501/-Users-junghard-Projects-Work-florent-code-game/82720aae-f502-4b10-9dd5-ad5f55d16b94/scratchpad/v512_failures"
sys.path.insert(0,V)
import walk, feat
R={r["tag"]:r for r in feat.load_batch()}
tag=sys.argv[1]
mb,turns,winner,cond=walk.load(os.path.join(V,"replays",tag+".replay26"))
W,H,tiles,cores=walk.parse_map(mb)
ourteam=0 if R[tag]["ord"]=="A" else 1
us="AB"[ourteam]
players={}
builds=collections.Counter()   # our builds by kind, cumulative -> scale
ents={}
born={}
died={}
for rnd,k,p in walk.events(turns):
    if k=="players": players[rnd]=p
    elif k=="place":
        if p.id not in ents:
            ents[p.id]={"team":p.team,"kind":p.kind,"birth":tuple(p.pos)}
            born[p.id]=rnd
    elif k=="remove": died[p["id"]]=rnd
SC={"conveyor":1,"splitter":1,"barrier":1,"harvester":5,"launcher":10,"builder_bot":20,"gunner":20,"sentinel":20,"core":0}
# scale timeline for our team
events=[]
for i,e in ents.items():
    if e["team"]!=ourteam: continue
    events.append((born[i],SC.get(e["kind"],0)))
    if i in died: events.append((died[i],-SC.get(e["kind"],0)))
events.sort()
scale={}
cur=100.0
j=0
n=len(turns)
for r in range(n):
    while j<len(events) and events[j][0]<=r:
        cur+=events[j][1]; j+=1
    scale[r]=cur
print("game",tag,"winner",winner,cond,"rounds",n,"ourteam",us)
prev=None
for r in sorted(players):
    a=players[r].get(us,{})
    row=(a.get("ti"),a.get("ammo"))
    if r%20==0 or (prev and row[1]!=prev[1] and r<400):
        sc=scale.get(r,100.0)
        print("r%-4d ti=%-5s ammo=%-5s scale=%5.0f%%  bar=%d sen=%d harv=%d" % (r,a.get("ti"),a.get("ammo"),sc,int(sc/100*3),int(sc/100*30),int(sc/100*20)))
    prev=row
