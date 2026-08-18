import os,re,subprocess
from concurrent.futures import ThreadPoolExecutor
REPO="/Users/junghard/Projects/Work/florent-code-game"
FC=REPO+"/.venv/bin/fcode"
S=os.path.dirname(os.path.abspath(__file__))
ARM=S+"/demo"; OPP=REPO+"/bots/_v488beltbreak2"
JOBS=[]
for m,sd,ordA in (("midgard",7501,False),("drakkarfjord",7405,False),
                  ("drakkarfjord",7503,False),("glacierkeep",7404,True),
                  ("glacierkeep",7402,True),("drakkarfjord",7501,False),
                  ("nordkap",7400,True),("atoll",7402,True)):
    for i in range(3):
        JOBS.append((m,sd,ordA,i))
def one(j):
    m,sd,ordA,i=j
    tag="%s_%d_%d"%(m,sd,i)
    rp=S+"/demoreps/%s.replay26"%tag
    first,second=(ARM,OPP) if ordA else (OPP,ARM)
    pr=subprocess.run([FC,"run",first,second,REPO+"/maps/%s.map26"%m,"--seed",str(sd),
                       "--tle","10","--replay",rp],capture_output=True,text=True,timeout=900)
    open(S+"/demoreps/%s.err"%tag,"w").write(pr.stderr)
    mm=re.search(r"Winner:\s+(\S+)\s+\((.*), turn (\d+)\)",pr.stdout)
    if not mm: return tag+"\tNOWIN"
    win,cond,turn=mm.group(1),mm.group(2),int(mm.group(3))
    ours = 1 if win=="demo" else 0
    e=pr.stderr
    return "\t".join([tag,str(ours),cond,str(turn),
                      "door=%d"%e.count("FS DOOR "),"sent=%d"%e.count("FS SENTINEL "),
                      "seal=%d"%e.count("FS SEAL "),"tb=%d"%e.count("Traceback")])
with ThreadPoolExecutor(max_workers=6) as ex:
    for r in ex.map(one,JOBS): print(r)
