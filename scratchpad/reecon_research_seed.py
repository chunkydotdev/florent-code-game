"""Independent re-decode of ti_collected / ammo_converted / shots / heals per (file,team,round-cap).
Written fresh (not reusing corpus/econ.tsv) because econ.tsv rows for 0033 v55-v57 are defective:
turns_run==0 and cpu_sum_us==0 while thousands of botOutput events exist."""
import sys, pickle, collections, os
sys.path.insert(0,"tools")
from replay_census import fields, WIRE_LEN, WIRE_VARINT
S=os.path.dirname(os.path.abspath(__file__))
def decode(f, caps=(50,100,150,10**9)):
    data=open('replay_archive/'+f,'rb').read()
    mapbuf=None; turns=[]
    for num,wire,value in fields(data):
        if num==1 and wire==WIRE_LEN: mapbuf=value
        elif num==3 and wire==WIRE_LEN: turns.append(value)
    pos_team={}; pos_kind={}; id_pos={}
    out={t:{c:{'ti':0,'ammo_conv':0,'shots':0,'heals':0,'attacks':0,'builds':0,'bo':0,'cpu_max':0,'cpu_sum':0} for c in caps} for t in (0,1)}
    for rnd,tb in enumerate(turns):
        for _n,_w,ub in fields(tb):
            for un,_uw,uv in fields(ub):
                if un==1:
                    for en,_ew,eb in fields(uv):
                        if en!=1: continue
                        d={};sub={}
                        for k,w2,v in fields(eb):
                            if w2==WIRE_VARINT: d[k]=v
                            else: sub[k]=v
                        p=sub.get(3)
                        if p is not None:
                            pd={k:v for k,w2,v in fields(p) if w2==WIRE_VARINT}
                            xy=(pd.get(1,0),pd.get(2,0))
                            pos_team[xy]=d.get(2,0); id_pos[d.get(1)]=xy
                            for kk in (21,22,23):
                                if kk in sub or kk in d: pos_kind[xy]=kk
                elif un==9:
                    d={k:v for k,w2,v in fields(uv) if w2==WIRE_VARINT}
                    xy=id_pos.get(d.get(1)); t=pos_team.get(xy) if xy else None
                    if t is None: continue
                    for c in caps:
                        if rnd<=c:
                            o=out[t][c]; o['bo']+=1; o['cpu_sum']+=d.get(3,0); o['cpu_max']=max(o['cpu_max'],d.get(3,0))
                elif un==12:
                    pd=None
                    for fn,fw,fv in fields(uv):
                        if fn==1 and fw==WIRE_LEN:
                            pd={k:v for k,w2,v in fields(fv) if w2==WIRE_VARINT}; break
                    if pd:
                        t=pos_team.get((pd.get(1,0),pd.get(2,0)))
                        if t is not None:
                            for c in caps:
                                if rnd<=c: out[t][c]['shots']+=1
                elif un in (15,16,13):
                    d={k:v for k,w2,v in fields(uv) if w2==WIRE_VARINT}
                    xy=id_pos.get(d.get(1)); t=pos_team.get(xy) if xy else None
                    if t is None: continue
                    key='heals' if un==15 else 'builds' if un==16 else 'attacks'
                    for c in caps:
                        if rnd<=c: out[t][c][key]+=1
                elif un==14:
                    d={k:v for k,w2,v in fields(uv) if w2==WIRE_VARINT}
                    t=d.get(1,0)
                    if t in out:
                        for c in caps:
                            if rnd<=c: out[t][c]['ammo_conv']+=d.get(2,0)
                elif un==6:
                    for pn,_pw,pv in fields(uv):
                        if pn!=1: continue
                        for tn,_tw,tv in fields(pv):
                            if tn not in (1,2): continue
                            d={k:v for k,w2,v in fields(tv) if w2==WIRE_VARINT}
                            for c in caps:
                                if rnd<=c: out[tn-1][c]['ti']=d.get(4,0)
    return out
if __name__=='__main__':
    info=pickle.load(open(S+'/prof.pkl','rb'))['info']
    sel=[f for f in info if info[f]['ver'] in ('56','57')]
    res={}
    for i,f in enumerate(sel):
        try: res[f]=decode(f)
        except Exception as e: print("ERR",f,e)
    pickle.dump(res,open(S+'/reecon.pkl','wb'))
    print("decoded",len(res))
