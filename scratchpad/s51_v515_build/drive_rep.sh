#!/bin/bash
# SAME-CONFIG, SAME-SEED REPEAT of headline blocks A/B/C, both arms.
# Why: the parent's `nodoor` arm read 53/90 on these exact seeds at PAR=6 and
# this session's byte-identical `p514nd` read 42/90 at PAR=4.  This third draw
# measures the same-config spread directly instead of attributing it.
set -e
cd /Users/junghard/Projects/Work/florent-code-game
S=scratchpad/s51_v515_build
export PAR=4
for blk in A:7400 B:7500 C:7600; do
  L=${blk%%:*}; SEED=${blk##*:}
  for arm in p514nd v515; do
    .venv/bin/python $S/run_grid.py $S/arms/$arm ${arm}R${L} \
      $S/grid/${arm}R${L}.tsv 6 $SEED - > $S/grid/${arm}R${L}.log 2>&1
  done
done
echo REPDONE > $S/grid/rep.run
