#!/bin/bash
# HEADLINE: 5 siege maps x 6 reps x 3 blocks, n=90/arm, paired seeds, vs
# _v488beltbreak2.  v515 fired config and THE PARENT-WITH-DOOR-OFF baseline run
# CONCURRENTLY on the same seeds (the parent report's own seeds: 7400/7500/7600).
set -e
cd /Users/junghard/Projects/Work/florent-code-game
S=scratchpad/s51_v515_build
export PAR=4
for blk in A:7400 B:7500 C:7600; do
  L=${blk%%:*}; SEED=${blk##*:}
  for arm in v515 p514nd; do
    .venv/bin/python $S/run_grid.py $S/arms/$arm ${arm}${L} \
      $S/grid/${arm}${L}.tsv 6 $SEED - > $S/grid/${arm}${L}.log 2>&1
    echo "done ${arm}${L}"
  done
done
echo HEADLINEDONE > $S/grid/headline.run
