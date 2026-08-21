"""Extract corpus/events.tsv rows for the frozen Bean counters set (s53 census).
Read-only. Writes scratchpad/s54_116_bc_events.tsv"""
import json, sys, time
FR={}
for l in open('scratchpad/s53_bean_census.jsonl'):
    r=json.loads(l); FR[r['file']]=(r['bc'], r['ver'])
t0=time.time(); n=0; kept=0
out=open('scratchpad/s54_116_bc_events.tsv','w')
with open('corpus/events.tsv') as f:
    hdr=f.readline(); out.write(hdr)
    for line in f:
        n+=1
        fn=line[:line.index('\t')]
        if fn in FR:
            out.write(line); kept+=1
out.close()
print('scanned',n,'kept',kept,'%.1fs'%(time.time()-t0))
