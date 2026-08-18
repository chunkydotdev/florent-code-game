#!/bin/bash
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v519_build
N="${N:-13}"
for a in parent v519 msoff; do
  dirs=""
  for i in $(seq 1 "$N"); do dirs="$dirs $B/grid/b$i/rep$a"; done
  .venv/bin/python $B/phase.py "arm_$a" $dirs > "$B/phase_$a.txt" 2>&1 &
done
wait
echo PHASEDONE
