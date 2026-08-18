#!/bin/bash
# GATED CONTROL: archipelago vs _v468kladturbo, POOLED n=72 (two draws of 36).
# archipelago's signature (26,26,(5,5),(19,19)) is in FS_MAP_SKIP, so `_fs_gate`
# REFUSES and the whole ferry-siege path is unreachable.  Every v518 change is
# siege-path (the ladder, `_fs_stand_target`, and a Core branch inside the
# `fs_live` siege block), so ANY movement here is an alarm.
# ⛔ TWO DRAWS, because the v516 leg showed a single 36-draw alarms falsely and
# the v517 leg reproduced that (23/36 vs 25/36 on draw 1, 29/36 vs 27/36 on
# draw 2, identical pooled).
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v518_build
export OPP=bots/_v468kladturbo
export MAPS=archipelago
export PAR=4
for draw in 1 2; do
  if [ "$draw" = 1 ]; then
    export SEEDS=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18
  else
    export SEEDS=19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36
  fi
  for arm in bots/_v518fastsent "$B/arms/f30" "$B/arms/parent"; do
    n=$(basename "$arm")
    mkdir -p "$B/gated/d$draw/$n"
    .venv/bin/python "$B/run_grid.py" "$arm" "$B/gated/d$draw/$n/res.tsv" \
        "$B/gated/d$draw/$n/rep" "$B/gated/d$draw/$n/log" \
        > "$B/gated/d$draw/$n/run.log" 2>&1
    echo "GATED draw$draw $n done $(date -u +%H:%M:%SZ)"
  done
done
echo "GATED DONE $(date -u +%Y-%m-%dT%H:%M:%SZ)"
