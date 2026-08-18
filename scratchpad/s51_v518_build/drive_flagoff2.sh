#!/bin/bash
# FLAG-OFF, SECOND INDEPENDENT FIXTURE, n=180 each on a DIFFERENT seed range.
# ⛔ v517 surprise 5 is the reason this exists: the SAME flag-off-vs-parent
# comparison read +5.6 pp on one fixture and -2.0 pp on another, on code that is
# provably identical on every path.  One battery cannot settle a null.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v518_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap
export PAR=2
for i in 1 2 3 4 5 6; do
  s=$((400+i*3)); export SEEDS="$s,$((s+1)),$((s+2))"
  mkdir -p "$B/fo2/b$i"
  .venv/bin/python "$B/run_grid.py" "$B/arms/flagoff" "$B/fo2/b$i/flagoff.tsv" \
      "$B/fo2/b$i/repf" "$B/fo2/b$i/logf" > "$B/fo2/b$i/f.log" 2>&1 &
  A=$!
  .venv/bin/python "$B/run_grid.py" "$B/arms/parent" "$B/fo2/b$i/parent.tsv" \
      "$B/fo2/b$i/repp" "$B/fo2/b$i/logp" > "$B/fo2/b$i/p.log" 2>&1 &
  Bp=$!
  wait $A $Bp
  echo "FO2 BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "FLAGOFF2 DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
