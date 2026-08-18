#!/bin/bash
# GATED CONTROL: archipelago vs _v468kladturbo, 36 games, both seats.
# archipelago's signature (26,26,(5,5),(19,19)) is in FS_MAP_SKIP, so the
# ferry-siege REFUSES and the bot plays the incumbent raid doctrine.  All three
# v516 changes are siege-path, so ANY movement here is an alarm.
# Bar: v515 measured 26/36 (72.2%).
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v516_build
export OPP=bots/_v468kladturbo
export MAPS=archipelago
export SEEDS=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18
export PAR=4
for arm in bots/_v516teardown "$B/arms/parent515"; do
  n=$(basename "$arm")
  mkdir -p "$B/gated/$n"
  .venv/bin/python "$B/run_grid.py" "$arm" "$B/gated/$n/res.tsv" \
      "$B/gated/$n/rep" "$B/gated/$n/log" > "$B/gated/$n/run.log" 2>&1
  echo "GATED $n done $(date -u +%H:%M:%SZ)"
done
echo "GATED DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
