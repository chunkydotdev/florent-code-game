#!/bin/bash
# FLAG-OFF, THIRD FIXTURE: the HEADLINE seeds (1-45), so the flag-off tree can be
# compared against the headline's own parent arm at n=450 without re-running it.
# ⛔ NOT time-adjacent to that parent run, so this is a weaker comparison than an
# interleaved block; it is here for the POOLED n, and it says so.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v518_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap
export PAR=4
for i in $(seq 1 15); do
  s1=$((i*3-2)); s2=$((i*3-1)); s3=$((i*3))
  export SEEDS="$s1,$s2,$s3"
  mkdir -p "$B/fo3/b$i"
  .venv/bin/python "$B/run_grid.py" "$B/arms/flagoff" "$B/fo3/b$i/flagoff.tsv" \
      "$B/fo3/b$i/repf" "$B/fo3/b$i/logf" > "$B/fo3/b$i/f.log" 2>&1
  echo "FO3 BLOCK $i done $(date -u +%H:%M:%SZ)"
done
echo "FLAGOFF3 DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
