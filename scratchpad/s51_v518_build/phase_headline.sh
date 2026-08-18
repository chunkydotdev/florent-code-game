#!/bin/bash
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v518_build
N="${N:-15}"
for a in parent f60 f45 f30; do
  dirs=""
  for i in $(seq 1 "$N"); do dirs="$dirs $B/grid/b$i/rep$a"; done
  .venv/bin/python $B/phase.py "arm_$a" $dirs > "$B/phase_$a.txt" 2>&1 &
done
wait
echo PHASEDONE
