#!/bin/bash
# GATED CONTROL: archipelago (signature in FS_MAP_SKIP) vs _v468kladturbo.
# Every v519 change is siege-path, and on a gated board `_fs_gate` already
# refuses -- so BOTH changes are structurally unreachable and the arms must
# land on the same number.  Two draws of 36, per the v518 two-draw design.
set -u
cd /Users/junghard/Projects/Work/florent-code-game
B=scratchpad/s51_v519_build
export OPP=bots/_v468kladturbo
export MAPS=archipelago
export PAR=3
for d in 1 2; do
  if [ "$d" = 1 ]; then export SEEDS=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18
  else export SEEDS=19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36; fi
  mkdir -p "$B/gated/d$d"
  .venv/bin/python "$B/run_grid.py" bots/_v519cripple "$B/gated/d$d/v519.tsv" "$B/gated/d$d/repv519" "$B/gated/d$d/logv519" >/dev/null 2>&1 &
  P1=$!
  .venv/bin/python "$B/run_grid.py" "$B/arms/parent" "$B/gated/d$d/parent.tsv" "$B/gated/d$d/repparent" "$B/gated/d$d/logparent" >/dev/null 2>&1 &
  P2=$!
  echo "$P1 $P2" >> "$B/PIDS"
  wait $P1 $P2
  echo "GATED draw $d done $(date -u +%H:%M:%SZ)"
done
