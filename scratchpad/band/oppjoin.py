import csv, json, collections
OURID='379a5d80-9921-4c9e-949b-f9b1dcba16be'
info={}
def take(r, tb):
    for s,o in (('A','B'),('B','A')):
        if r['team%sId'%s]==OURID:
            info[r['id']]=dict(oppid=r['team%sId'%o], oppname=r['team%sName'%o],
                               oppver=r['team%sVersion'%o], ourver2=r['team%sVersion'%s], tb=tb)
for r in csv.DictReader(open('corpus/league_matches.tsv'),delimiter='\t'): take(r,'?')
for r in csv.DictReader(open('corpus/league_elo_log.tsv'),delimiter='\t'):
    if r['triggeredBy']=='ladder': take(r,'ladder')
rows=[m for m in json.load(open('scratchpad/band/matches.json')) if m['delta'] is not None]
hit=sum(1 for m in rows if m['mid'] in info)
print('opponent identity resolved for %d of %d our rated ladder matches'%(hit,len(rows)))
badver=sum(1 for m in rows if m['mid'] in info and info[m['mid']]['oppver'] in ('None','',None))
print('  oppver missing/None:',badver)
# our version cross-check
mism=sum(1 for m in rows if m['mid'] in info and info[m['mid']]['ourver2']!=m['ourver'])
print('  CROSS-CHECK our version, corpus ladder_games vs league tape, mismatches:',mism)
for m in rows:
    i=info.get(m['mid'])
    if i: m.update(oppid=i['oppid'], oppname=i['oppname'], oppver=i['oppver'])
json.dump(rows,open('scratchpad/band/matches2.json','w'))
c=collections.Counter(m.get('oppname') for m in rows if m.get('oppname'))
print('distinct opponents faced (rated ladder):',len(c))
print('top 15 by matches:'); 
for k,v in c.most_common(15): print('   %-28s %3d'%(k,v))
