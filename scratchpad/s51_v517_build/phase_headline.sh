#!/bin/bash
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v517_build
for a in 517 516 fo; do
  dirs=""
  for i in $(seq 1 15); do dirs="$dirs $B/grid/b$i/rep$a"; done
  .venv/bin/python $B/phase.py "arm$a" $dirs > "$B/phase_$a.txt" 2>&1 &
done
wait
echo PHASEDONE
