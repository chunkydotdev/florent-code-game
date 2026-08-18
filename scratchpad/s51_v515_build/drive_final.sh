#!/bin/bash
# DEFINITIVE CONCURRENT BATTERY.  Seven arms, six fresh blocks, INTERLEAVED
# WITHIN each block so every arm meets the same machine-load conditions on the
# same seeds.  Why interleaved: the earlier passes ran arms in separate drivers
# minutes apart, and two byte-equivalent configs (flagoff, p514nd) came out
# 20 games apart in 270 -- which is either fixture noise or a run-order effect,
# and the design that cannot be argued about is the one where every arm shares
# every block.
set -e
cd /Users/junghard/Projects/Work/florent-code-game
S=scratchpad/s51_v515_build
export PAR=4
for blk in M:8800 N:8900 O:9000 P:9100 Q:9200 R:9300; do
  L=${blk%%:*}; SEED=${blk##*:}
  for arm in parent514 flagoff p514nd v515 only1 only2 only3; do
    .venv/bin/python $S/run_grid.py $S/arms/$arm ${arm}${L} \
      $S/grid/${arm}${L}.tsv 6 $SEED - > $S/grid/${arm}${L}.log 2>&1
  done
  echo "block $L done"
done
echo FINALDONE > $S/grid/final.run
