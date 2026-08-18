#!/bin/bash
# MORE DRAWS on the headline pair.  Reason: the measured same-config spread on
# this fixture is ~9-11 games in 90, so a 3-block read is one draw of a noisy
# instrument.  Blocks G..L, fresh seeds, both arms concurrent on each seed.
set -e
cd /Users/junghard/Projects/Work/florent-code-game
S=scratchpad/s51_v515_build
export PAR=4
for blk in G:8200 H:8300 I:8400 J:8500 K:8600 L:8700; do
  L2=${blk%%:*}; SEED=${blk##*:}
  for arm in v515 p514nd; do
    .venv/bin/python $S/run_grid.py $S/arms/$arm ${arm}${L2} \
      $S/grid/${arm}${L2}.tsv 6 $SEED - > $S/grid/${arm}${L2}.log 2>&1
  done
done
echo MOREDONE > $S/grid/more.run
