#!/bin/bash
# Extend the single-flag isolation from n=90 to n=270/arm.  At n=90 every arm
# sat inside the measured block-to-block spread, so the n=90 table cannot
# attribute anything; this buys the power before the verdict is written.
set -e
cd /Users/junghard/Projects/Work/florent-code-game
S=scratchpad/s51_v515_build
export PAR=4
for blk in D:7700 E:7800 F:7900 G:8200 H:8300 I:8400; do
  L=${blk%%:*}; SEED=${blk##*:}
  for arm in flagoff only1 only2 only3; do
    .venv/bin/python $S/run_grid.py $S/arms/$arm ${arm}${L} \
      $S/grid/${arm}${L}.tsv 6 $SEED - > $S/grid/${arm}${L}.log 2>&1
  done
done
echo ONLY2DONE > $S/grid/only2.run
