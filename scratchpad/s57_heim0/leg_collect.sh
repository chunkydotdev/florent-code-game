#!/bin/zsh
# Poll both leg cells to completion, then full audit. In-game league.
cd /Users/junghard/Projects/Work/florent-code-game
G=d36c553f-9e7c-497a-a786-06df834291da
J=ea021442-b0d7-4dbd-8bba-be492e16738c
for i in $(seq 1 40); do
  sleep 10
  SG=$(.venv/bin/fcode match info $G --json 2>/dev/null | .venv/bin/python -c "import json,sys; m=json.load(sys.stdin); m=m.get('match',m); print(m.get('status'))" 2>/dev/null)
  SJ=$(.venv/bin/fcode match info $J --json 2>/dev/null | .venv/bin/python -c "import json,sys; m=json.load(sys.stdin); m=m.get('match',m); print(m.get('status'))" 2>/dev/null)
  [ "$SG" = "complete" ] && [ "$SJ" = "complete" ] && break
done
echo "== CELL RESULTS =="
for MID in $G $J; do
  .venv/bin/fcode match info $MID --json 2>/dev/null | .venv/bin/python -c "
import json,sys
d=json.load(sys.stdin); m=d.get('match',d)
print(m.get('teamAName'),'vs',m.get('teamBName'),'|',m.get('status'),'| score',m.get('teamAScore'),'-',m.get('teamBScore'))
for g in (m.get('games') or []):
    print('  game', g.get('index',g.get('gameNumber','?')),'winner:',g.get('winnerName',g.get('winner','?')),'| turns:',g.get('turns',g.get('rounds','?')),'| cond:',g.get('condition',g.get('winCondition','?')))"
done
echo "== BOUNDARY AUDIT (per-match versions around the window) =="
.venv/bin/fcode match list --mine --type ladder --json 2>/dev/null | .venv/bin/python -c "
import json,sys
d=json.load(sys.stdin); ms=d.get('matches',d) if isinstance(d,dict) else d
for m in ms[:4]:
    print(m.get('createdAt'),'|',m.get('teamAName'),'v'+str(m.get('teamAVersion')),'vs',m.get('teamBName'),'v'+str(m.get('teamBVersion')))"
