#!/bin/bash
set -e
cd /Users/junghard/Projects/Work/florent-code-game
S=scratchpad/s51_v515_build
export PAR=4
for blk in A:7400 B:7500 C:7600; do
  L=${blk%%:*}; SEED=${blk##*:}
  for arm in only1 only2 only3; do
    .venv/bin/python $S/run_grid.py $S/arms/$arm ${arm}${L} \
      $S/grid/${arm}${L}.tsv 6 $SEED - > $S/grid/${arm}${L}.log 2>&1
  done
done
.venv/bin/python $S/run_grid.py $S/arms/flagoff flagoffC $S/grid/flagoffC.tsv 6 7600 - > $S/grid/flagoffC.log 2>&1
echo ONLYDONE > $S/grid/only.run
