#!/bin/bash
# FLAG-OFF, POWERED.  The n=60 read was 34/60 (flag-off) vs 40/60 (parent) with
# the whole gap on atoll (2/12 vs 7/12) -- inside the one-draw law but worth
# buying out, because the ONE thing the master flag must do is reproduce the
# parent.  180 games each, interleaved blocks, fresh seeds.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v516_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap
export PAR=2
for i in 1 2 3 4 5 6; do
  s=$((100+i*3)); export SEEDS="$s,$((s+1)),$((s+2))"
  mkdir -p "$B/fo/b$i"
  .venv/bin/python "$B/run_grid.py" "$B/arms/flagoff" "$B/fo/b$i/flagoff.tsv" \
      "$B/fo/b$i/repf" "$B/fo/b$i/logf" > "$B/fo/b$i/f.log" 2>&1 &
  A=$!
  .venv/bin/python "$B/run_grid.py" "$B/arms/parent515" "$B/fo/b$i/parent.tsv" \
      "$B/fo/b$i/repp" "$B/fo/b$i/logp" > "$B/fo/b$i/p.log" 2>&1 &
  Bp=$!
  wait $A $Bp
  echo "FO BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "FLAGOFF2 DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
