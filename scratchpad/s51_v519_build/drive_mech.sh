#!/bin/bash
# MECHANISM ARMS, n=30 each (6 maps x 3 seeds x 2 seats = 36 actually), every
# instrument ON in every arm so the tables read off the same volume of trace.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v519_build
export OPP=bots/_v488beltbreak2
export MAPS=atoll,drakkarfjord,glacierkeep,midgard,nordkap,yulerune
export SEEDS=1,2,3
export PAR=2
for a in "$@"; do
  mkdir -p "$B/mech/$a"
  .venv/bin/python "$B/run_grid.py" "$B/arms/$a" "$B/mech/$a/grid.tsv" "$B/mech/$a/rep" "$B/mech/$a/log" >/dev/null 2>&1
  echo "MECH $a done $(date -u +%H:%M:%SZ)"
done
