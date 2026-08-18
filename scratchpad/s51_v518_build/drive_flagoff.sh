#!/bin/bash
# FLAG-OFF, BEHAVIOURAL, n=180 each on FRESH seeds, interleaved blocks.
# A structural diff and an AST scan are not enough (v515 finding 3): the one
# thing the master flag must do is reproduce the parent.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v518_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap
export PAR=2
for i in 1 2 3 4 5 6; do
  s=$((200+i*3)); export SEEDS="$s,$((s+1)),$((s+2))"
  mkdir -p "$B/fo/b$i"
  .venv/bin/python "$B/run_grid.py" "$B/arms/flagoff" "$B/fo/b$i/flagoff.tsv" \
      "$B/fo/b$i/repf" "$B/fo/b$i/logf" > "$B/fo/b$i/f.log" 2>&1 &
  A=$!
  .venv/bin/python "$B/run_grid.py" "$B/arms/parent" "$B/fo/b$i/parent.tsv" \
      "$B/fo/b$i/repp" "$B/fo/b$i/logp" > "$B/fo/b$i/p.log" 2>&1 &
  Bp=$!
  wait $A $Bp
  echo "FO BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "FLAGOFF DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
